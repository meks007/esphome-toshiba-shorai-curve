import re
from pathlib import Path


ROOT = Path(__file__).parent
HEADER = (ROOT / "esphome/toshiba_controller/toshiba_controller.h").read_text()
CODEGEN = (ROOT / "esphome/toshiba_controller/__init__.py").read_text()
CONFIG = (ROOT / "esphome/package.yaml").read_text()
TEMPLATE = (ROOT / "esphome/template_v3.yaml").read_text()


assert re.search(r"SWING_MODE_HADA_CARE_FLOW\s*=\s*0x60", HEADER)
assert re.search(
    r"case ToshibaSwingMode::SWING_MODE_HADA_CARE_FLOW:.*?"
    r'select_state = "HADA Care Flow";',
    HEADER,
    re.DOTALL,
)
assert re.search(
    r"case 9:.*?"
    r"internal_swing_mode_ = ToshibaSwingMode::SWING_MODE_HADA_CARE_FLOW;",
    HEADER,
    re.DOTALL,
)
assert "set_supported_swing_modes" not in HEADER

assert re.search(r"SELF_CLEANING\s*=\s*0xCB", HEADER)
assert re.search(r"SELF_CLEANING_ON\s*=\s*0x18", HEADER)
assert re.search(r"SELF_CLEANING_OFF\s*=\s*0x10", HEADER)
assert re.search(r"SELF_CLEANING_MIN_RUNTIME_MS\s+600000UL", HEADER)
assert re.search(
    r"previous_mode == climate::CLIMATE_MODE_COOL.*?"
    r"previous_mode == climate::CLIMATE_MODE_DRY.*?"
    r"ToshibaCommand::SELF_CLEANING,\s*"
    r"ToshibaSelfCleaning::SELF_CLEANING_ON.*?"
    r"ToshibaCommand::POWER_STATE, ToshibaState::STATE_OFF",
    HEADER,
    re.DOTALL,
)
assert "millis() - this->wet_operation_started_millis_ >= SELF_CLEANING_MIN_RUNTIME_MS" in HEADER

swing_options = re.search(
    r'name: Airflow Mode.*?options:\n(?P<options>.*?)\n\s+on_value:',
    CONFIG,
    re.DOTALL,
)
assert swing_options is not None
options = re.findall(r'^\s+- "([^"]+)"$', swing_options["options"], re.MULTILINE)
assert options[9] == "HADA Care Flow"

for name in ("Special Mode", "Silent Mode", "Fireplace"):
    assert re.search(rf"name: {name}\n\s+id: .+\n\s+internal: true", CONFIG)

assert "!secret" not in CONFIG
assert "files:\n      - esphome/package.yaml" in TEMPLATE
assert "cv.Optional(CONF_TEMPERATURE_SENSOR_ID)" in CODEGEN
assert "cv.Optional(CONF_ENABLE_SELF_CLEANING, default=False)" in CODEGEN
assert 'enable_self_cleaning: "true"' in CONFIG
assert "temperature_sensor_id" not in CONFIG
assert "temperature_sensor_entity_id" not in CONFIG
assert "SWITCH_ALWAYS_ON" in HEADER
assert re.search(
    r"internal_thermistor:\n\s+name: Internal Thermistor\n\s+internal: true",
    CONFIG,
)
assert "name: WiFi LED" not in CONFIG

print("Toshiba mappings are consistent")
