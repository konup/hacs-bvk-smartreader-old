import subprocess
from homeassistant.helpers.entity import Entity

from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up BVK Smart Reader sensor platform."""
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

        try:
            result = subprocess.run(
                [script_path, username, password],
                capture_output=True,
                text=True,
                check=True
            )
            self._state = result.stdout.strip()  # Get the output from the script
        except subprocess.CalledProcessError as e:
            self._state = None
            # Log error or handle as needed
            self._state = f"Error: {e}"
