from typing import List

# Importy relatywne wychodzące o jeden poziom wyżej do paczki domain
from ..port.gate_hardware_port import GateHardwarePort
from ..event.gate_intent_event import GateIntentEvent

class GateAggregate:
    """Główny punkt wejścia do logiki domeny bramy."""
    
    def __init__(self, hardware: GateHardwarePort):
        self._hardware = hardware
        self._events: List[GateIntentEvent] = []

    async def open(self) -> None:
        await self._hardware.trigger_open_sequence()
        self._events.append(GateIntentEvent(action="opening"))

    async def close(self) -> None:
        await self._hardware.trigger_close_sequence()
        self._events.append(GateIntentEvent(action="closing"))

    async def stop(self) -> None:
        await self._hardware.trigger_stop_sequence()
        self._events.append(GateIntentEvent(action="stopped"))

    def pull_events(self) -> List[GateIntentEvent]:
        """Zwraca listę zdarzeń i czyści bufor."""
        events = self._events.copy()
        self._events.clear()
        return events