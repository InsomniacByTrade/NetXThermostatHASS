"""Sensor platform for NetX Thermostat integration."""
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    UnitOfTemperature,
)
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
    """Set up the NetX Thermostat sensor platform."""
    from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
    
    host = config_entry.data[CONF_HOST]
    username = config_entry.data[CONF_USERNAME]
    password = config_entry.data[CONF_PASSWORD]
    
    coordinator = NetXDataUpdateCoordinator(hass, host, username, password)
    await coordinator.async_config_entry_first_refresh()

    sensors = [
        # CO2 Level Sensors
        NetXCO2Sensor(coordinator, config_entry, "co2_level", "CO2 Level", "mdi:molecule-co2"),
        NetXCO2Sensor(coordinator, config_entry, "co2_peak_level", "CO2 Peak Level", "mdi:chart-line"),
        NetXCO2Sensor(coordinator, config_entry, "co2_alert_level", "CO2 Alert Level", "mdi:alert-circle"),
        
        # CO2 Binary/Text Sensors
        NetXBinarySensor(coordinator, config_entry, "co2_type", "CO2 Type", "mdi:information"),
        NetXBinarySensor(coordinator, config_entry, "co2_valid", "CO2 Valid", "mdi:check-circle"),
        NetXBinarySensor(coordinator, config_entry, "co2_in_alert", "CO2 In Alert", "mdi:alert"),
        NetXBinarySensor(coordinator, config_entry, "co2_peak_reset", "CO2 Peak Reset", "mdi:restore"),
        NetXBinarySensor(coordinator, config_entry, "co2_display", "CO2 Display", "mdi:monitor"),
        NetXBinarySensor(coordinator, config_entry, "co2_relay_high", "CO2 Relay High", "mdi:electric-switch"),
        NetXBinarySensor(coordinator, config_entry, "co2_relay_failure", "CO2 Relay Failure", "mdi:alert-circle"),
        
        # Temperature Sensors
        NetXTemperatureSensor(coordinator, config_entry, "outdoor", "Outdoor Temperature", "mdi:thermometer"),
        
        # Humidity Sensors
        NetXHumiditySensor(coordinator, config_entry, "outhum", "Outdoor Humidity", "mdi:water-percent"),
        
        # Schedule/Program Sensors
        NetXBinarySensor(coordinator, config_entry, "manual_program", "Manual Program", "mdi:calendar-edit"),
        NetXBinarySensor(coordinator, config_entry, "cursched", "Current Schedule", "mdi:calendar-clock"),
        NetXBinarySensor(coordinator, config_entry, "schedstat1", "Schedule Status 1", "mdi:calendar-check"),
        NetXBinarySensor(coordinator, config_entry, "schedstat", "Schedule Status", "mdi:calendar-check"),
        NetXBinarySensor(coordinator, config_entry, "isoverride", "Override Active", "mdi:lock-open"),
        
        # Setpoint Sensors (Occupied/Unoccupied)
        NetXTemperatureSensor(coordinator, config_entry, "ul_occ_cool", "Upper Occupied Cool", "mdi:thermometer-high"),
        NetXTemperatureSensor(coordinator, config_entry, "l_occ_cool", "Lower Occupied Cool", "mdi:thermometer-low"),
        NetXTemperatureSensor(coordinator, config_entry, "ul_unocc_cool", "Upper Unoccupied Cool", "mdi:thermometer-high"),
        NetXTemperatureSensor(coordinator, config_entry, "l_unocc_cool", "Lower Unoccupied Cool", "mdi:thermometer-low"),
        NetXTemperatureSensor(coordinator, config_entry, "ul_occ_heat", "Upper Occupied Heat", "mdi:thermometer-high"),
        NetXTemperatureSensor(coordinator, config_entry, "l_occ_heat", "Lower Occupied Heat", "mdi:thermometer-low"),
        NetXTemperatureSensor(coordinator, config_entry, "ul_unocc_heat", "Upper Unoccupied Heat", "mdi:thermometer-high"),
        NetXTemperatureSensor(coordinator, config_entry, "l_unocc_heat", "Lower Unoccupied Heat", "mdi:thermometer-low"),
        
        # Indicator Sensors
        NetXBinarySensor(coordinator, config_entry, "ind0", "Indicator 0", "mdi:numeric-0-circle"),
        NetXBinarySensor(coordinator, config_entry, "ind1", "Indicator 1", "mdi:numeric-1-circle"),
        NetXBinarySensor(coordinator, config_entry, "ind2", "Indicator 2", "mdi:numeric-2-circle"),
        
        # System Status Sensors
        NetXBinarySensor(coordinator, config_entry, "sysadapt", "System Adapt", "mdi:auto-fix"),
        NetXBinarySensor(coordinator, config_entry, "ishumidity", "Has Humidity", "mdi:water-percent"),
        NetXBinarySensor(coordinator, config_entry, "ishumidityinternal", "Internal Humidity", "mdi:home-thermometer"),
        NetXBinarySensor(coordinator, config_entry, "is_locked", "Locked", "mdi:lock"),
        
        # Additional Sensors
        NetXBinarySensor(coordinator, config_entry, "sensor0", "Sensor 0", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "sensor1", "Sensor 1", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "sensor2", "Sensor 2", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "sensor3", "Sensor 3", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "sensor4", "Sensor 4", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "sensor5", "Sensor 5", "mdi:thermometer"),
        
        # Raw Value Sensors (ending in _r)
        NetXBinarySensor(coordinator, config_entry, "curtemp_r", "Current Temperature Raw", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "outdoor_r", "Outdoor Temperature Raw", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "sptcool_r", "Cool Setpoint Raw", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "sptheat_r", "Heat Setpoint Raw", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "sensor_idt_r", "Indoor Temperature Raw", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "sensor_odt_r", "Outdoor Temperature Raw", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "sensor_ihum_r", "Indoor Humidity Raw", "mdi:water-percent"),
        NetXBinarySensor(coordinator, config_entry, "sensor_ohum_r", "Outdoor Humidity Raw", "mdi:water-percent"),
        NetXBinarySensor(coordinator, config_entry, "sensor_occ_r", "Occupancy Raw", "mdi:account"),
        NetXBinarySensor(coordinator, config_entry, "sensor_door_r", "Door Sensor Raw", "mdi:door"),
        NetXBinarySensor(coordinator, config_entry, "sensor1_r", "Sensor 1 Raw", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "sensor2_r", "Sensor 2 Raw", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "sensor3_r", "Sensor 3 Raw", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "sensor4_r", "Sensor 4 Raw", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "sensor5_r", "Sensor 5 Raw", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "sensor6_r", "Sensor 6 Raw", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "sensor7_r", "Sensor 7 Raw", "mdi:thermometer"),
        NetXBinarySensor(coordinator, config_entry, "sensor_water_r", "Water Sensor Raw", "mdi:water-alert"),
        
        # X7 Sensors
        NetXBinarySensor(coordinator, config_entry, "x7hkhd", "X7 HKHD", "mdi:alpha-x"),
        NetXBinarySensor(coordinator, config_entry, "x7hk2", "X7 HK2", "mdi:alpha-x"),
    ]

    async_add_entities(sensors)


