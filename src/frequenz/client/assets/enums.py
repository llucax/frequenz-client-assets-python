"""Enums for the assets."""

from enum import Enum

from frequenz.api.common.v1alpha8.metrics.metrics_pb2 import Metric as PBMetric
from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    BatteryType as PBBatteryType,
)
from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    EvChargerType as PBEvChargerType,
)
from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    InverterType as PBInverterType,
)


class BatteryType(Enum):
    """Enum representing the type of battery."""

    UNSPECIFIED = PBBatteryType.BATTERY_TYPE_UNSPECIFIED
    """Unspecified type of battery."""

    LI_ION = PBBatteryType.BATTERY_TYPE_LI_ION
    """Lithium-ion battery."""

    NA_ION = PBBatteryType.BATTERY_TYPE_NA_ION
    """Sodium-ion battery."""


class EvChargerType(Enum):
    """Enum representing the type of EV charger."""

    UNSPECIFIED = PBEvChargerType.EV_CHARGER_TYPE_UNSPECIFIED
    """Unspecified type of EV charger."""

    AC = PBEvChargerType.EV_CHARGER_TYPE_AC
    """The EV charging station supports AC charging only."""

    DC = PBEvChargerType.EV_CHARGER_TYPE_DC
    """The EV charging station supports DC charging only."""

    HYBRID = PBEvChargerType.EV_CHARGER_TYPE_HYBRID
    """The EV charging station supports both AC and DC."""


class InverterType(Enum):
    """Enum representing the type of inverter."""

    UNSPECIFIED = PBInverterType.INVERTER_TYPE_UNSPECIFIED
    """Unspecified type of inverter."""

    BATTERY = PBInverterType.INVERTER_TYPE_BATTERY
    """Battery inverter."""

    PV = PBInverterType.INVERTER_TYPE_PV
    """PV (photovoltaic) inverter."""

    HYBRID = PBInverterType.INVERTER_TYPE_HYBRID
    """Hybrid inverter."""


