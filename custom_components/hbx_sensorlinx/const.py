"""Constants for the HBX SensorLinx integration."""

DOMAIN = "hbx_sensorlinx"
MANUFACTURER = "HBX Controls"

DEFAULT_URL = "https://connect.sensorlinx.co"
DEFAULT_SCAN_INTERVAL = 30  # seconds

# Device types
DEVICE_TYPE_THM = "THM"
DEVICE_TYPE_ZON = "ZON"
DEVICE_TYPE_WFS = "WFS"
DEVICE_TYPE_WPS = "WPS"
DEVICE_TYPE_ECO = "ECO"
DEVICE_TYPE_SNO = "SNO"
DEVICE_TYPE_CPU = "CPU"

# Sensor types for different devices
THM_SENSORS = {
    "heatTarget": {
        "name": "Heat Target",
        "unit": "°F",
        "device_class": "temperature",
        "state_class": "measurement",
        "icon": "mdi:thermometer-chevron-up"
    },
    "coolTarget": {
        "name": "Cool Target",
        "unit": "°F", 
        "device_class": "temperature",
        "state_class": "measurement",
        "icon": "mdi:thermometer-chevron-down"
    },
    "room": {
        "name": "Room Temperature",
        "unit": "°F",
        "device_class": "temperature",
        "state_class": "measurement",
        "icon": "mdi:thermometer"
    },
    "floor": {
        "name": "Floor Temperature",
        "unit": "°F",
        "device_class": "temperature",
        "state_class": "measurement",
        "icon": "mdi:thermometer-water"
    },
    "humidity": {
        "name": "Humidity",
        "unit": "%",
        "device_class": "humidity",
        "state_class": "measurement",
        "icon": "mdi:water-percent"
    },
    "demand1": {
        "name": "Demand 1",
        "unit": "",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:gauge"
    },
    "demand2": {
        "name": "Demand 2",
        "unit": "",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:gauge"
    },
    "zone": {
        "name": "Zone",
        "unit": "",
        "device_class": None,
        "state_class": None,
        "icon": "mdi:home-group"
    },
    "priority": {
        "name": "Priority",
        "unit": "",
        "device_class": None,
        "state_class": None,
        "icon": "mdi:priority-high"
    },
    "humidityOn": {
        "name": "Humidity On",
        "unit": "",
        "device_class": None,
        "state_class": None,
        "icon": "mdi:water"
    }
}

# Add other device sensor definitions as needed
ZON_SENSORS = {
    # Add ZON sensor definitions when available
}

WFS_SENSORS = {
    # Add WFS sensor definitions when available
}

WPS_SENSORS = {
    # Add WPS sensor definitions when available
}

DEVICE_SENSORS = {
    DEVICE_TYPE_THM: THM_SENSORS,
    DEVICE_TYPE_ZON: ZON_SENSORS,
    DEVICE_TYPE_WFS: WFS_SENSORS,
    DEVICE_TYPE_WPS: WPS_SENSORS,
}