class NetXCO2Sensor(CoordinatorEntity, SensorEntity):
    """Representation of a NetX CO2 Sensor."""

    _attr_device_class = SensorDeviceClass.CO2
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = CONCENTRATION_PARTS_PER_MILLION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: NetXDataUpdateCoordinator,
        config_entry: ConfigEntry,
        sensor_type: str,
        name: str,
        icon: str,
    ):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_type}"
        
        device_name = config_entry.data.get("device_name", "NetX Thermostat")
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": device_name,
            "manufacturer": "NetX",
            "model": "Thermostat",
        }

    @property
    def native_value(self):
        """Return the state of the sensor."""
        value = self.coordinator.data.get(self._sensor_type)
        if value is not None and value != "--":
            try:
                return int(value)
            except (ValueError, TypeError):
                return None
        return None

    @property
    def available(self):
        """Return if entity is available."""
        value = self.coordinator.data.get(self._sensor_type)
        return (
            self.coordinator.last_update_success
            and value is not None
            and value != "--"
        )


class NetXTemperatureSensor(CoordinatorEntity, SensorEntity):
    """Representation of a NetX Temperature Sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.FAHRENHEIT
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: NetXDataUpdateCoordinator,
        config_entry: ConfigEntry,
        sensor_type: str,
        name: str,
        icon: str,
    ):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_type}"
        
        device_name = config_entry.data.get("device_name", "NetX Thermostat")
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": device_name,
            "manufacturer": "NetX",
            "model": "Thermostat",
        }

    @property
    def native_value(self):
        """Return the state of the sensor."""
        value = self.coordinator.data.get(self._sensor_type)
        if value is not None and value != "--":
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        return None

    @property
    def available(self):
        """Return if entity is available."""
        value = self.coordinator.data.get(self._sensor_type)
        return (
            self.coordinator.last_update_success
            and value is not None
            and value != "--"
        )


class NetXHumiditySensor(CoordinatorEntity, SensorEntity):
    """Representation of a NetX Humidity Sensor."""

    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: NetXDataUpdateCoordinator,
        config_entry: ConfigEntry,
        sensor_type: str,
        name: str,
        icon: str,
    ):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_type}"
        
        device_name = config_entry.data.get("device_name", "NetX Thermostat")
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": device_name,
            "manufacturer": "NetX",
            "model": "Thermostat",
        }

    @property
    def native_value(self):
        """Return the state of the sensor."""
        value = self.coordinator.data.get(self._sensor_type)
        if value is not None and value != "--":
            try:
                return int(value)
            except (ValueError, TypeError):
                return None
        return None

    @property
    def available(self):
        """Return if entity is available."""
        value = self.coordinator.data.get(self._sensor_type)
        return (
            self.coordinator.last_update_success
            and value is not None
            and value != "--"
        )


class NetXBinarySensor(CoordinatorEntity, SensorEntity):
    """Representation of a NetX Binary/Text Sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: NetXDataUpdateCoordinator,
        config_entry: ConfigEntry,
        sensor_type: str,
        name: str,
        icon: str,
    ):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_type}"
        
        device_name = config_entry.data.get("device_name", "NetX Thermostat")
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": device_name,
            "manufacturer": "NetX",
            "model": "Thermostat",
        }

    @property
    def native_value(self):
        """Return the state of the sensor."""
        value = self.coordinator.data.get(self._sensor_type)
        if value is not None and value != "--":
            return str(value)
        return None

    @property
    def available(self):
        """Return if entity is available."""
        value = self.coordinator.data.get(self._sensor_type)
        return (
            self.coordinator.last_update_success
            and value is not None
            and value != "--"
        )
