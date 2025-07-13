"""HBX SensorLinx integration for Home Assistant."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SensorLinxAPI
from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HBX SensorLinx from a config entry."""
    
    # Create API instance
    api = SensorLinxAPI(
        api_key=entry.data["api_key"],
        base_url=entry.data.get("base_url", "https://api.connect.sensorlinx.co"),
        session=async_get_clientsession(hass)
    )
    
    # Create coordinator
    coordinator = SensorLinxDataUpdateCoordinator(
        hass=hass,
        api=api,
        update_interval=entry.data.get("update_interval", DEFAULT_UPDATE_INTERVAL)
    )
    
    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()
    
    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Setup platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

class SensorLinxDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from SensorLinx API."""
    
    def __init__(self, hass: HomeAssistant, api: SensorLinxAPI, update_interval: int):
        """Initialize coordinator."""
        self.api = api
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=update_interval),
        )
        
    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            # Get all devices
            devices = await self.api.get_devices()
            _LOGGER.debug(f"Received devices from API: {devices}")
            
            # Validate devices response
            if not devices:
                _LOGGER.warning("No devices returned from API")
                return {}
                
            if not isinstance(devices, list):
                _LOGGER.error(f"Expected list of devices, got: {type(devices)}")
                raise UpdateFailed(f"Invalid devices response format: {type(devices)}")
            
            # Get sensor data for each device
            data = {}
            for device in devices:
                _LOGGER.debug(f"Processing device: {device}")
                
                # Check if device has required fields
                if not isinstance(device, dict):
                    _LOGGER.error(f"Expected device dict, got: {type(device)}")
                    continue
                    
                # Try different possible ID field names
                device_id = None
                for id_field in ["syncCode", "id", "device_id", "deviceId", "ID", "Id"]:
                    if id_field in device:
                        device_id = device[id_field]
                        break
                        
                if device_id is None:
                    _LOGGER.error(f"No ID field found in device: {device}")
                    continue
                
                try:
                    device_data = await self.api.get_device_data(device_id)
                    data[device_id] = {
                        "info": device,
                        "sensors": device_data
                    }
                except Exception as device_err:
                    _LOGGER.error(f"Error getting data for device {device_id}: {device_err}")
                    # Continue with other devices even if one fails
                    continue
                
            return data
            
        except Exception as err:
            _LOGGER.error(f"Error in _async_update_data: {err}")
            raise UpdateFailed(f"Error communicating with API: {err}") from err