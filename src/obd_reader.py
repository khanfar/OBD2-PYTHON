#!/usr/bin/env python3
"""
OBD-2 Diagnostic Tool
Created by Khanfar Systems
"""

import obd
import time
from typing import List, Dict, Optional

class OBDDiagnosticTool:
    def __init__(self):
        """Initialize the OBD connection"""
        self.connection = None
        self.supported_commands = []

    def connect(self) -> bool:
        """Establish connection with the OBD-II adapter"""
        try:
            self.connection = obd.OBD()
            if self.connection.is_connected():
                self.supported_commands = self.connection.supported_commands
                return True
            return False
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def get_fault_codes(self) -> List[str]:
        """Read and return diagnostic trouble codes"""
        if not self.connection:
            return []
        
        response = self.connection.query(obd.commands.GET_DTC)
        if response.is_null():
            return []
        return response.value

    def clear_fault_codes(self) -> bool:
        """Clear diagnostic trouble codes from the vehicle's computer"""
        if not self.connection:
            return False
        
        response = self.connection.query(obd.commands.CLEAR_DTC)
        return not response.is_null()

    def get_vehicle_info(self) -> Dict[str, str]:
        """Get basic vehicle information"""
        info = {}
        if not self.connection:
            return info

        commands = [
            (obd.commands.VIN, "VIN"),
            (obd.commands.ELM_VERSION, "ELM Version"),
            (obd.commands.ELM_VOLTAGE, "Battery Voltage")
        ]

        for command, key in commands:
            if command in self.supported_commands:
                response = self.connection.query(command)
                if not response.is_null():
                    info[key] = str(response.value)

        return info

    def monitor_live_data(self, duration: int = 10) -> Dict[str, List]:
        """Monitor live data for specified duration in seconds"""
        if not self.connection:
            return {}

        data = {
            "RPM": [],
            "Speed": [],
            "Throttle Position": [],
            "Engine Load": []
        }

        commands = {
            "RPM": obd.commands.RPM,
            "Speed": obd.commands.SPEED,
            "Throttle Position": obd.commands.THROTTLE_POS,
            "Engine Load": obd.commands.ENGINE_LOAD
        }

        start_time = time.time()
        while time.time() - start_time < duration:
            for key, command in commands.items():
                if command in self.supported_commands:
                    response = self.connection.query(command)
                    if not response.is_null():
                        data[key].append(response.value)
            time.sleep(0.5)

        return data

    def close(self):
        """Close the OBD connection"""
        if self.connection:
            self.connection.close()

def main():
    """Main function to demonstrate usage"""
    tool = OBDDiagnosticTool()
    
    print("Connecting to OBD-II adapter...")
    if tool.connect():
        print("Successfully connected!")
        
        # Get vehicle info
        info = tool.get_vehicle_info()
        print("\nVehicle Information:")
        for key, value in info.items():
            print(f"{key}: {value}")
        
        # Read fault codes
        codes = tool.get_fault_codes()
        if codes:
            print("\nFault Codes Found:")
            for code in codes:
                print(code)
        else:
            print("\nNo fault codes found.")
        
        # Monitor live data
        print("\nMonitoring live data for 10 seconds...")
        live_data = tool.monitor_live_data(10)
        for key, values in live_data.items():
            if values:
                avg = sum(values) / len(values)
                print(f"Average {key}: {avg:.2f}")
        
        tool.close()
    else:
        print("Failed to connect to OBD-II adapter!")

if __name__ == "__main__":
    main()
