"""The BVK SmartReader integration."""
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the BVK SmartReader component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry):
    """Set up BVK SmartReader from a config entry."""
    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, "sensor"))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True
