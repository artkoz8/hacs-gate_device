import logging
import asyncio
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType

# Importy z Twojej struktury katalogów
from .const import DOMAIN
from .infrastructure.adapter.faac740_physical_gate_adapter import Faac740PhysicalGateAdapter
from .domain.model.gate_aggregate import GateAggregate
from .application.gate_service import GateService

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Setup integracji hex_gate."""
    _LOGGER.error("!!! [HEX_GATE] INICJALIZACJA ARCHITEKTURY !!!")
    
    try:
        # 1. Mapowanie encji (Upewnij się, że te ID są poprawne w Twoim HA)
        entity_map = {
            "stop": "switch.brama_wjazdowa_stop",   
            "open_a": "switch.brama_wjazdowa_a_open",
            "open_b": "switch.brama_wjazdowa_b_open"
        }

        # 2. Dependency Injection (Składanie klocków)
        adapter = Faac740PhysicalGateAdapter(hass, entity_map)
        aggregate = GateAggregate(adapter)
        gate_service = GateService(hass, aggregate)

        # 3. Rejestracja usług (Actions)
        async def handle_open(call: ServiceCall):
            _LOGGER.warning("[HEX_GATE] Wywołano akcję OPEN")
            await gate_service.open_gate()

        async def handle_close(call: ServiceCall):
            _LOGGER.warning("[HEX_GATE] Wywołano akcję CLOSE")
            await gate_service.close_gate()

        async def handle_stop(call: ServiceCall):
            _LOGGER.warning("[HEX_GATE] Wywołano akcję STOP")
            await gate_service.stop_gate()

        hass.services.async_register(DOMAIN, "open", handle_open)
        hass.services.async_register(DOMAIN, "close", handle_close)
        hass.services.async_register(DOMAIN, "stop", handle_stop)

        _LOGGER.error("!!! [HEX_GATE] ARCHITEKTURA ZAŁADOWANA POMYŚLNIE !!!")
        return True

    except Exception as e:
        _LOGGER.error("!!! [HEX_GATE] BŁĄD SETUPU: %s", str(e), exc_info=True)
        return False