import subprocess
import logging
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the BVK SmartReader sensor."""
    username = config.get("username")
    password = config.get("password")

    if username is None or password is None:
        _LOGGER.error("Username and password must be set in the configuration")
        return

    add_entities([WaterMeterSensor(username, password)])

class WaterMeterSensor(Entity):
    """Representation of a BVK SmartReader sensor."""

    def __init__(self, username, password):
        """Initialize the sensor."""
        self._state = None
        self._username = username
        self._password = password

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Water Meter'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor."""
        try:
            result = subprocess.run(
                ['./custom_components/bvk_smartreader/getBvkSuezData.sh', self._username, self._password],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            self._state = result.stdout.decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            _LOGGER.error(f"Error fetching data from BVK SmartReader: {e.stderr.decode('utf-8')}")
            self._state = None
