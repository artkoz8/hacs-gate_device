import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from .const import DOMAIN, CONF_STOP_SWITCH, CONF_OPEN_A_SWITCH, CONF_OPEN_B_SWITCH

class HexGateConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Obsługa formularza konfiguracji w UI."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Pierwszy krok konfiguracji wywołany przez użytkownika."""
        errors = {}

        if user_input is not None:
            # Tutaj można dodać walidację, czy encje istnieją
            return self.async_create_entry(title="Sterownik Bramy", data=user_input)

        # Definicja pól formularza z selektorami encji (ładne listy rozwijane)
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
            step_id="user", data_schema=data_schema, errors=errors
        )