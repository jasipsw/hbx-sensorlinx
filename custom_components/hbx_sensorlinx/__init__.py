"""The HBX SensorLinx integration."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_URL, CONF_SCAN_INTERVAL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .api import SensorLinxAPI
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, DEFAULT_URL
from .sensor import SensorLinxDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HBX SensorLinx from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    api_key = entry.data[CONF_API_KEY]
    base_url = entry.data.get(CONF_URL, DEFAULT_URL)
    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    
    api = SensorLinxAPI(api_key, base_url)
    
    # Test the API connection
    try:
        devices = await api.get_available_devices()
        if not devices:
            raise ConfigEntryNotReady("Unable to connect to SensorLinx API")
    except Exception as err:
        _LOGGER.error("Error connecting to SensorLinx API: %s", err)
        raise ConfigEntryNotReady(f"Error connecting to SensorLinx API: {err}")
    
    # Create data update coordinator
    coordinator = SensorLinxDataUpdateCoordinator(
        hass,
        api,
        timedelta(seconds=scan_interval),
    )
    
    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()
    
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Setup platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        coordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.api.close()
    
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
