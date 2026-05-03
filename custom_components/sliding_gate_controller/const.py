"""Constants for the Hexagonal Gate integration."""

DOMAIN = "sliding_gate_controller"
SWITCH_DOMAIN = "switch"
SERVICE_TURN_ON = "turn_on"
SERVICE_TURN_OFF = "turn_off"

CONF_STOP_SWITCH = "stop_switch"
CONF_OPEN_A_SWITCH = "open_a_switch"
CONF_OPEN_B_SWITCH = "open_b_switch"

# Czas trwania impulsu i przerwy między nimi
PULSE_DURATION = 0.1
INTER_PULSE_DELAY = 0.1