import asyncio
import logging
from typing import Dict

from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_ENTITIES

from ...domain.port.gate_hardware_port import GateHardwarePort
from ...const import (
    SWITCH_DOMAIN, 
    SERVICE_TURN_ON, 
    SERVICE_TURN_OFF, 
    PULSE_DURATION, 
    INTER_PULSE_DELAY
)

_LOGGER = logging.getLogger(__name__)

class Faac740PhysicalGateAdapter(GateHardwarePort):
    """Adapter dla napędu FAAC 740 realizujący specyficzny flow impulsów."""

    def __init__(self, hass: HomeAssistant, entity_map: Dict[str, str]):
        self._hass = hass
        self._stop_pin = entity_map["stop"]
        self._open_a_pin = entity_map["open_a"]
        self._open_b_pin = entity_map["open_b"]

    async def _fire_pulse(self, entity_id: str) -> None:
        """Realizuje cykl off -> on -> off."""
        _LOGGER.debug("Firing pulse on entity: %s", entity_id)
        
        await self._hass.services.async_call(
            SWITCH_DOMAIN, SERVICE_TURN_ON, {"entity_id": entity_id}
        )
        await asyncio.sleep(PULSE_DURATION)
        await self._hass.services.async_call(
            SWITCH_DOMAIN, SERVICE_TURN_OFF, {"entity_id": entity_id}
        )

    async def trigger_open_sequence(self) -> None:
        # Flow: stop -> delay -> open_a
        await self._fire_pulse(self._stop_pin)
        await asyncio.sleep(INTER_PULSE_DELAY)
        await self._fire_pulse(self._open_a_pin)

    async def trigger_close_sequence(self) -> None:
        # Flow: stop -> delay -> open_b
        await self._fire_pulse(self._stop_pin)
        await asyncio.sleep(INTER_PULSE_DELAY)
        await self._fire_pulse(self._open_b_pin)

    async def trigger_stop_sequence(self) -> None:
        # Flow: stop
        await self._fire_pulse(self._stop_pin)