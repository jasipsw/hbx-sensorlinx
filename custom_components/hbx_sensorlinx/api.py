"""SensorLinx API client."""
import asyncio
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

import aiohttp
import async_timeout

from .const import DEFAULT_TIMEOUT

_LOGGER = logging.getLogger(__name__)

class SensorLinxAPI:
    """API client for SensorLinx Connect."""
    
    def __init__(self, api_key: str, base_url: str, session: aiohttp.ClientSession):
        """Initialize the API client."""
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self._session = session
        self._headers = {
            'X-API-KEY': api_key,  # Use X-API-KEY header instead of Authorization
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            async with async_timeout.timeout(DEFAULT_TIMEOUT):
                async with self._session.request(
                    method, url, headers=self._headers, **kwargs
                ) as response:
                    # Log response details for debugging
                    _LOGGER.debug("Request %s %s - Status: %s", method, url, response.status)
                    
                    if response.status == 401:
                        raise ConnectionError(f"Authentication failed - check API key")
                    elif response.status == 404:
                        raise ConnectionError(f"Endpoint not found: {url}")
                    
                    response.raise_for_status()
                    return await response.json()
        except asyncio.TimeoutError as err:
            raise TimeoutError(f"Timeout error fetching {url}") from err
        except aiohttp.ClientError as err:
            raise ConnectionError(f"Connection error fetching {url}: {response.status}, message='{err}', url='{url}'") from err
            
    async def test_connection(self) -> bool:
        """Test API connection."""
        try:
            await self._request('GET', '/v1/devices/available')
            return True
        except Exception as err:
            _LOGGER.error("Connection test failed: %s", err)
            return False
            
    async def get_devices(self) -> List[Dict[str, Any]]:
        """Get list of all devices."""
        try:
            response = await self._request('GET', '/v1/devices/available')
            devices = response.get('items', [])
            _LOGGER.info("Successfully got %d devices", len(devices))
            return devices
        except Exception as err:
            _LOGGER.error("Failed to get devices: %s", err)
            return []
            
    async def get_device_data(self, device_id: str) -> List[Dict[str, Any]]:
        """Get current sensor data for a device."""
        try:
            # Use syncCode as the device identifier
            response = await self._request('GET', f'/v1/devices/{device_id}/data')
            return response.get('sensors', response.get('data', []))
        except Exception as err:
            _LOGGER.error("Failed to get device data for %s: %s", device_id, err)
            return []
            
    async def get_device_details(self, sync_code: str) -> Dict[str, Any]:
        """Get detailed information for a specific device."""
        try:
            response = await self._request('GET', f'/v1/devices/{sync_code}')
            return response
        except Exception as err:
            _LOGGER.error("Failed to get device details for %s: %s", sync_code, err)
            return {}
            
    async def get_historical_data(
        self, 
        device_id: str, 
        sensor_type: str, 
        start_time: datetime, 
        end_time: datetime
    ) -> List[Dict[str, Any]]:
        """Get historical sensor data."""
        try:
            params = {
                'sensor_type': sensor_type,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat()
            }
            response = await self._request('GET', f'/v1/devices/{device_id}/history', params=params)
            return response.get('data', [])
        except Exception as err:
            _LOGGER.error("Failed to get historical data for %s: %s", device_id, err)
            return []
            
    async def set_device_parameter(self, device_id: str, parameter: str, value: Any) -> bool:
        """Set device parameter/control."""
        try:
            payload = {
                'parameter': parameter,
                'value': value
            }
            await self._request('POST', f'/v1/devices/{device_id}/control', json=payload)
            return True
        except Exception as err:
            _LOGGER.error("Failed to set parameter %s on %s: %s", parameter, device_id, err)
            return False
            
    async def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        try:
            return await self._request('GET', '/v1/system/status')
        except Exception as err:
            _LOGGER.error("Failed to get system status: %s", err)
            return {}
            
    async def get_device_current_data(self, sync_code: str) -> Dict[str, Any]:
        """Get current sensor readings for a device."""
        try:
            response = await self._request('GET', f'/v1/devices/{sync_code}/current')
            return response
        except Exception as err:
            _LOGGER.error("Failed to get current data for %s: %s", sync_code, err)
            return {}
            
    async def get_all_devices_paginated(self, page: int = 1, limit: int = 25) -> Dict[str, Any]:
        """Get devices with pagination."""
        try:
            params = {
                'page': page,
                'limit': limit
            }
            response = await self._request('GET', '/v1/devices/available', params=params)
            return response
        except Exception as err:
            _LOGGER.error("Failed to get paginated devices: %s", err)
            return {'items': [], 'totalItems': 0}