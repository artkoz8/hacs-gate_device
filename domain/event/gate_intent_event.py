from dataclasses import dataclass

@dataclass(frozen=True)
class GateIntentEvent:
    """Reprezentuje intencję wykonania akcji na bramie."""
    action: str