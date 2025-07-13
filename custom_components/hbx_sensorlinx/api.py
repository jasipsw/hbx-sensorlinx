"""API client for HBX SensorLinx integration."""
import logging
import aiohttp
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime

_LOGGER = logging.getLogger(__name__)

class SensorLinxAPI:
    """API client for SensorLinx devices."""
    
    def __init__(self, api_key: str, base_url: str = "https://connect.sensorlinx.co"):
        """Initialize the API client."""
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = None
        
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={
                    "X-API-KEY": self.api_key,
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
            )
        return self.session
        
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Make HTTP request to the API."""
        session = await self._get_session()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            async with session.request(method, url, **kwargs) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    _LOGGER.error(f"Endpoint not found: {url}")
                    return None
                else:
                    _LOGGER.error(f"API request failed: {response.status} - {await response.text()}")
                    return None
                    
        except aiohttp.ClientError as e:
            _LOGGER.error(f"HTTP client error: {e}")
            return None
        except Exception as e:
            _LOGGER.error(f"Unexpected error: {e}")
            return None
            
    async def get_available_devices(self, limit: int = 25, page: int = 1) -> Optional[Dict[str, Any]]:
        """Get list of available devices."""
        params = {"limit": limit, "page": page}
        return await self._make_request("GET", "/v1/devices/available", params=params)
        
    async def get_device_data(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Get device data - FIXED: removed /data from endpoint."""
        return await self._make_request("GET", f"/v1/devices/{device_id}")
        
    async def get_device_history(self, device_id: str, start_date: str = None, end_date: str = None) -> Optional[Dict[str, Any]]:
        """Get device history data."""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
            
        return await self._make_request("GET", f"/v1/devices/{device_id}/history", params=params)
        
    async def get_system_status(self) -> Optional[Dict[str, Any]]:
        """Get system status."""
        return await self._make_request("GET", "/v1/system/status")
        
    async def control_device(self, device_id: str, control_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Control device parameters."""
        return await self._make_request("POST", f"/v1/devices/{device_id}/control", json=control_data)
        
    async def get_all_device_data(self) -> Dict[str, Any]:
        """Get data for all available devices."""
        devices_response = await self.get_available_devices()
        if not devices_response or "items" not in devices_response:
            _LOGGER.error("Failed to get available devices")
            return {}
            
        device_data = {}
        tasks = []
        
        for device in devices_response["items"]:
            device_id = device["syncCode"]
            tasks.append(self._get_single_device_data(device_id))
            
        # Execute all requests concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            device_id = devices_response["items"][i]["syncCode"]
            if isinstance(result, Exception):
                _LOGGER.error(f"Failed to get device data for {device_id}: {result}")
            elif result:
                device_data[device_id] = result
                
        return device_data
        
    async def _get_single_device_data(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Get data for a single device with error handling."""
        try:
            return await self.get_device_data(device_id)
        except Exception as e:
            _LOGGER.error(f"Failed to get device data for {device_id}: {e}")
            return None
            
    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()
            
    async def __aenter__(self):
        """Async context manager entry."""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()


class SensorLinxDevice:
    """Represents a SensorLinx device."""
    
    def __init__(self, device_data: Dict[str, Any]):
        """Initialize device from API data."""
        self.sync_code = device_data.get("syncCode")
        self.name = device_data.get("name", self.sync_code)
        self.device_type = device_data.get("deviceType")
        self.firmware_version = device_data.get("firmVer")
        self.connected_at = device_data.get("connectedAt")
        self.connected = device_data.get("connected", False)
        self._data = device_data
        
    @property
    def id(self) -> str:
        """Return device ID."""
        return self.sync_code
        
    @property
    def display_name(self) -> str:
        """Return device display name."""
        return self.name or f"{self.device_type}-{self.sync_code}"
        
    @property
    def is_online(self) -> bool:
        """Check if device is online."""
        return self.connected
        
    def update_data(self, new_data: Dict[str, Any]):
        """Update device data."""
        self._data.update(new_data)
        self.connected = new_data.get("connected", False)
        
    def get_sensor_value(self, sensor_key: str) -> Any:
        """Get sensor value by key."""
        return self._data.get(sensor_key)
        
    def get_all_sensors(self) -> Dict[str, Any]:
        """Get all sensor data."""
        # Filter out metadata and return only sensor readings
        metadata_keys = {"syncCode", "name", "deviceType", "firmVer", "connectedAt", "connected"}
        return {k: v for k, v in self._data.items() if k not in metadata_keys}
        
    def get_sensor_definitions(self) -> Dict[str, Dict[str, Any]]:
        """Get sensor definitions for this device type."""
        sensors = {}
        
        if self.device_type == "THM":
            # Temperature and humidity sensors for THM devices
            sensor_configs = {
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
            
            # Only add sensors that have values in the device data
            for sensor_key, config in sensor_configs.items():
                if sensor_key in self._data:
                    sensors[sensor_key] = config
                    
        elif self.device_type == "ZON":
            # Add ZON device sensors when we have examples
            pass
            
        return sensors
        
    def __repr__(self) -> str:
        """Return string representation."""
        return f"SensorLinxDevice(id={self.id}, name={self.display_name}, type={self.device_type}, online={self.is_online})"
