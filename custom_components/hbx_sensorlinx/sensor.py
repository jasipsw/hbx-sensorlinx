"""Sensor platform for HBX SensorLinx integration."""
import logging
from typing import Optional, Dict, Any
from datetime import timedelta

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.const import (
    CONF_API_KEY,
    CONF_URL,
    CONF_SCAN_INTERVAL,
    UnitOfTemperature,
    PERCENTAGE,
)

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, MANUFACTURER
from .api import SensorLinxAPI, SensorLinxDevice

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = []
    
    # Create sensors for each device
    for device_id, device_data in coordinator.data.items():
        device = SensorLinxDevice(device_data)
        sensor_definitions = device.get_sensor_definitions()
        
        for sensor_key, sensor_config in sensor_definitions.items():
            entities.append(
                SensorLinxSensor(
                    coordinator=coordinator,
                    device=device,
                    sensor_key=sensor_key,
                    sensor_config=sensor_config,
                )
            )
    
    async_add_entities(entities)


class SensorLinxSensor(CoordinatorEntity, SensorEntity):
    """Representation of a SensorLinx sensor."""
    
    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        device: SensorLinxDevice,
        sensor_key: str,
        sensor_config: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        
        self._device = device
        self._sensor_key = sensor_key
        self._sensor_config = sensor_config
        
        # Generate unique ID
        self._attr_unique_id = f"{device.id}_{sensor_key}"
        
        # Set entity attributes
        self._attr_name = f"{device.display_name} {sensor_config['name']}"
        self._attr_native_unit_of_measurement = sensor_config.get("unit")
        self._attr_device_class = sensor_config.get("device_class")
        self._attr_state_class = sensor_config.get("state_class")
        self._attr_icon = sensor_config.get("icon")
        
        # Device info for grouping sensors under devices
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device.id)},
            name=device.display_name,
            manufacturer=MANUFACTURER,
            model=device.device_type,
            sw_version=str(device.firmware_version),
            configuration_url=f"https://connect.sensorlinx.co/devices/{device.id}",
        )
        
    @property
    def native_value(self) -> Optional[float]:
        """Return the state of the sensor."""
        if self.coordinator.data and self._device.id in self.coordinator.data:
            device_data = self.coordinator.data[self._device.id]
            value = device_data.get(self._sensor_key)
            
            if value is not None:
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return value
        return None
        
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            self.coordinator.last_update_success
            and self.coordinator.data
            and self._device.id in self.coordinator.data
            and self.coordinator.data[self._device.id].get("connected", False)
        )
        
    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return additional state attributes."""
        if self.coordinator.data and self._device.id in self.coordinator.data:
            device_data = self.coordinator.data[self._device.id]
            return {
                "device_type": device_data.get("deviceType"),
                "firmware_version": device_data.get("firmVer"),
                "connected_at": device_data.get("connectedAt"),
                "zone": device_data.get("zone"),
                "priority": device_data.get("priority"),
            }
        return {}


class SensorLinxDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""
    
    def __init__(
        self,
        hass: HomeAssistant,
        api: SensorLinxAPI,
        update_interval: timedelta,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self.api = api
        
    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from API endpoint."""
        try:
            return await self.api.get_all_device_data()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
