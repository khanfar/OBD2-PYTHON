#!/usr/bin/env python3
"""
OBD-2 Data Logger
Created by Khanfar Systems
"""

import csv
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Any
import obd
from pathlib import Path

class OBDDataLogger:
    def __init__(self, log_dir: str = "logs"):
        """Initialize the OBD data logger"""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.connection = None
        self.logging = False
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_dir / "obd_logger.log"),
                logging.StreamHandler()
            ]
        )

    def connect(self) -> bool:
        """Establish connection with OBD adapter"""
        try:
            self.connection = obd.OBD()
            return self.connection.is_connected()
        except Exception as e:
            logging.error(f"Connection failed: {e}")
            return False

    def get_supported_commands(self) -> List[str]:
        """Get list of supported OBD commands"""
        if not self.connection:
            return []
        return [str(cmd) for cmd in self.connection.supported_commands]

    def log_to_csv(self, commands: List[obd.commands], duration: int = 60, 
                   interval: float = 1.0) -> str:
        """Log OBD data to CSV file"""
        if not self.connection:
            logging.error("No connection established")
            return ""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = self.log_dir / f"obd_log_{timestamp}.csv"
        
        headers = ["Timestamp"] + [str(cmd) for cmd in commands]
        
        try:
            with open(csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                
                start_time = time.time()
                while time.time() - start_time < duration:
                    row = [datetime.now().isoformat()]
                    for cmd in commands:
                        response = self.connection.query(cmd)
                        row.append(str(response.value) if not response.is_null() else "NULL")
                    writer.writerow(row)
                    time.sleep(interval)
                    
            logging.info(f"Data logged to {csv_file}")
            return str(csv_file)
        except Exception as e:
            logging.error(f"Error logging data: {e}")
            return ""

    def log_to_json(self, commands: List[obd.commands], duration: int = 60, 
                    interval: float = 1.0) -> str:
        """Log OBD data to JSON file"""
        if not self.connection:
            logging.error("No connection established")
            return ""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file = self.log_dir / f"obd_log_{timestamp}.json"
        
        data = []
        try:
            start_time = time.time()
            while time.time() - start_time < duration:
                entry = {
                    "timestamp": datetime.now().isoformat(),
                    "data": {}
                }
                for cmd in commands:
                    response = self.connection.query(cmd)
                    entry["data"][str(cmd)] = str(response.value) if not response.is_null() else None
                data.append(entry)
                time.sleep(interval)

            with open(json_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            logging.info(f"Data logged to {json_file}")
            return str(json_file)
        except Exception as e:
            logging.error(f"Error logging data: {e}")
            return ""

    def continuous_monitor(self, commands: List[obd.commands], 
                         callback: callable = None) -> None:
        """Continuously monitor OBD data with optional callback"""
        if not self.connection:
            logging.error("No connection established")
            return

        self.logging = True
        try:
            while self.logging:
                data = {}
                for cmd in commands:
                    response = self.connection.query(cmd)
                    data[str(cmd)] = str(response.value) if not response.is_null() else None
                
                if callback:
                    callback(data)
                else:
                    print(data)
                time.sleep(0.1)
        except KeyboardInterrupt:
            logging.info("Monitoring stopped by user")
        except Exception as e:
            logging.error(f"Error in continuous monitoring: {e}")
        finally:
            self.logging = False

    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.logging = False

    def analyze_log_file(self, log_file: str) -> Dict[str, Any]:
        """Analyze logged data file"""
        if not Path(log_file).exists():
            logging.error(f"Log file not found: {log_file}")
            return {}

        try:
            if log_file.endswith('.csv'):
                return self._analyze_csv(log_file)
            elif log_file.endswith('.json'):
                return self._analyze_json(log_file)
            else:
                logging.error("Unsupported file format")
                return {}
        except Exception as e:
            logging.error(f"Error analyzing log file: {e}")
            return {}

    def _analyze_csv(self, csv_file: str) -> Dict[str, Any]:
        """Analyze CSV log file"""
        analysis = {"parameters": {}}
        
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames[1:]  # Skip timestamp
            
            for header in headers:
                analysis["parameters"][header] = {
                    "min": float('inf'),
                    "max": float('-inf'),
                    "values": []
                }
            
            for row in reader:
                for header in headers:
                    try:
                        value = float(row[header])
                        analysis["parameters"][header]["values"].append(value)
                        analysis["parameters"][header]["min"] = min(
                            analysis["parameters"][header]["min"], value)
                        analysis["parameters"][header]["max"] = max(
                            analysis["parameters"][header]["max"], value)
                    except (ValueError, TypeError):
                        continue
            
            # Calculate averages
            for param in analysis["parameters"].values():
                if param["values"]:
                    param["avg"] = sum(param["values"]) / len(param["values"])
                del param["values"]  # Remove raw values to save memory
                
        return analysis

    def _analyze_json(self, json_file: str) -> Dict[str, Any]:
        """Analyze JSON log file"""
        with open(json_file, 'r') as f:
            data = json.load(f)
            
        analysis = {"parameters": {}}
        
        for entry in data:
            for param, value in entry["data"].items():
                if param not in analysis["parameters"]:
                    analysis["parameters"][param] = {
                        "min": float('inf'),
                        "max": float('-inf'),
                        "values": []
                    }
                
                try:
                    value = float(value) if value is not None else None
                    if value is not None:
                        analysis["parameters"][param]["values"].append(value)
                        analysis["parameters"][param]["min"] = min(
                            analysis["parameters"][param]["min"], value)
                        analysis["parameters"][param]["max"] = max(
                            analysis["parameters"][param]["max"], value)
                except (ValueError, TypeError):
                    continue
        
        # Calculate averages
        for param in analysis["parameters"].values():
            if param["values"]:
                param["avg"] = sum(param["values"]) / len(param["values"])
            del param["values"]  # Remove raw values to save memory
            
        return analysis

    def close(self):
        """Close the OBD connection"""
        if self.connection:
            self.connection.close()
            logging.info("OBD connection closed")

def main():
    """Main function demonstrating logger usage"""
    logger = OBDDataLogger()
    
    print("Connecting to OBD adapter...")
    if logger.connect():
        print("Connected successfully!")
        
        # Get supported commands
        commands = [
            obd.commands.RPM,
            obd.commands.SPEED,
            obd.commands.THROTTLE_POS,
            obd.commands.ENGINE_LOAD
        ]
        
        # Log data to CSV
        print("\nLogging data to CSV (10 seconds)...")
        csv_file = logger.log_to_csv(commands, duration=10, interval=0.5)
        
        # Analyze the log file
        if csv_file:
            print("\nAnalyzing log file...")
            analysis = logger.analyze_log_file(csv_file)
            print("\nAnalysis Results:")
            for param, stats in analysis["parameters"].items():
                print(f"\n{param}:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
        
        logger.close()
    else:
        print("Failed to connect to OBD adapter!")

if __name__ == "__main__":
    main()
