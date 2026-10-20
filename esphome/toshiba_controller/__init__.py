import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor, climate, select, sensor, uart
from esphome.const import CONF_ID

CODEOWNERS = []
DEPENDENCIES = ["uart"]
AUTO_LOAD = ["binary_sensor", "climate", "sensor", "switch", "select"]

toshiba_controller_ns = cg.esphome_ns
ToshibaController = toshiba_controller_ns.class_(
    "ToshibaController", climate.Climate, cg.Component
)

CONF_TEMPERATURE_SENSOR_ID = "temperature_sensor_id"
CONF_SPECIAL_MODE_SELECT_ID = "special_mode_select_id"
CONF_SWING_MODE_SELECT_ID = "swing_mode_select_id"
CONF_POWER_SELECT_ID = "power_select_id"
CONF_SMART_THERMOSTAT_MULTIPLIER = "smart_thermostat_multiplier"
CONF_SMART_THERMOSTAT_RUNAWAY_PROTECTION = "smart_thermostat_runaway_protection"
CONF_DISABLE_COOLING_MODES = "disable_cooling_modes"
CONF_ENABLE_SELF_CLEANING = "enable_self_cleaning"

CONFIG_SCHEMA = (
    climate.climate_schema(ToshibaController)
    .extend(
        {
            cv.Required("uart_id"): cv.use_id(uart.UARTComponent),
            cv.Optional(CONF_TEMPERATURE_SENSOR_ID): cv.use_id(sensor.Sensor),
            cv.Required(CONF_SPECIAL_MODE_SELECT_ID): cv.use_id(select.Select),
            cv.Required(CONF_SWING_MODE_SELECT_ID): cv.use_id(select.Select),
            cv.Required(CONF_POWER_SELECT_ID): cv.use_id(select.Select),
            cv.Optional(CONF_SMART_THERMOSTAT_MULTIPLIER, default=3.0): cv.float_range(
                min=1.0, max=10.0
            ),
            cv.Optional(
                CONF_SMART_THERMOSTAT_RUNAWAY_PROTECTION, default=True
            ): cv.boolean,
            cv.Optional(CONF_DISABLE_COOLING_MODES, default=False): cv.boolean,
            cv.Optional(CONF_ENABLE_SELF_CLEANING, default=False): cv.boolean,
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await climate.register_climate(var, config)

    uart_comp = await cg.get_variable(config["uart_id"])
    cg.add(var.set_uart(uart_comp))

    if CONF_TEMPERATURE_SENSOR_ID in config:
        temp_sensor = await cg.get_variable(config[CONF_TEMPERATURE_SENSOR_ID])
        cg.add(var.set_temperature_sensor(temp_sensor))

    special = await cg.get_variable(config[CONF_SPECIAL_MODE_SELECT_ID])
    cg.add(var.set_special_mode_select(special))

    swing = await cg.get_variable(config[CONF_SWING_MODE_SELECT_ID])
    cg.add(var.set_swing_mode_select(swing))

    power = await cg.get_variable(config[CONF_POWER_SELECT_ID])
    cg.add(var.set_power_select(power))

    cg.add(
        var.set_smart_thermostat_multiplier(
            config[CONF_SMART_THERMOSTAT_MULTIPLIER]
        )
    )
    cg.add(
        var.set_smart_thermostat_runaway_protection(
            config[CONF_SMART_THERMOSTAT_RUNAWAY_PROTECTION]
        )
    )
    cg.add(var.set_disable_cooling_modes(config[CONF_DISABLE_COOLING_MODES]))
    cg.add(var.set_enable_self_cleaning(config[CONF_ENABLE_SELF_CLEANING]))
