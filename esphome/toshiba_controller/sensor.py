import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    DEVICE_CLASS_TEMPERATURE,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
)

from . import ToshibaController

CONF_TOSHIBA_CONTROLLER_ID = "toshiba_controller_id"

TEMP_SENSOR_SCHEMA = sensor.sensor_schema(
    unit_of_measurement=UNIT_CELSIUS,
    icon="mdi:thermometer",
    device_class=DEVICE_CLASS_TEMPERATURE,
    state_class=STATE_CLASS_MEASUREMENT,
    accuracy_decimals=0,
)

SENSOR_KEYS = {
    "outdoor_temperature": {
        "setter": "set_outdoor_temperature_sensor",
        "schema": sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            icon="mdi:home-thermometer-outline",
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
            accuracy_decimals=0,
        ),
    },
    "fcu_air_temp": {"setter": "set_fcu_air_temp_sensor", "schema": TEMP_SENSOR_SCHEMA},
    "fcu_setpoint": {"setter": "set_fcu_setpoint_sensor", "schema": TEMP_SENSOR_SCHEMA},
    "fcu_tc_temp": {"setter": "set_fcu_tc_temp_sensor", "schema": TEMP_SENSOR_SCHEMA},
    "fcu_tcj_temp": {"setter": "set_fcu_tcj_temp_sensor", "schema": TEMP_SENSOR_SCHEMA},
    "fcu_fan_rpm": {
        "setter": "set_fcu_fan_rpm_sensor",
        "schema": sensor.sensor_schema(
            unit_of_measurement="rpm",
            icon="mdi:fan",
            state_class=STATE_CLASS_MEASUREMENT,
            accuracy_decimals=0,
        ),
    },
    "cdu_td_temp": {"setter": "set_cdu_td_temp_sensor", "schema": TEMP_SENSOR_SCHEMA},
    "cdu_ts_temp": {"setter": "set_cdu_ts_temp_sensor", "schema": TEMP_SENSOR_SCHEMA},
    "cdu_te_temp": {"setter": "set_cdu_te_temp_sensor", "schema": TEMP_SENSOR_SCHEMA},
    "cdu_load": {
        "setter": "set_cdu_load_sensor",
        "schema": sensor.sensor_schema(
            unit_of_measurement="%",
            icon="mdi:heat-pump-outline",
            state_class=STATE_CLASS_MEASUREMENT,
            accuracy_decimals=0,
        ),
    },
    "cdu_iac": {
        "setter": "set_cdu_iac_sensor",
        "schema": sensor.sensor_schema(
            state_class=STATE_CLASS_MEASUREMENT,
            accuracy_decimals=0,
        ),
    },
    "smart_thermostat_offset": {
        "setter": "set_smart_thermostat_offset_sensor",
        "schema": sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            icon="mdi:thermometer-lines",
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
            accuracy_decimals=2,
        ),
    },
}

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_TOSHIBA_CONTROLLER_ID): cv.use_id(ToshibaController),
        **{cv.Optional(key): info["schema"] for key, info in SENSOR_KEYS.items()},
    }
)


async def to_code(config):
    hub = await cg.get_variable(config[CONF_TOSHIBA_CONTROLLER_ID])
    for key, info in SENSOR_KEYS.items():
        if key in config:
            sens = await sensor.new_sensor(config[key])
            cg.add(getattr(hub, info["setter"])(sens))
