from typing import Protocol

class GateHardwarePort(Protocol):
    """
    Interfejs wyjściowy dla sprzętu. 
    Definiuje operacje bez zdradzania szczegółów implementacji.
    """
    async def trigger_open_sequence(self) -> None: ...
    async def trigger_close_sequence(self) -> None: ...
    async def trigger_stop_sequence(self) -> None: ...