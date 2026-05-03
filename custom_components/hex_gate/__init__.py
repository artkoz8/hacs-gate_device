# __init__.py
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.hex_gate.const import DOMAIN, CONF_STOP_SWITCH, CONF_OPEN_A_SWITCH, CONF_OPEN_B_SWITCH
from custom_components.hex_gate.infrastructure.adapter.faac740_physical_gate_adapter import Faac740PhysicalGateAdapter
from custom_components.hex_gate.domain import GateAggregate
from custom_components.hex_gate.application.gate_service import GateService

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Zostawiamy puste dla wsparcia UI, chyba że chcesz też wspierać YAML."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setup integracji wyklikanej w UI."""
    _LOGGER.error("!!! [HEX_GATE] Inicjalizacja z Config Flow (UI) !!!")

    # Pobieramy dane z zapisanego "Entry"
    entity_map = {
        "stop": entry.data[CONF_STOP_SWITCH],
        "open_a": entry.data[CONF_OPEN_A_SWITCH],
        "open_b": entry.data[CONF_OPEN_B_SWITCH]
    }

    # Składamy architekturę (Dependency Injection)
    adapter = Faac740PhysicalGateAdapter(hass, entity_map)
    aggregate = GateAggregate(adapter)
    gate_service = GateService(hass, aggregate)

    # Rejestracja usług (Actions)
    async def handle_open(call): await gate_service.open_gate()
    async def handle_close(call): await gate_service.close_gate()
    async def handle_stop(call): await gate_service.stop_gate()

    hass.services.async_register(DOMAIN, "open", handle_open)
    hass.services.async_register(DOMAIN, "close", handle_close)
    hass.services.async_register(DOMAIN, "stop", handle_stop)

    # Zapisujemy serwis w hass.data, żeby mieć do niego dostęp później (opcjonalnie)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = gate_service

    return True