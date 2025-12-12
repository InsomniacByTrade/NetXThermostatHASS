"""Button platform for NetX Thermostat integration."""
import logging
import aiohttp

from homeassistant.components.button import ButtonEntity
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the NetX Thermostat button platform."""
    host = config_entry.data[CONF_HOST]
    username = config_entry.data[CONF_USERNAME]
    password = config_entry.data[CONF_PASSWORD]

    buttons = [
        NetXRebootButton(config_entry, host, username, password),
    ]

    async_add_entities(buttons)


class NetXRebootButton(ButtonEntity):
    """Representation of a NetX Thermostat Reboot Button."""

    _attr_has_entity_name = True
    _attr_name = "Restart"
    _attr_icon = "mdi:restart"

    def __init__(
        self,
        config_entry: ConfigEntry,
        host: str,
        username: str,
        password: str,
    ):
        """Initialize the button."""
        self._host = host
        self._username = username
        self._password = password
        self._attr_unique_id = f"{config_entry.entry_id}_restart"
        
        device_name = config_entry.data.get("device_name", "NetX Thermostat")
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": device_name,
            "manufacturer": "NetX",
            "model": "Thermostat",
        }

    async def async_press(self) -> None:
        """Handle the button press - restart the thermostat."""
        url = f"http://{self._host}/reboot.htm"
        auth = aiohttp.BasicAuth(self._username, self._password)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url, auth=auth, timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        _LOGGER.info("Thermostat restart command sent successfully")
                    else:
                        _LOGGER.error("Failed to restart thermostat: %s", response.status)
        except aiohttp.ClientError as err:
            _LOGGER.error("Error sending restart command: %s", err)
