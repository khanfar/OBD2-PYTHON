#!/usr/bin/env python3
"""
OBD-2 Real-time Dashboard
Created by Khanfar Systems
"""

import tkinter as tk
from tkinter import ttk
import obd
import threading
import time
from typing import Dict, List
import json
from pathlib import Path
import logging

class OBDDashboard:
    def __init__(self, root):
        """Initialize the OBD dashboard"""
        self.root = root
        self.root.title("OBD-2 Dashboard")
        self.connection = None
        self.monitoring = False
        self.setup_logging()
        self.setup_ui()
        self.load_config()

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("dashboard.log"),
                logging.StreamHandler()
            ]
        )

    def setup_ui(self):
        """Setup the dashboard UI"""
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Connection frame
        self.connection_frame = ttk.LabelFrame(self.main_frame, text="Connection", padding="5")
        self.connection_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.conn_status = ttk.Label(self.connection_frame, text="Not Connected")
        self.conn_status.grid(row=0, column=0, padx=5)
        
        self.connect_btn = ttk.Button(self.connection_frame, text="Connect", command=self.connect)
        self.connect_btn.grid(row=0, column=1, padx=5)

        # Data display frame
        self.data_frame = ttk.LabelFrame(self.main_frame, text="Vehicle Data", padding="5")
        self.data_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # Initialize data labels
        self.data_labels: Dict[str, ttk.Label] = {}
        self.setup_data_labels()

        # Control frame
        self.control_frame = ttk.LabelFrame(self.main_frame, text="Controls", padding="5")
        self.control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.start_btn = ttk.Button(self.control_frame, text="Start Monitoring", 
                                  command=self.start_monitoring)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = ttk.Button(self.control_frame, text="Stop Monitoring", 
                                 command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=5)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, 
                                  relief=tk.SUNKEN)
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))

    def setup_data_labels(self):
        """Setup labels for OBD data display"""
        parameters = [
            ("RPM", "Engine RPM"),
            ("SPEED", "Vehicle Speed"),
            ("THROTTLE_POS", "Throttle Position"),
            ("ENGINE_LOAD", "Engine Load"),
            ("COOLANT_TEMP", "Coolant Temp"),
            ("INTAKE_TEMP", "Intake Temp"),
            ("MAF", "Mass Air Flow"),
            ("FUEL_LEVEL", "Fuel Level")
        ]

        for i, (key, name) in enumerate(parameters):
            frame = ttk.Frame(self.data_frame)
            frame.grid(row=i//2, column=i%2, padx=5, pady=2, sticky=(tk.W, tk.E))
            
            ttk.Label(frame, text=f"{name}:").grid(row=0, column=0, sticky=tk.W)
            value_label = ttk.Label(frame, text="--")
            value_label.grid(row=0, column=1, sticky=tk.E)
            
            self.data_labels[key] = value_label

    def load_config(self):
        """Load dashboard configuration"""
        config_file = Path("dashboard_config.json")
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    self.config = json.load(f)
            except Exception as e:
                logging.error(f"Error loading config: {e}")
                self.config = self.get_default_config()
        else:
            self.config = self.get_default_config()
            self.save_config()

    def get_default_config(self) -> Dict:
        """Get default dashboard configuration"""
        return {
            "update_interval": 100,  # milliseconds
            "commands": {
                "RPM": "RPM",
                "SPEED": "SPEED",
                "THROTTLE_POS": "THROTTLE_POS",
                "ENGINE_LOAD": "ENGINE_LOAD",
                "COOLANT_TEMP": "COOLANT_TEMP",
                "INTAKE_TEMP": "INTAKE_TEMP",
                "MAF": "MAF",
                "FUEL_LEVEL": "FUEL_LEVEL"
            }
        }

    def save_config(self):
        """Save dashboard configuration"""
        try:
            with open("dashboard_config.json", 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving config: {e}")

    def connect(self):
        """Connect to OBD adapter"""
        try:
            self.connection = obd.OBD()
            if self.connection.is_connected():
                self.conn_status.config(text="Connected")
                self.connect_btn.config(state=tk.DISABLED)
                self.start_btn.config(state=tk.NORMAL)
                self.status_var.set("Connected to OBD adapter")
                logging.info("Connected to OBD adapter")
            else:
                self.status_var.set("Connection failed")
                logging.error("Connection failed")
        except Exception as e:
            self.status_var.set(f"Connection error: {str(e)}")
            logging.error(f"Connection error: {e}")

    def start_monitoring(self):
        """Start monitoring OBD data"""
        if not self.connection:
            return

        self.monitoring = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set("Monitoring started")

        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.update_data)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def stop_monitoring(self):
        """Stop monitoring OBD data"""
        self.monitoring = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("Monitoring stopped")

    def update_data(self):
        """Update OBD data in the dashboard"""
        while self.monitoring:
            try:
                for key, cmd_name in self.config["commands"].items():
                    if hasattr(obd.commands, cmd_name):
                        cmd = getattr(obd.commands, cmd_name)
                        response = self.connection.query(cmd)
                        
                        if not response.is_null():
                            self.root.after(0, self.update_label, key, str(response.value))
                        else:
                            self.root.after(0, self.update_label, key, "--")
                
                time.sleep(self.config["update_interval"] / 1000)
            except Exception as e:
                logging.error(f"Error updating data: {e}")
                self.root.after(0, self.stop_monitoring)
                break

    def update_label(self, key: str, value: str):
        """Update a specific data label"""
        if key in self.data_labels:
            self.data_labels[key].config(text=value)

    def on_closing(self):
        """Handle window closing"""
        self.monitoring = False
        if self.connection:
            self.connection.close()
        self.root.destroy()

def main():
    """Main function to run the dashboard"""
    root = tk.Tk()
    dashboard = OBDDashboard(root)
    root.protocol("WM_DELETE_WINDOW", dashboard.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
