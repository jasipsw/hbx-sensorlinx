"""Constants for HBX SensorLinx integration."""

DOMAIN = "hbx_sensorlinx"
NAME = "HBX SensorLinx"
MANUFACTURER = "HBX Controls"

# Configuration
CONF_API_KEY = "api_key"
CONF_BASE_URL = "base_url"
CONF_UPDATE_INTERVAL = "update_interval"

# Defaults
DEFAULT_BASE_URL = "https://connect.sensorlinx.co"
DEFAULT_UPDATE_INTERVAL = 30
DEFAULT_TIMEOUT = 10

# Device types
DEVICE_TYPES = {
    "wfs": "Wi-Fi Flow & Temperature Sensor",
    "wps": "Wi-Fi Pressure & Temperature Sensor", 
    "zon-600": "Zoning Controller",
    "thm-0600": "Boiler Controller",
    "eco-0600": "Geothermal Controller",
    "sno-0600": "Snow Melt Controller",
    "cpu-0600": "CPU Controller"
}

# Sensor types and their device classes
SENSOR_TYPES = {
    "temperature": {
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement"
    },
    "pressure": {
        "device_class": "pressure", 
        "unit": "kPa",
        "state_class": "measurement"
    },
    "flow_rate": {
        "device_class": "volume_flow_rate",
        "unit": "L/min",
        "state_class": "measurement"
    },
    "energy": {
        "device_class": "energy",
        "unit": "kWh", 
        "state_class": "total_increasing"
    },
    "power": {
        "device_class": "power",
        "unit": "W",
        "state_class": "measurement"
    },
    "humidity": {
        "device_class": "humidity",
        "unit": "%",
        "state_class": "measurement"
    },
    "voltage": {
        "device_class": "voltage",
        "unit": "V",
        "state_class": "measurement"
    },
    "current": {
        "device_class": "current",
        "unit": "A", 
        "state_class": "measurement"
    }
}