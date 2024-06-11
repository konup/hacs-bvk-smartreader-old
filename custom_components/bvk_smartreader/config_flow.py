"""Config flow for BVK SmartReader integration."""
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
from .const import DOMAIN

@callback
def configured_instances(hass):
    """Return a set of configured instances."""
    return set(entry.data["username"] for entry in hass.config_entries.async_entries(DOMAIN))

class BVKSmartReaderConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for BVK SmartReader."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            if user_input["username"] in configured_instances(self.hass):
                errors["base"] = "username_exists"
            if not errors:
                return self.async_create_entry(title="BVK SmartReader", data=user_input)

        data_schema = vol.Schema({
            vol.Required("username", description={"suggested_value": "Enter your username"}): str,
            vol.Required("password", description={"suggested_value": "Enter your password"}): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "username": "Enter your zis.bvk.cz username",
                "password": "Enter your zis.bvk.cz password"
            }
        )
