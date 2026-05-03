# __init__.py
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

# Używamy kropki (import relatywny), aby uniknąć błędów przy zmianie nazwy folderu
from .const import DOMAIN, CONF_STOP_SWITCH, CONF_OPEN_A_SWITCH, CONF_OPEN_B_SWITCH
from .infrastructure.adapter.faac740_physical_gate_adapter import Faac740PhysicalGateAdapter
from .domain import GateAggregate
from .application.gate_service import GateService

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setup integracji wyklikanej w UI."""
    _LOGGER.info("!!! [%s] Inicjalizacja z Config Flow (UI) !!!", DOMAIN)

    entity_map = {
        "stop": entry.data[CONF_STOP_SWITCH],
        "open_a": entry.data[CONF_OPEN_A_SWITCH],
        "open_b": entry.data[CONF_OPEN_B_SWITCH]
    }

    adapter = Faac740PhysicalGateAdapter(hass, entity_map)
    aggregate = GateAggregate(adapter)
    gate_service = GateService(hass, aggregate)

    async def handle_open(call): await gate_service.open_gate()
    async def handle_close(call): await gate_service.close_gate()
    async def handle_stop(call): await gate_service.stop_gate()

    hass.services.async_register(DOMAIN, "open", handle_open)
    hass.services.async_register(DOMAIN, "close", handle_close)
    hass.services.async_register(DOMAIN, "stop", handle_stop)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = gate_service

    return True