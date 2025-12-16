"""Switch platform for NetX Thermostat integration."""
import logging
import aiohttp
import asyncio

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .climate import NetXDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the NetX Thermostat switch platform."""
    host = config_entry.data[CONF_HOST]
    username = config_entry.data[CONF_USERNAME]
    password = config_entry.data[CONF_PASSWORD]

    coordinator = NetXDataUpdateCoordinator(hass, host, username, password)
    await coordinator.async_config_entry_first_refresh()

    switches = [
        NetXFanSwitch(coordinator, config_entry, host, username, password),
    ]

    async_add_entities(switches)


class NetXFanSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a NetX Thermostat Fan Switch."""

    _attr_has_entity_name = True
    _attr_name = "Fan"
    _attr_icon = "mdi:fan"

    def __init__(
        self,
        coordinator: NetXDataUpdateCoordinator,
        config_entry: ConfigEntry,
        host: str,
        username: str,
        password: str,
    ):
        """Initialize the switch."""
        super().__init__(coordinator)
        self._host = host
        self._username = username
        self._password = password
        self._attr_unique_id = f"{config_entry.entry_id}_fan_switch"
        
        device_name = config_entry.data.get("device_name", "NetX Thermostat")
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": device_name,
            "manufacturer": "NetX",
            "model": "Thermostat",
        }

    @property
    def is_on(self):
        """Return true if fan is on."""
        fan_mode = self.coordinator.data.get("curfan", "AUTO")
        return fan_mode == "ON"

    async def async_turn_on(self, **kwargs):
        """Turn the fan on."""
        url = f"http://{self._host}/index.htm"
        data = {"fan": "ON", "update": "Update"}
        auth = aiohttp.BasicAuth(self._username, self._password)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, data=data, auth=auth, timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        _LOGGER.info("Fan turned on successfully")
                    else:
                        _LOGGER.error("Failed to turn on fan: %s", response.status)
        except aiohttp.ClientError as err:
            _LOGGER.error("Error turning on fan: %s", err)
        
        await asyncio.sleep(1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn the fan off."""
        url = f"http://{self._host}/index.htm"
        data = {"fan": "AUTO", "update": "Update"}
        auth = aiohttp.BasicAuth(self._username, self._password)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, data=data, auth=auth, timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        _LOGGER.info("Fan turned off successfully")
                    else:
                        _LOGGER.error("Failed to turn off fan: %s", response.status)
        except aiohttp.ClientError as err:
            _LOGGER.error("Error turning off fan: %s", err)
        
        await asyncio.sleep(1)
        await self.coordinator.async_request_refresh()
