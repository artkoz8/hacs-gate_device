import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from .const import DOMAIN, CONF_STOP_SWITCH, CONF_OPEN_A_SWITCH, CONF_OPEN_B_SWITCH

class SlidingGateConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Obsługa formularza konfiguracji Sterownika Bramy Przesuwnej."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Pierwszy krok konfiguracji wywołany przez użytkownika w UI."""
        errors = {}

        if user_input is not None:
            # Tworzymy wpis w HA - nazwa będzie widoczna w Urządzeniach
            return self.async_create_entry(title="Sterownik Bramy Przesuwnej", data=user_input)

        # Schemat formularza z ładnymi selektorami encji typu 'switch'
        data_schema = vol.Schema({
            vol.Required(CONF_STOP_SWITCH): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="switch")
            ),
            vol.Required(CONF_OPEN_A_SWITCH): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="switch")
            ),
            vol.Required(CONF_OPEN_B_SWITCH): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="switch")
            ),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )