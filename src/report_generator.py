#!/usr/bin/env python3
"""
OBD-2 Diagnostic Report Generator
Created by Khanfar Systems
"""

import obd
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Template
import webbrowser

class DiagnosticReportGenerator:
    def __init__(self, output_dir: str = "reports"):
        """Initialize the diagnostic report generator"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.connection = None
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.output_dir / "report_generator.log"),
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

    def get_vehicle_info(self) -> Dict[str, Any]:
        """Get basic vehicle information"""
        info = {}
        if not self.connection:
            return info

        commands = [
            (obd.commands.VIN, "VIN"),
            (obd.commands.ELM_VERSION, "ELM Version"),
            (obd.commands.ELM_VOLTAGE, "Battery Voltage"),
            (obd.commands.FUEL_TYPE, "Fuel Type"),
            (obd.commands.DISTANCE_W_MIL, "Distance with MIL")
        ]

        for command, key in commands:
            try:
                response = self.connection.query(command)
                if not response.is_null():
                    info[key] = str(response.value)
            except Exception as e:
                logging.warning(f"Error getting {key}: {e}")

        return info

    def get_dtc_codes(self) -> List[Dict[str, str]]:
        """Get diagnostic trouble codes"""
        if not self.connection:
            return []

        try:
            response = self.connection.query(obd.commands.GET_DTC)
            if response.is_null():
                return []

            codes = []
            for code in response.value:
                codes.append({
                    "code": code[0],
                    "description": self.get_dtc_description(code[0])
                })
            return codes
        except Exception as e:
            logging.error(f"Error getting DTC codes: {e}")
            return []

    def get_dtc_description(self, code: str) -> str:
        """Get description for DTC code"""
        # This is a simplified version. In a real implementation,
        # you would want to use a comprehensive DTC database
        prefix_meanings = {
            "P": "Powertrain",
            "C": "Chassis",
            "B": "Body",
            "U": "Network"
        }
        
        try:
            system = prefix_meanings.get(code[0], "Unknown")
            return f"{system} related issue (Code: {code})"
        except Exception:
            return "Unknown issue"

    def collect_sensor_data(self) -> Dict[str, Any]:
        """Collect current sensor data"""
        if not self.connection:
            return {}

        sensors = {
            "RPM": obd.commands.RPM,
            "Speed": obd.commands.SPEED,
            "Throttle Position": obd.commands.THROTTLE_POS,
            "Engine Load": obd.commands.ENGINE_LOAD,
            "Coolant Temp": obd.commands.COOLANT_TEMP,
            "Intake Temp": obd.commands.INTAKE_TEMP,
            "MAF": obd.commands.MAF,
            "O2 Voltage": obd.commands.O2_B1S1,
            "Fuel Level": obd.commands.FUEL_LEVEL,
            "Timing Advance": obd.commands.TIMING_ADVANCE
        }

        data = {}
        for name, command in sensors.items():
            try:
                response = self.connection.query(command)
                if not response.is_null():
                    data[name] = str(response.value)
            except Exception as e:
                logging.warning(f"Error getting {name}: {e}")

        return data

    def generate_graphs(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Generate graphs from sensor data"""
        graph_files = {}
        
        try:
            # Convert data to pandas DataFrame
            df = pd.DataFrame([data])
            
            # Generate graphs for numeric data
            for column in df.columns:
                try:
                    values = pd.to_numeric(df[column])
                    plt.figure(figsize=(8, 4))
                    plt.bar(column, values[0])
                    plt.title(f"{column} Reading")
                    plt.ylabel("Value")
                    
                    # Save graph
                    graph_file = self.output_dir / f"graph_{column}.png"
                    plt.savefig(graph_file)
                    plt.close()
                    
                    graph_files[column] = str(graph_file)
                except Exception:
                    continue
                    
        except Exception as e:
            logging.error(f"Error generating graphs: {e}")
            
        return graph_files

    def generate_html_report(self, data: Dict[str, Any]) -> str:
        """Generate HTML diagnostic report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_dir / f"diagnostic_report_{timestamp}.html"

        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>OBD-2 Diagnostic Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { background-color: #f8f9fa; padding: 20px; margin-bottom: 20px; }
                .section { margin-bottom: 30px; }
                .data-table { width: 100%; border-collapse: collapse; }
                .data-table td, .data-table th { 
                    border: 1px solid #ddd; 
                    padding: 8px; 
                }
                .data-table tr:nth-child(even) { background-color: #f2f2f2; }
                .graph { margin: 20px 0; }
                .dtc-code { 
                    background-color: #fff3cd;
                    padding: 10px;
                    margin: 5px 0;
                    border-radius: 4px;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>OBD-2 Diagnostic Report</h1>
                <p>Generated: {{ timestamp }}</p>
            </div>

            <div class="section">
                <h2>Vehicle Information</h2>
                <table class="data-table">
                    {% for key, value in vehicle_info.items() %}
                    <tr>
                        <td><strong>{{ key }}</strong></td>
                        <td>{{ value }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </div>

            {% if dtc_codes %}
            <div class="section">
                <h2>Diagnostic Trouble Codes</h2>
                {% for code in dtc_codes %}
                <div class="dtc-code">
                    <strong>{{ code.code }}</strong>: {{ code.description }}
                </div>
                {% endfor %}
            </div>
            {% endif %}

            <div class="section">
                <h2>Sensor Readings</h2>
                <table class="data-table">
                    {% for key, value in sensor_data.items() %}
                    <tr>
                        <td><strong>{{ key }}</strong></td>
                        <td>{{ value }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </div>

            {% if graphs %}
            <div class="section">
                <h2>Sensor Graphs</h2>
                {% for name, path in graphs.items() %}
                <div class="graph">
                    <h3>{{ name }}</h3>
                    <img src="{{ path }}" alt="{{ name }} Graph">
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </body>
        </html>
        """

        try:
            template = Template(template)
            html_content = template.render(
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                vehicle_info=data.get("vehicle_info", {}),
                dtc_codes=data.get("dtc_codes", []),
                sensor_data=data.get("sensor_data", {}),
                graphs=data.get("graphs", {})
            )

            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            return str(report_file)
        except Exception as e:
            logging.error(f"Error generating HTML report: {e}")
            return ""

    def generate_report(self) -> str:
        """Generate complete diagnostic report"""
        if not self.connection:
            logging.error("No connection established")
            return ""

        try:
            # Collect all data
            data = {
                "vehicle_info": self.get_vehicle_info(),
                "dtc_codes": self.get_dtc_codes(),
                "sensor_data": self.collect_sensor_data()
            }

            # Generate graphs
            data["graphs"] = self.generate_graphs(data["sensor_data"])

            # Generate HTML report
            report_file = self.generate_html_report(data)

            if report_file:
                logging.info(f"Report generated: {report_file}")
                return report_file
            return ""

        except Exception as e:
            logging.error(f"Error generating report: {e}")
            return ""

    def close(self):
        """Close the OBD connection"""
        if self.connection:
            self.connection.close()
            logging.info("OBD connection closed")

def main():
    """Main function demonstrating report generation"""
    generator = DiagnosticReportGenerator()
    
    print("Connecting to OBD adapter...")
    if generator.connect():
        print("Connected successfully!")
        
        print("\nGenerating diagnostic report...")
        report_file = generator.generate_report()
        
        if report_file:
            print(f"\nReport generated: {report_file}")
            # Open report in default browser
            webbrowser.open(f"file://{report_file}")
        else:
            print("\nFailed to generate report!")
        
        generator.close()
    else:
        print("Failed to connect to OBD adapter!")

if __name__ == "__main__":
    main()
