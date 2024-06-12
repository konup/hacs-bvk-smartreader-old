"""The BVK SmartReader integration."""
import os
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the BVK SmartReader component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up BVK SmartReader from a config entry."""
    hass.data[DOMAIN] = entry.data

    # Set execute permission for the script
    script_path = hass.config.path('custom_components/bvk_smartreader/getBvkSuezData.sh')
    if os.path.exists(script_path):
        os.chmod(script_path, 0o755)

    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "sensor"))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    hass.data.pop(DOMAIN)
    return True
