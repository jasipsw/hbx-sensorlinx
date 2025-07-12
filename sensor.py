"""Sensor platform for HBX SensorLinx integration."""
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import UnitOfTemperature, PERCENTAGE

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SensorLinx sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    
    # Create sensors for each device
    for device_id, device_data in coordinator.data.items():
        device_info = device_data["info"]
        sensors_data = device_data["sensors"]
        
        # Create temperature sensor
        if "temperature" in sensors_data or "temp" in sensors_data:
            entities.append(
                SensorLinxTemperatureSensor(
                    coordinator=coordinator,
                    device_id=device_id,
                    device_info=device_info,
                )
            )
        
        # Create humidity sensor
        if "humidity" in sensors_data or "hum" in sensors_data:
            entities.append(
                SensorLinxHumiditySensor(
                    coordinator=coordinator,
                    device_id=device_id,
                    device_info=device_info,
                )
            )
        
        # Create battery sensor if available
        if "battery" in sensors_data or "bat" in sensors_data:
            entities.append(
                SensorLinxBatterySensor(
                    coordinator=coordinator,
                    device_id=device_id,
                    device_info=device_info,
                )
            )
    
    async_add_entities(entities)

class SensorLinxSensorBase(CoordinatorEntity, SensorEntity):
    """Base class for SensorLinx sensors."""
    
    def __init__(self, coordinator, device_id: str, device_info: dict):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._device_info = device_info
        self._attr_has_entity_name = True
        
    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": f"SensorLinx {self._device_id}",
            "manufacturer": "HBX",
            "model": self._device_info.get("deviceType", "Unknown"),
            "sw_version": self._device_info.get("firmVer"),
        }
    
    @property
    def unique_id(self):
        """Return unique ID."""
        return f"{DOMAIN}_{self._device_id}_{self._sensor_type}"
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            self.coordinator.last_update_success
            and self._device_id in self.coordinator.data
        )

class SensorLinxTemperatureSensor(SensorLinxSensorBase):
    """Temperature sensor for SensorLinx."""
    
    _sensor_type = "temperature"
    
    def __init__(self, coordinator, device_id: str, device_info: dict):
        """Initialize the temperature sensor."""
        super().__init__(coordinator, device_id, device_info)
        self._attr_name = "Temperature"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_state_class = "measurement"
    
    @property
    def native_value(self) -> float | None:
        """Return the temperature value."""
        if self._device_id not in self.coordinator.data:
            return None
            
        sensors_data = self.coordinator.data[self._device_id]["sensors"]
        
        # Try different possible temperature field names
        for temp_field in ["temperature", "temp", "Temperature", "Temp"]:
            if temp_field in sensors_data:
                try:
                    return float(sensors_data[temp_field])
                except (ValueError, TypeError):
                    _LOGGER.warning(f"Invalid temperature value: {sensors_data[temp_field]}")
                    return None
        
        return None

class SensorLinxHumiditySensor(SensorLinxSensorBase):
    """Humidity sensor for SensorLinx."""
    
    _sensor_type = "humidity"
    
    def __init__(self, coordinator, device_id: str, device_info: dict):
        """Initialize the humidity sensor."""
        super().__init__(coordinator, device_id, device_info)
        self._attr_name = "Humidity"
        self._attr_device_class = SensorDeviceClass.HUMIDITY
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_state_class = "measurement"
    
    @property
    def native_value(self) -> float | None:
        """Return the humidity value."""
        if self._device_id not in self.coordinator.data:
            return None
            
        sensors_data = self.coordinator.data[self._device_id]["sensors"]
        
        # Try different possible humidity field names
        for hum_field in ["humidity", "hum", "Humidity", "Hum"]:
            if hum_field in sensors_data:
                try:
                    return float(sensors_data[hum_field])
                except (ValueError, TypeError):
                    _LOGGER.warning(f"Invalid humidity value: {sensors_data[hum_field]}")
                    return None
        
        return None

class SensorLinxBatterySensor(SensorLinxSensorBase):
    """Battery sensor for SensorLinx."""
    
    _sensor_type = "battery"
    
    def __init__(self, coordinator, device_id: str, device_info: dict):
        """Initialize the battery sensor."""
        super().__init__(coordinator, device_id, device_info)
        self._attr_name = "Battery"
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_state_class = "measurement"
    
    @property
    def native_value(self) -> float | None:
        """Return the battery value."""
        if self._device_id not in self.coordinator.data:
            return None
            
        sensors_data = self.coordinator.data[self._device_id]["sensors"]
        
        # Try different possible battery field names
        for bat_field in ["battery", "bat", "Battery", "Bat", "batteryLevel"]:
            if bat_field in sensors_data:
                try:
                    return float(sensors_data[bat_field])
                except (ValueError, TypeError):
                    _LOGGER.warning(f"Invalid battery value: {sensors_data[bat_field]}")
                    return None
        
        return None