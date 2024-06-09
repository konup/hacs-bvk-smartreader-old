import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD, CONF_UPDATE_INTERVAL

class BvkSmartReaderConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="BVK Smart Reader", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(CONF_UPDATE_INTERVAL, default=8): vol.All(vol.Coerce(int), vol.Range(min=1))
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return BvkSmartReaderOptionsFlowHandler(config_entry)

class BvkSmartReaderOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME, default=self.config_entry.data.get(CONF_USERNAME)): str,
                vol.Required(CONF_PASSWORD, default=self.config_entry.data.get(CONF_PASSWORD)): str,
                vol.Required(CONF_UPDATE_INTERVAL, default=self.config_entry.data.get(CONF_UPDATE_INTERVAL, 8)): vol.All(vol.Coerce(int), vol.Range(min=1))
            })
        )
