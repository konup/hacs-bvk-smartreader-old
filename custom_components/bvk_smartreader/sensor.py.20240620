import subprocess
import logging
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import async_get_platforms
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up BVK Smart Reader sensor platform."""
    # Check if the entity is already added to avoid duplication
    platforms = async_get_platforms(hass, DOMAIN)
    if any(platform.platform_name == 'sensor' for platform in platforms):
        _LOGGER.warning("BVK Smart Reader sensor has already been set up!")
        return

    async_add_entities([WaterMeterSensor(hass.data[DOMAIN])])

class WaterMeterSensor(Entity):
    """Representation of a Water Meter sensor."""

    def __init__(self, config):
        self._config = config
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Water Meter"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        username = self._config["username"]
        password = self._config["password"]
        script_path = './custom_components/bvk_smartreader/getBvkSuezData.sh'

        _LOGGER.debug("Checking if script is executable: %s", script_path)
        result = subprocess.run(['ls', '-l', script_path], capture_output=True, text=True)
        _LOGGER.debug("Script permissions: %s", result.stdout.strip())

        try:
            _LOGGER.debug("Running script %s with username %s", script_path, username)
            result = subprocess.run(
                [script_path, username, password],
                capture_output=True,
                text=True,
                check=True
            )
            _LOGGER.debug("Script output: %s", result.stdout.strip())
            self._state = result.stdout.strip()  # Get the output from the script
        except subprocess.CalledProcessError as e:
            _LOGGER.error("Script error: %s", e)
            self._state = None
            # Log error or handle as needed
            self._state = f"Error: {e}"
