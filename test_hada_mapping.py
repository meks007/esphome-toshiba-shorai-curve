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
    r"case 4:.*?"
    r"internal_swing_mode_ = ToshibaSwingMode::SWING_MODE_HADA_CARE_FLOW;",
    HEADER,
    re.DOTALL,
)
assert "set_supported_swing_modes" not in HEADER

assert "set_supported_custom_fan_modes" not in HEADER
assert "add_supported_fan_mode(climate::CLIMATE_FAN_QUIET)" not in HEADER
for mode in ("AUTO", "LOW", "MEDIUM", "HIGH"):
    assert f"add_supported_fan_mode(climate::CLIMATE_FAN_{mode})" in HEADER
assert re.search(
    r"case ToshibaFanMode::FAN_QUIET:\s*"
    r"case ToshibaFanMode::FAN_LOW:.*?"
    r"set_fan_mode_\(climate::CLIMATE_FAN_LOW\)",
    HEADER,
    re.DOTALL,
)
assert re.search(
    r"case ToshibaFanMode::FAN_LOW_MEDIUM:\s*"
    r"case ToshibaFanMode::FAN_MEDIUM:.*?"
    r"set_fan_mode_\(climate::CLIMATE_FAN_MEDIUM\)",
    HEADER,
    re.DOTALL,
)
assert re.search(
    r"case ToshibaFanMode::FAN_MEDIUM_HIGH:\s*"
    r"case ToshibaFanMode::FAN_HIGH:.*?"
    r"set_fan_mode_\(climate::CLIMATE_FAN_HIGH\)",
    HEADER,
    re.DOTALL,
)

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
assert options == ["Off", "Vertical", "Horizontal", "Vertical & Horizontal", "HADA Care Flow"]
assert all(f"Fixed {position}" not in options for position in range(1, 6))
for position in range(1, 6):
    assert re.search(
        rf"case ToshibaSwingMode::SWING_MODE_FIXED_{position}:.*?"
        r'select_state = "Off";',
        HEADER,
        re.DOTALL,
    )

for name in ("Special Mode", "Silent Mode", "Fireplace"):
    assert re.search(rf"name: {name}\n\s+id: .+\n\s+internal: true", CONFIG)

assert "!secret" not in CONFIG
assert "files:\n      - esphome/package.yaml" in TEMPLATE
assert "cv.Optional(CONF_TEMPERATURE_SENSOR_ID)" in CODEGEN
assert "cv.Optional(CONF_ENABLE_SELF_CLEANING, default=False)" in CODEGEN
assert 'enable_self_cleaning: "true"' in CONFIG
assert "temperature_sensor_id" not in CONFIG
assert "temperature_sensor_entity_id" not in CONFIG
assert re.search(
    r"platform: internal_temperature\n\s+name: ESP Temperature\n\s+entity_category: diagnostic",
    CONFIG,
)
assert re.search(r"debug:\n\s+update_interval: 60s", CONFIG)
assert re.search(
    r"platform: wifi_signal\n\s+name: WiFi Signal\n\s+update_interval: 60s\n\s+entity_category: diagnostic",
    CONFIG,
)
assert re.search(
    r"platform: debug\n\s+reset_reason:\n\s+name: Reset Reason\n\s+entity_category: diagnostic",
    CONFIG,
)
assert "SWITCH_ALWAYS_ON" in HEADER
assert re.search(
    r"internal_thermistor:\n\s+name: Internal Thermistor\n\s+internal: true",
    CONFIG,
)
assert "name: WiFi LED" not in CONFIG

print("Toshiba mappings are consistent")
