# Vehicle Compatibility Guide

## Supported Protocols

### 1. CAN Protocols (ISO 15765-4)
- **11-bit CAN (ISO 15765-4)**
  - Most vehicles after 2008
  - High-speed communication
  - Reliable data transfer

- **29-bit CAN (ISO 15765-4)**
  - Extended addressing
  - Used in some modern vehicles
  - Enhanced functionality

### 2. Legacy Protocols
- **ISO 9141-2**
  - European and Asian vehicles
  - 1996-2008 typically
  - Slower communication speed

- **ISO 14230-4 (KWP2000)**
  - Some European and Asian vehicles
  - Variable speed protocol
  - Good compatibility

- **SAE J1850 PWM**
  - Ford vehicles (mainly)
  - 41.6k baudrate
  - Older protocol

- **SAE J1850 VPW**
  - GM vehicles (mainly)
  - Variable pulse width
  - Legacy support

## Vehicle Compatibility

### US Vehicles
- **Required by Law**: All vehicles from 1996 onwards
- **Protocol Support**: Varies by manufacturer and year
- **Common Brands**:
  - Ford (1996+)
  - GM (1996+)
  - Chrysler (1996+)
  - Toyota USA (1996+)
  - Honda USA (1996+)

### European Vehicles
- **Required by Law**: All vehicles from 2001 onwards
- **EOBD Compliance**: 2004+ gasoline, 2005+ diesel
- **Common Brands**:
  - BMW (2000+)
  - Mercedes (2000+)
  - Volkswagen Group (2001+)
  - Volvo (2001+)
  - Peugeot/Citroën (2001+)

### Asian Vehicles
- **Japanese Brands**:
  - Toyota (2000+)
  - Honda (2000+)
  - Nissan (2000+)
  - Mazda (2000+)
  - Subaru (2000+)

- **Korean Brands**:
  - Hyundai (2001+)
  - Kia (2001+)

## Protocol Detection

### Automatic Protocol Detection
```python
import obd

connection = obd.OBD()
print(f"Active Protocol: {connection.protocol_name()}")
```

### Manual Protocol Selection
```python
# Force specific protocol
connection = obd.OBD(protocol="3") # ISO 9141-2
```

## Protocol Numbers Reference

1. **Auto** (Default)
2. **SAE J1850 PWM** (41.6k baudrate)
3. **SAE J1850 VPW** (10.4k baudrate)
4. **ISO 9141-2** (5 baud init)
5. **ISO 14230-4 KWP** (5 baud init)
6. **ISO 14230-4 KWP** (fast init)
7. **ISO 15765-4 CAN** (11 bit ID, 500k baudrate)
8. **ISO 15765-4 CAN** (29 bit ID, 500k baudrate)
9. **ISO 15765-4 CAN** (11 bit ID, 250k baudrate)
10. **ISO 15765-4 CAN** (29 bit ID, 250k baudrate)

## Common Vehicle-Specific Notes

### 1. BMW
- Supports extended PIDs
- Good CAN protocol support
- Some models require specific initialization

### 2. Toyota/Lexus
- Reliable standard PID support
- Some models use non-standard PIDs
- Good compatibility with ELM327

### 3. Ford
- Strong J1850 PWM support
- Later models use CAN
- Good diagnostic coverage

### 4. GM
- J1850 VPW in older models
- CAN in newer models
- Extended PID support

### 5. VAG (Volkswagen, Audi)
- KWP2000 in older models
- CAN in newer models
- Some models require specific tools

## Troubleshooting Protocol Issues

### 1. Connection Problems
- Try forcing specific protocol
- Check voltage levels
- Verify physical connection

### 2. Data Reading Issues
- Verify protocol support
- Check command compatibility
- Monitor timing issues

### 3. Protocol-Specific Solutions
```python
# Example: Force protocol with timeout
connection = obd.OBD(protocol="6", timeout=30)
```

## Advanced Protocol Features

### 1. Multi-Protocol Support
Some vehicles support multiple protocols:
```python
# Check supported protocols
protocols = connection.supported_protocols
print(f"Supported Protocols: {protocols}")
```

### 2. Protocol Switching
```python
# Switch protocols during operation
connection.change_protocol("7")
```

### 3. Custom Protocol Settings
```python
# Custom baudrate and protocol
connection = obd.OBD(baudrate=38400, protocol="3")
```

## Manufacturer-Specific Commands

### 1. Toyota Example
```python
# Toyota-specific DTC command
response = connection.query(obd.commands.GET_DTC)
```

### 2. BMW Example
```python
# BMW-specific sensor data
response = connection.query(obd.commands.CONTROL_MODULE_VOLTAGE)
```

## Future Protocol Support

### 1. Upcoming Standards
- **ISO 15765-4:2021**
- **DoIP** (ISO 13400)
- **Ethernet** based diagnostics

### 2. Legacy Support
- Continued support for older protocols
- Backward compatibility
- Adapter firmware updates
