import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor

from . import ToshibaController

CONF_TOSHIBA_CONTROLLER_ID = "toshiba_controller_id"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_TOSHIBA_CONTROLLER_ID): cv.use_id(ToshibaController),
        cv.Optional("smart_thermostat_runaway_active"): binary_sensor.binary_sensor_schema(
            device_class="problem",
            icon="mdi:thermostat-alert",
            entity_category="diagnostic",
        ),
    }
)


async def to_code(config):
    hub = await cg.get_variable(config[CONF_TOSHIBA_CONTROLLER_ID])
    if "smart_thermostat_runaway_active" in config:
        sens = await binary_sensor.new_binary_sensor(
            config["smart_thermostat_runaway_active"]
        )
        cg.add(hub.set_smart_thermostat_runaway_active_binary_sensor(sens))
