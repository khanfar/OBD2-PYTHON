# OBD-2 Python Diagnostic Tool

[![GitHub](https://img.shields.io/github/license/khanfar/OBD2-PYTHON)](https://github.com/khanfar/OBD2-PYTHON)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

![Screenshot 2025-01-17 201953](https://github.com/user-attachments/assets/6ccf3e7b-6c58-47bf-a3fe-b4bd93064858)

A Python-based OBD-2 (On-Board Diagnostics II) car diagnostic tool for reading fault codes and monitoring vehicle data. This educational project demonstrates how to interface with your car's OBD-2 system using Python.

## 📑 Table of Contents
- [Features](#-features)
- [Hardware Requirements](#-hardware-requirements)
- [Software Requirements](#-software-requirements)
- [Installation](#️-installation)
- [Project Structure](#-project-structure)
- [Usage](#-usage)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)
- [Developer](#-developer)
- [Disclaimer](#️-disclaimer)

## 🚗 Features

- Read diagnostic trouble codes (DTCs)
- Monitor real-time vehicle data
- Support for ELM327-based OBD2 adapters
- Compatible with various OBD2 protocols (CAN, ISO 9141-2, KWP2000)

## 📋 Hardware Requirements

For detailed information about hardware requirements and recommended tools, see our comprehensive guides:
- [Recommended Tools and Adapters Guide](docs/recommended_tools.md)
- [Hardware Requirements Guide](docs/hardware_requirements.md)

Quick hardware selection guide:
1. **For Basic Reading**: ELM327-based adapter (e.g., OBDLink SX)
2. **For Advanced Features**: STN1110/STN2120-based adapter (e.g., OBDLink MX+)
3. **For Full Access**: J2534 Pass-Thru device (e.g., MongoosePro)

## 💻 Software Requirements
- Python 3.6 or higher
- python-OBD library
- Additional dependencies listed in `requirements.txt`

## 🛠️ Installation

1. Clone this repository:
```bash
git clone https://github.com/khanfar/OBD2-PYTHON.git
cd OBD2-PYTHON
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
OBD2-PYTHON/
├── src/               # Source code files
│   └── obd_reader.py  # Main diagnostic tool implementation
├── docs/              # Documentation
│   ├── hardware_requirements.md  # Detailed hardware guide
│   └── recommended_tools.md      # Tools and adapters guide
├── examples/          # Example scripts and usage
│   └── basic_usage.py # Basic usage examples
├── requirements.txt   # Project dependencies
├── LICENSE           # MIT License
└── README.md         # Project documentation
```

## 🚀 Usage

Basic example of reading fault codes:

```python
import obd

# Connect to the OBD2 adapter
connection = obd.OBD()

if connection.is_connected():
    # Query for Diagnostic Trouble Codes (DTCs)
    response = connection.query(obd.commands.GET_DTC)
    print("Fault Codes:", response.value)
```

For more examples, check the [`examples/`](examples/) directory.

## 📚 Documentation

- [Hardware Requirements](docs/hardware_requirements.md) - Detailed guide about required hardware
- [Recommended Tools](docs/recommended_tools.md) - Comprehensive guide about OBD2 adapters and tools
- [Vehicle Compatibility](docs/vehicle_compatibility.md) - Supported vehicles and protocols
- [Troubleshooting Guide](docs/troubleshooting.md) - Common issues and solutions
- [Example Scripts](examples/basic_usage.py) - Example usage of the diagnostic tool

## 🔧 Advanced Features

### Real-time Monitoring
```python
# Monitor multiple parameters in real-time
connection = obd.OBD()
while True:
    rpm = connection.query(obd.commands.RPM)
    speed = connection.query(obd.commands.SPEED)
    temp = connection.query(obd.commands.COOLANT_TEMP)
    print(f"RPM: {rpm.value}, Speed: {speed.value}, Temp: {temp.value}")
```

### Custom Commands
```python
# Define and use custom OBD commands
from obd import OBDCommand, Unit
from obd.protocols import ECU
from obd.utils import bytes_to_int

custom_cmd = OBDCommand("CUSTOM_SENSOR",
                       "Description",
                       b"01 1D",
                       2,
                       bytes_to_int,
                       ECU.ENGINE,
                       True)
```

### Error Handling
```python
try:
    connection = obd.OBD()
    if not connection.is_connected():
        raise Exception("Failed to connect")
    
    # Your diagnostic code here
    
except Exception as e:
    print(f"Error: {e}")
finally:
    if connection:
        connection.close()
```

## 🌟 Features in Detail

### 1. Basic Operations
- Read and clear diagnostic trouble codes (DTCs)
- Access real-time sensor data
- Monitor vehicle performance metrics
- Support for multiple OBD-II protocols

### 2. Advanced Tools

#### Data Logger (`src/data_logger.py`)
- Log OBD data to CSV and JSON formats
- Continuous data monitoring
- Statistical analysis of logged data
- Flexible data export options

#### Real-time Dashboard (`src/dashboard.py`)
- GUI-based live data monitoring
- Configurable display parameters
- Real-time updates of vehicle sensors
- User-friendly interface

#### Report Generator (`src/report_generator.py`)
- Generate detailed HTML reports
- Visual graphs and charts
- DTC code interpretation
- Comprehensive vehicle diagnostics

### 3. Safety Features
- Connection validation
- Error handling
- Data validation
- Safe disconnection

## 📊 Example Usage

### Basic Fault Code Reading
```python
import obd

connection = obd.OBD()
if connection.is_connected():
    codes = connection.query(obd.commands.GET_DTC)
    print("Fault Codes:", codes.value)
```

### Data Logging
```python
from src.data_logger import OBDDataLogger

logger = OBDDataLogger()
if logger.connect():
    # Log 60 seconds of data to CSV
    log_file = logger.log_to_csv([
        obd.commands.RPM,
        obd.commands.SPEED,
        obd.commands.THROTTLE_POS
    ], duration=60)
```

### Real-time Dashboard
```python
from src.dashboard import main as dashboard_main

# Launch the GUI dashboard
dashboard_main()
```

### Generate Report
```python
from src.report_generator import DiagnosticReportGenerator

generator = DiagnosticReportGenerator()
if generator.connect():
    report_file = generator.generate_report()
    print(f"Report generated: {report_file}")
```

## 🔄 Update and Maintenance

To keep your OBD2 diagnostic tool up to date:

1. Update Python packages:
```bash
pip install --upgrade -r requirements.txt
```

2. Check for firmware updates for your OBD2 adapter

3. Verify vehicle compatibility regularly

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

Created and maintained by [Khanfar Systems](https://github.com/khanfar).

## ⚠️ Disclaimer

This tool is for educational purposes only. Always consult professional diagnostic tools and qualified mechanics for critical vehicle issues.
