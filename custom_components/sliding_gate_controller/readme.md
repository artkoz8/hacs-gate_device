# Hexagonal Gate Controller for Home Assistant

Integracja sterownika bramy wjazdowej (FAAC 740) zaimplementowana zgodnie z zasadami **Architektury Heksagonalnej** (Ports and Adapters) oraz **DDD** (Domain-Driven Design).

## 🏗️ Architektura
Projekt został podzielony na wyraźne warstwy zgodnie z zasadą *Screaming Architecture*:

- **Domain**: Czysta logika biznesowa bramy, niezależna od Home Assistanta.
  - `model/`: Agregat bramy zarządza stanem i intencjami.
  - `port/`: Interfejsy definiujące wymagania wobec sprzętu.
  - `event/`: Zdarzenia domenowe publikowane po wykonaniu akcji.
- **Application**: Orkiestracja i połączenie domeny ze światem zewnętrznym.
  - `gate_service.py`: Application Service tłumaczący akcje HA na wywołania agregatu.
- **Infrastructure**: Implementacja szczegółów technicznych.
  - `adapter/`: Fizyczny adapter FAAC 740 realizujący specyficzny flow impulsów (STOP -> DELAY -> OPEN).

## 🚀 Funkcjonalności
- Pełna izolacja logiki sterowania od infrastruktury.
- Obsługa specyficznej sekwencji impulsów dla sterowników FAAC.
- Publikowanie zdarzeń `sliding_gate_controller_event` na szynie zdarzeń HA, co pozwala na łatwe podpięcie automatyzacji (np. oświetlenia podjazdu).

## 🛠️ Konfiguracja
Integracja jest ładowana manualnie. W `configuration.yaml` należy dodać wpis:
```yaml
sliding_gate_controller: