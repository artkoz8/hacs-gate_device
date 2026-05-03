import logging
from homeassistant.core import HomeAssistant

# Cofamy się o dwa poziomy do hex_gate, potem do domain
from ..domain.model.gate_aggregate import GateAggregate
from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class GateService:
    """Application Service - Orkiestrator akcji i zdarzeń."""

    def __init__(self, hass: HomeAssistant, aggregate: GateAggregate):
        self._hass = hass
        self._aggregate = aggregate

    async def open_gate(self) -> None:
        await self._aggregate.open()
        self._publish_events()

    async def close_gate(self) -> None:
        await self._aggregate.close()
        self._publish_events()

    async def stop_gate(self) -> None:
        await self._aggregate.stop()
        self._publish_events()

    def _publish_events(self) -> None:
        """Pobiera eventy z domeny i publikuje je na szynie HA."""
        for event in self._aggregate.pull_events():
            event_type = f"{DOMAIN}_event"
            _LOGGER.debug("Firing HA event: %s with action: %s", event_type, event.action)
            self._hass.bus.async_fire(
                event_type,
                {"action": event.action}
            )