# Hardware Requirements for OBD-2 Python Diagnostic Tool

## Required Hardware

### 1. OBD2 Adapter
The most critical component needed is an OBD2 adapter. Here are the recommended options:

#### ELM327-based Adapters
- USB ELM327 adapter
- Bluetooth ELM327 adapter
- WiFi ELM327 adapter

Recommended features:
- Supports multiple protocols (CAN, ISO 9141-2, KWP2000)
- Firmware version 1.5 or higher
- Genuine chip (avoid counterfeit products)

#### Alternative: STN1110-based Adapters
- More reliable than ELM327
- Better performance and protocol support
- Higher cost but better quality

### 2. Computer Requirements
- Any computer capable of running Python 3.6 or higher
- Available USB port (for USB adapters)
- Bluetooth capability (for Bluetooth adapters)
- WiFi capability (for WiFi adapters)

### 3. Vehicle Requirements
- OBD2 port (standard in most vehicles)
  - US vehicles: 1996 or newer
  - EU vehicles: 2001 or newer
- Compatible OBD2 protocol
  - Most modern vehicles use CAN protocol
  - Older vehicles might use ISO 9141-2 or KWP2000

## Where to Buy

### Recommended Vendors
1. ScanTool.net
   - High-quality adapters
   - Good technical support
   - Genuine products

2. OBD Solutions
   - Wide range of adapters
   - Professional-grade options
   - Reliable customer service

3. Amazon/eBay (Caution)
   - Look for sellers with good ratings
   - Check for genuine products
   - Read reviews carefully

## Setup Tips

1. Physical Connection
   - Locate your vehicle's OBD2 port (usually under dashboard)
   - Ensure firm connection between adapter and port
   - Check for any bent pins

2. Software Setup
   - Install required drivers (if using USB)
   - Pair device (if using Bluetooth)
   - Configure network settings (if using WiFi)

3. Testing Connection
   - Use simple commands first
   - Verify communication before complex operations
   - Check error messages if connection fails

## Troubleshooting

Common issues and solutions:
1. No Connection
   - Check physical connection
   - Verify adapter power (LED indicators)
   - Confirm correct COM port (USB) or pairing (Bluetooth)

2. Data Errors
   - Try different baud rates
   - Check for interference (Bluetooth/WiFi)
   - Verify protocol compatibility

3. Poor Performance
   - Use shorter cable lengths
   - Reduce interference sources
   - Consider upgrading adapter quality

## Safety Notes

- Always connect/disconnect with ignition off
- Don't leave adapter plugged in when not in use
- Be careful when clearing codes
- Consult professional help for serious issues
