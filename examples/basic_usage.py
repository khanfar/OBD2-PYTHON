#!/usr/bin/env python3
"""
Basic usage example of the OBD-2 Diagnostic Tool
Created by Khanfar Systems
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.obd_reader import OBDDiagnosticTool

def demonstrate_basic_usage():
    """Demonstrate basic usage of the OBD diagnostic tool"""
    tool = OBDDiagnosticTool()
    
    print("Basic OBD-2 Diagnostic Demo")
    print("==========================")
    
    # Connect to the adapter
    print("\n1. Connecting to OBD-II adapter...")
    if not tool.connect():
        print("Failed to connect! Please check your adapter connection.")
        return
    
    print("Successfully connected!")
    
    # Get vehicle information
    print("\n2. Reading vehicle information...")
    info = tool.get_vehicle_info()
    for key, value in info.items():
        print(f"{key}: {value}")
    
    # Check for fault codes
    print("\n3. Checking for fault codes...")
    codes = tool.get_fault_codes()
    if codes:
        print("Found the following fault codes:")
        for code in codes:
            print(f"  - {code}")
        
        # Ask before clearing codes
        response = input("\nWould you like to clear these codes? (y/n): ")
        if response.lower() == 'y':
            if tool.clear_fault_codes():
                print("Fault codes cleared successfully!")
            else:
                print("Failed to clear fault codes.")
    else:
        print("No fault codes found.")
    
    # Monitor some live data
    print("\n4. Monitoring live data (5 seconds)...")
    live_data = tool.monitor_live_data(5)
    
    print("\nAverage readings:")
    for parameter, values in live_data.items():
        if values:
            avg = sum(values) / len(values)
            print(f"{parameter}: {avg:.2f}")
    
    # Clean up
    tool.close()
    print("\nConnection closed. Demo complete!")

if __name__ == "__main__":
    demonstrate_basic_usage()
