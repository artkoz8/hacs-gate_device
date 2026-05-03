# __init__.py
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

# Używamy importów relatywnych do konkretnych plików, aby uniknąć błędów ładowania
from .const import DOMAIN, CONF_STOP_SWITCH, CONF_OPEN_A_SWITCH, CONF_OPEN_B_SWITCH
from .infrastructure.adapter.faac740_physical_gate_adapter import Faac740PhysicalGateAdapter
from .domain.model.gate_aggregate import GateAggregate
from .application.gate_service import GateService

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Zostawiamy True dla wsparcia UI."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setup integracji wyklikanej w UI."""
    _LOGGER.info("!!! [%s] Inicjalizacja Sterownika Bramy !!!", DOMAIN)

    # Pobieramy dane z zapisanego "Entry"
    entity_map = {
        "stop": entry.data[CONF_STOP_SWITCH],
        "open_a": entry.data[CONF_OPEN_A_SWITCH],
        "open_b": entry.data[CONF_OPEN_B_SWITCH]
    }

    # Składamy architekturę (Dependency Injection) z poprawnymi ścieżkami
    adapter = Faac740PhysicalGateAdapter(hass, entity_map)
    aggregate = GateAggregate(adapter)
    gate_service = GateService(hass, aggregate)

    # Rejestracja usług (Actions) pod nową domeną
    async def handle_open(call): await gate_service.open_gate()
    async def handle_close(call): await gate_service.close_gate()
    async def handle_stop(call): await gate_service.stop_gate()

    hass.services.async_register(DOMAIN, "open", handle_open)
    hass.services.async_register(DOMAIN, "close", handle_close)
    hass.services.async_register(DOMAIN, "stop", handle_stop)

    # Przechowywanie instancji serwisu
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = gate_service

    return True