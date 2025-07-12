# HBX SensorLinx Custom Integration for Home Assistant

This custom integration allows you to connect your HBX Controls SensorLinx devices to Home Assistant, providing real-time monitoring of HVAC, solar thermal, and geothermal systems.

## Installation

### Method 1: Manual Installation

1. Create a `custom_components` directory in your Home Assistant configuration directory if it doesn't exist.

2. Create the following directory structure:
   ```
   custom_components/
   └── hbx_sensorlinx/
       ├── __init__.py
       ├── manifest.json
       ├── config_flow.py
       ├── sensor.py
       ├── api.py
       ├── const.py
       └── strings.json
   ```

3. Copy all the provided files into the `hbx_sensorlinx` directory.

4. Restart Home Assistant.

### Method 2: Using HACS (Recommended)

1. Add this repository to HACS as a custom repository.
2. Install the integration through HACS.
3. Restart Home Assistant.

## Configuration

1. Go to **Settings** → **Devices & Services** → **Add Integration**.
2. Search for "HBX SensorLinx" and select it.
3. Enter your configuration:
   - **API Key**: Your SensorLinx API key (FZ2KW6:7a295842-eb04-46b4-b9b5-fa69d5a18548)
   - **Base URL**: Usually `https://api.connect.sensorlinx.co` (default)
   - **Update Interval**: How often to poll for data (30 seconds default)

## Supported Devices

- **WFS**: Wi-Fi Flow & Temperature Sensor
- **WPS**: Wi-Fi Pressure & Temperature Sensor
- **ZON-600**: Zoning Controller
- **THM-0600**: Boiler Controller
- **ECO-0600**: Geothermal Controller
- **SNO-0600**: Snow Melt Controller
- **CPU-0600**: CPU Controller

## Supported Sensor Types

- **Temperature**: Ambient, supply, return temperatures
- **Pressure**: System pressures
- **Flow Rate**: Water/fluid flow rates
- **Energy**: Energy consumption
- **Power**: Power consumption
- **Humidity**: Relative humidity
- **Voltage**: System voltages
- **Current**: Electrical current

## Features

- **Real-time Monitoring**: Automatically polls your SensorLinx devices
- **Device Auto-Discovery**: Automatically discovers all connected devices
- **Proper Device Classes**: Sensors are properly classified for Home Assistant
- **Error Handling**: Robust error handling and logging
- **Configurable Update Intervals**: Adjust polling frequency as needed

## API Endpoints Used

Based on the SensorLinx Connect API, this integration uses:

- `GET /devices` - Get list of all devices
- `GET /devices/{device_id}/data` - Get current sensor data
- `GET /devices/{device_id}/history` - Get historical data
- `POST /devices/{device_id}/control` - Control device parameters
- `GET /system/status` - Get system status

## Troubleshooting

1. **Connection Issues**: Verify your API key and network connectivity
2. **No Devices Found**: Check that your devices are properly connected to SensorLinx
3. **Sensor Data Not Updating**: Check the update interval and device status
4. **API Rate Limits**: Increase update intervals if hitting rate limits

## Logs

Enable debug logging by adding this to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.hbx_sensorlinx: debug
```

## Support

For issues and support:
- Check the Home Assistant logs for error messages
- Verify your API key is valid and has proper permissions
- Ensure your SensorLinx devices are online and connected

## License

This integration is provided as-is for educational and personal use.