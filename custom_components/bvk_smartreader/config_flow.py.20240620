import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

class BVKSmartReaderConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for BVK Smart Reader."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return BVKSmartReaderOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the user input here
            username = user_input["username"]
            password = user_input["password"]

            # Try to authenticate (simplified example, replace with actual check)
            if username and password:
                return self.async_create_entry(title="BVK Smart Reader", data=user_input)
            else:
                errors["base"] = "auth"

        data_schema = vol.Schema({
            vol.Required("username"): str,
            vol.Required("password"): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

class BVKSmartReaderOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for BVK Smart Reader."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle the options flow."""
        errors = {}

        if user_input is not None:
            # Validate the user input here
            username = user_input["username"]
            password = user_input["password"]

            # Try to authenticate (simplified example, replace with actual check)
            if username and password:
                self.hass.config_entries.async_update_entry(
                    self.config_entry, data=user_input
                )
                return self.async_create_entry(title="BVK Smart Reader", data=user_input)
            else:
                errors["base"] = "auth"

        data_schema = vol.Schema({
            vol.Required("username", default=self.config_entry.data.get("username", "")): str,
            vol.Required("password", default=self.config_entry.data.get("password", "")): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

