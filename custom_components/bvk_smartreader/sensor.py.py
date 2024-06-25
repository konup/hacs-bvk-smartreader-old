import logging
import subprocess
import json
import datetime
import os
from datetime import timedelta, datetime as dt
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfVolume
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD, CONF_UPDATE_INTERVAL

# Ensure the logs directory exists
os.makedirs('./custom_components/bvk_smartreader/logs', exist_ok=True)

class Colors:
    RED = 'ERROR '
    GREEN = 'SUCCESS '
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = 'WARN '
    CYAN = 'INFO '
    RESET = ''

# Create a custom logger for the component
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

# File handler for writing logs to a file
file_handler = logging.FileHandler('./custom_components/bvk_smartreader/logs/bvk_smartreader.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
_LOGGER.addHandler(file_handler)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    pass

async def async_setup_entry(hass, entry, async_add_entities):
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    update_interval = entry.data.get(CONF_UPDATE_INTERVAL, 8)
    days = 1

    water_consumption_sensor = WaterConsumptionSensor(hass, username, password, days, update_interval)

    async_add_entities([water_consumption_sensor], True)

class WaterDataSensor(Entity):
    def __init__(self, hass, username, password, days, update_interval):
        self.hass = hass
        self.username = username
        self.password = password
        self.days = days
        self.update_interval = timedelta(hours=update_interval)
        self._state = None
        self._attributes = {}
        self._unique_id = f"bvk_smartreader"
        self.entity_id = f"sensor.bvk_smartreader"
        self._last_reset = None
        _LOGGER.debug(dt.now().strftime("%Y-%m-%d %H:%M:%S") + f": {Colors.CYAN}Initialized WaterDataSensor with Username: {self.username}{Colors.RESET}")
        self.update = Throttle(self.update_interval)(self.update)
        self.update()

    @property
    def name(self):
        return "Water Data Sensor"

    @property
    def state(self):
        return self._state

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def extra_state_attributes(self):
        return self._attributes

    @property
    def state_class(self):
        return SensorStateClass.TOTAL_INCREASING

    @property
    def unit_of_measurement(self):
        return UnitOfVolume.CUBIC_METERS

    @property
    def device_class(self):
        return SensorDeviceClass.WATER

    @property
    def last_reset(self):
        return self._last_reset

    @property
    def icon(self):
        return "mdi:gauge"

    def update(self, no_throttle=False):
        if not self.username:
            _LOGGER.warning(dt.now().strftime("%Y-%m-%d %H:%M:%S") + f": {Colors.RED}Username is not set. Skipping update.{Colors.RESET}")
            return

        _LOGGER.debug(dt.now().strftime("%Y-%m-%d %H:%M:%S") + f": {Colors.CYAN}>>>>>>>>>>>Updating Water Data Sensor for Username: {self.username}{Colors.RESET}")
        try:
            self._get_data()
        except Exception as e:
            _LOGGER.error(dt.now().strftime("%Y-%m-%d %H:%M:%S") + f": {Colors.RED}Error updating sensor: {e}{Colors.RESET}")

    def _get_data(self):
        _LOGGER.debug(dt.now().strftime("%Y-%m-%d %H:%M:%S") + f": {Colors.CYAN}Retrieving data{Colors.RESET}")

        try:
            result = subprocess.run(
                ['./custom_components/bvk_smartreader/getBvkSuezData.sh', self.username, self.password],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode != 0:
                _LOGGER.error(dt.now().strftime("%Y-%m-%d %H:%M:%S") + f": {Colors.RED}Error retrieving data: {result.stderr}{Colors.RESET}")
                return

            data = json.loads(result.stdout)

            total_value = sum(item['value'] for item in data)
            self._state = total_value
            self._attributes = {
                'data': data,
                'last_update': dt.now().strftime("%Y-%m-%d %H:%M:%S"),
                'unit_of_measurement': self.unit_of_measurement,
                'device_class': self.device_class,
                'state_class': self.state_class,
                'icon': self.icon
            }
            self._last_reset = dt.now().replace(hour=0, minute=0, second=0, microsecond=0)
            _LOGGER.debug(dt.now().strftime("%Y-%m-%d %H:%M:%S") + f": {Colors.CYAN}Total value: {total_value}{Colors.RESET}")
        except Exception as e:
            _LOGGER.error(dt.now().strftime("%Y-%m-%d %H:%M:%S") + f": {Colors.RED}Error retrieving data: {e}{Colors.RESET}")

class WaterConsumptionSensor(WaterDataSensor):
    def __init__(self, hass, username, password, days, update_interval):
        super().__init__(hass, username, password, days, update_interval)