class Metric(Enum):
    """Enum representing the type of metric."""

    UNSPECIFIED = PBMetric.METRIC_UNSPECIFIED
    """Unspecified metric."""

    DC_VOLTAGE = PBMetric.METRIC_DC_VOLTAGE
    """DC voltage."""

    DC_CURRENT = PBMetric.METRIC_DC_CURRENT
    """DC current."""

    DC_POWER = PBMetric.METRIC_DC_POWER
    """DC power."""

    AC_FREQUENCY = PBMetric.METRIC_AC_FREQUENCY
    """AC frequency."""

    AC_VOLTAGE = PBMetric.METRIC_AC_VOLTAGE
    """AC voltage."""

    AC_VOLTAGE_PHASE_1_N = PBMetric.METRIC_AC_VOLTAGE_PHASE_1_N
    """AC voltage phase 1 to neutral."""

    AC_VOLTAGE_PHASE_2_N = PBMetric.METRIC_AC_VOLTAGE_PHASE_2_N
    """AC voltage phase 2 to neutral."""

    AC_VOLTAGE_PHASE_3_N = PBMetric.METRIC_AC_VOLTAGE_PHASE_3_N
    """AC voltage phase 3 to neutral."""

    AC_VOLTAGE_PHASE_1_PHASE_2 = PBMetric.METRIC_AC_VOLTAGE_PHASE_1_PHASE_2
    """AC voltage phase 1 to phase 2."""

    AC_VOLTAGE_PHASE_2_PHASE_3 = PBMetric.METRIC_AC_VOLTAGE_PHASE_2_PHASE_3
    """AC voltage phase 2 to phase 3."""

    AC_VOLTAGE_PHASE_3_PHASE_1 = PBMetric.METRIC_AC_VOLTAGE_PHASE_3_PHASE_1
    """AC voltage phase 3 to phase 1."""

    AC_CURRENT = PBMetric.METRIC_AC_CURRENT
    """AC current."""

    AC_CURRENT_PHASE_1 = PBMetric.METRIC_AC_CURRENT_PHASE_1
    """AC current phase 1."""

    AC_CURRENT_PHASE_2 = PBMetric.METRIC_AC_CURRENT_PHASE_2
    """AC current phase 2."""

    AC_CURRENT_PHASE_3 = PBMetric.METRIC_AC_CURRENT_PHASE_3
    """AC current phase 3."""

    AC_POWER_APPARENT = PBMetric.METRIC_AC_POWER_APPARENT
    """AC power apparent."""

    AC_POWER_APPARENT_PHASE_1 = PBMetric.METRIC_AC_POWER_APPARENT_PHASE_1
    """AC power apparent phase 1."""

    AC_POWER_APPARENT_PHASE_2 = PBMetric.METRIC_AC_POWER_APPARENT_PHASE_2
    """AC power apparent phase 2."""

    AC_POWER_APPARENT_PHASE_3 = PBMetric.METRIC_AC_POWER_APPARENT_PHASE_3
    """AC power apparent phase 3."""

    AC_POWER_ACTIVE = PBMetric.METRIC_AC_POWER_ACTIVE
    """AC power active."""

    AC_POWER_ACTIVE_PHASE_1 = PBMetric.METRIC_AC_POWER_ACTIVE_PHASE_1
    """AC power active phase 1."""

    AC_POWER_ACTIVE_PHASE_2 = PBMetric.METRIC_AC_POWER_ACTIVE_PHASE_2
    """AC power active phase 2."""

    AC_POWER_ACTIVE_PHASE_3 = PBMetric.METRIC_AC_POWER_ACTIVE_PHASE_3
    """AC power active phase 3."""

    AC_POWER_REACTIVE = PBMetric.METRIC_AC_POWER_REACTIVE
    """AC power reactive."""

    AC_POWER_REACTIVE_PHASE_1 = PBMetric.METRIC_AC_POWER_REACTIVE_PHASE_1
    """AC power reactive phase 1."""

    AC_POWER_REACTIVE_PHASE_2 = PBMetric.METRIC_AC_POWER_REACTIVE_PHASE_2
    """AC power reactive phase 2."""

    AC_POWER_REACTIVE_PHASE_3 = PBMetric.METRIC_AC_POWER_REACTIVE_PHASE_3
    """AC power reactive phase 3."""

    AC_POWER_FACTOR = PBMetric.METRIC_AC_POWER_FACTOR
    """AC power factor."""

    AC_POWER_FACTOR_PHASE_1 = PBMetric.METRIC_AC_POWER_FACTOR_PHASE_1
    """AC power factor phase 1."""

    AC_POWER_FACTOR_PHASE_2 = PBMetric.METRIC_AC_POWER_FACTOR_PHASE_2
    """AC power factor phase 2."""

    AC_POWER_FACTOR_PHASE_3 = PBMetric.METRIC_AC_POWER_FACTOR_PHASE_3
    """AC power factor phase 3."""

    AC_ENERGY_APPARENT = PBMetric.METRIC_AC_ENERGY_APPARENT
    """AC energy apparent."""

    AC_ENERGY_APPARENT_PHASE_1 = PBMetric.METRIC_AC_ENERGY_APPARENT_PHASE_1
    """AC energy apparent phase 1."""

    AC_ENERGY_APPARENT_PHASE_2 = PBMetric.METRIC_AC_ENERGY_APPARENT_PHASE_2
    """AC energy apparent phase 2."""

    AC_ENERGY_APPARENT_PHASE_3 = PBMetric.METRIC_AC_ENERGY_APPARENT_PHASE_3
    """AC energy apparent phase 3."""

    AC_ENERGY_ACTIVE = PBMetric.METRIC_AC_ENERGY_ACTIVE
    """AC energy active."""

    AC_ENERGY_ACTIVE_PHASE_1 = PBMetric.METRIC_AC_ENERGY_ACTIVE_PHASE_1
    """AC energy active phase 1."""

    AC_ENERGY_ACTIVE_PHASE_2 = PBMetric.METRIC_AC_ENERGY_ACTIVE_PHASE_2
    """AC energy active phase 2."""

    AC_ENERGY_ACTIVE_PHASE_3 = PBMetric.METRIC_AC_ENERGY_ACTIVE_PHASE_3
    """AC energy active phase 3."""

    AC_ENERGY_ACTIVE_CONSUMED = PBMetric.METRIC_AC_ENERGY_ACTIVE_CONSUMED
    """AC energy active consumed."""

    AC_ENERGY_ACTIVE_CONSUMED_PHASE_1 = (
        PBMetric.METRIC_AC_ENERGY_ACTIVE_CONSUMED_PHASE_1
    )
    """AC energy active consumed phase 1."""

    AC_ENERGY_ACTIVE_CONSUMED_PHASE_2 = (
        PBMetric.METRIC_AC_ENERGY_ACTIVE_CONSUMED_PHASE_2
    )
    """AC energy active consumed phase 2."""

    AC_ENERGY_ACTIVE_CONSUMED_PHASE_3 = (
        PBMetric.METRIC_AC_ENERGY_ACTIVE_CONSUMED_PHASE_3
    )
    """AC energy active consumed phase 3."""

    AC_ENERGY_ACTIVE_DELIVERED = PBMetric.METRIC_AC_ENERGY_ACTIVE_DELIVERED
    """AC energy active delivered."""

    AC_ENERGY_ACTIVE_DELIVERED_PHASE_1 = (
        PBMetric.METRIC_AC_ENERGY_ACTIVE_DELIVERED_PHASE_1
    )
    """AC energy active delivered phase 1."""

    AC_ENERGY_ACTIVE_DELIVERED_PHASE_2 = (
        PBMetric.METRIC_AC_ENERGY_ACTIVE_DELIVERED_PHASE_2
    )
    """AC energy active delivered phase 2."""

    AC_ENERGY_ACTIVE_DELIVERED_PHASE_3 = (
        PBMetric.METRIC_AC_ENERGY_ACTIVE_DELIVERED_PHASE_3
    )
    """AC energy active delivered phase 3."""

    AC_ENERGY_REACTIVE = PBMetric.METRIC_AC_ENERGY_REACTIVE
    """AC energy reactive."""

    AC_ENERGY_REACTIVE_PHASE_1 = PBMetric.METRIC_AC_ENERGY_REACTIVE_PHASE_1
    """AC energy reactive phase 1."""

    AC_ENERGY_REACTIVE_PHASE_2 = PBMetric.METRIC_AC_ENERGY_REACTIVE_PHASE_2
    """AC energy reactive phase 2."""

    AC_ENERGY_REACTIVE_PHASE_3 = PBMetric.METRIC_AC_ENERGY_REACTIVE_PHASE_3
    """AC energy reactive phase 3."""

    AC_TOTAL_HARMONIC_DISTORTION_CURRENT = (
        PBMetric.METRIC_AC_TOTAL_HARMONIC_DISTORTION_CURRENT
    )
    """AC total harmonic distortion current."""

    AC_TOTAL_HARMONIC_DISTORTION_CURRENT_PHASE_1 = (
        PBMetric.METRIC_AC_TOTAL_HARMONIC_DISTORTION_CURRENT_PHASE_1
    )
    """AC total harmonic distortion current phase 1."""

    AC_TOTAL_HARMONIC_DISTORTION_CURRENT_PHASE_2 = (
        PBMetric.METRIC_AC_TOTAL_HARMONIC_DISTORTION_CURRENT_PHASE_2
    )
    """AC total harmonic distortion current phase 2."""

    AC_TOTAL_HARMONIC_DISTORTION_CURRENT_PHASE_3 = (
        PBMetric.METRIC_AC_TOTAL_HARMONIC_DISTORTION_CURRENT_PHASE_3
    )
    """AC total harmonic distortion current phase 3."""

    BATTERY_CAPACITY = PBMetric.METRIC_BATTERY_CAPACITY
    """Battery capacity."""

    BATTERY_SOC_PCT = PBMetric.METRIC_BATTERY_SOC_PCT
    """Battery state of charge percentage."""

    BATTERY_TEMPERATURE = PBMetric.METRIC_BATTERY_TEMPERATURE
    """Battery temperature."""

    INVERTER_TEMPERATURE = PBMetric.METRIC_INVERTER_TEMPERATURE
    """Inverter temperature."""

    INVERTER_TEMPERATURE_CABINET = PBMetric.METRIC_INVERTER_TEMPERATURE_CABINET
    """Inverter temperature cabinet."""

    INVERTER_TEMPERATURE_HEATSINK = PBMetric.METRIC_INVERTER_TEMPERATURE_HEATSINK
    """Inverter temperature heatsink."""

    INVERTER_TEMPERATURE_TRANSFORMER = PBMetric.METRIC_INVERTER_TEMPERATURE_TRANSFORMER
    """Inverter temperature transformer."""

    EV_CHARGER_TEMPERATURE = PBMetric.METRIC_EV_CHARGER_TEMPERATURE
    """EV charger temperature."""

    SENSOR_WIND_SPEED = PBMetric.METRIC_SENSOR_WIND_SPEED
    """Sensor wind speed."""

    SENSOR_WIND_DIRECTION = PBMetric.METRIC_SENSOR_WIND_DIRECTION
    """Sensor wind direction."""

    SENSOR_TEMPERATURE = PBMetric.METRIC_SENSOR_TEMPERATURE
    """Sensor temperature."""

    SENSOR_RELATIVE_HUMIDITY = PBMetric.METRIC_SENSOR_RELATIVE_HUMIDITY
    """Sensor relative humidity."""

    SENSOR_DEW_POINT = PBMetric.METRIC_SENSOR_DEW_POINT
    """Sensor dew point."""

    SENSOR_AIR_PRESSURE = PBMetric.METRIC_SENSOR_AIR_PRESSURE
    """Sensor air pressure."""

    SENSOR_IRRADIANCE = PBMetric.METRIC_SENSOR_IRRADIANCE
    """Sensor irradiance."""
