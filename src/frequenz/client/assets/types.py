# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Type definitions for the Assets API client.

This module contains the core data types used by the Assets API client,
including data classes for representing assets, microgrids, and related entities.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

from frequenz.api.common.v1alpha8.grid.delivery_area_pb2 import (
    DeliveryArea as PBDeliveryArea,
)
from frequenz.api.common.v1alpha8.metrics.metrics_pb2 import Metric as PBMetric
from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    BatteryType as PBBatteryType,
)
from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    ElectricalComponent as PBElectricalComponent,
)
from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    EvChargerType as PBEvChargerType,
)
from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    InverterType as PBInverterType,
)
from frequenz.api.common.v1alpha8.microgrid.microgrid_pb2 import (
    Microgrid as PBMicrogrid,
)
from frequenz.api.common.v1alpha8.types.location_pb2 import Location as PBLocation
from frequenz.client.common import enum_proto
from frequenz.client.common.microgrid import EnterpriseId, MicrogridId
from frequenz.client.common.microgrid.electrical_components import (
    ElectricalComponentCategory,
    ElectricalComponentId,
)


@dataclass(frozen=True)
class DeliveryArea:
    """A wrapper class for the protobuf DeliveryArea message.

    A delivery area is a geographical area that is served by a microgrid.
    """

    code: str
    code_type: str

    @staticmethod
    def from_protobuf(pb: PBDeliveryArea) -> "DeliveryArea":
        """
        Create a DeliveryArea instance from a protobuf message.

        Args:
            pb: The protobuf DeliveryArea message.

        Returns:
            A new DeliveryArea instance populated with data from the protobuf message.
        """
        return DeliveryArea(
            code=pb.code,
            code_type=str(pb.code_type),
        )


@dataclass(frozen=True)
class Location:
    """A wrapper class for the protobuf Location message.

    A location is a geographical location that is served by a microgrid.
    """

    latitude: float
    longitude: float
    country_code: str | None

    @staticmethod
    def from_protobuf(pb: PBLocation) -> "Location":
        """Create a Location instance from a protobuf message.

        Args:
            pb: The protobuf Location message.

        Returns:
            A new Location instance populated with data from the protobuf message.
        """
        return Location(
            latitude=pb.latitude,
            longitude=pb.longitude,
            country_code=pb.country_code,
        )


@dataclass(frozen=True)
class Microgrid:
    """A wrapper class for the protobuf Microgrid message.

    A microgrid is a localized group of electricity sources and loads that normally
    operates connected to and synchronous with the traditional wide area electrical
    grid (macrogrid), but is able to disconnect from the grid and operate autonomously.
    """

    id: MicrogridId
    """Unique identifier for the microgrid."""

    enterprise_id: EnterpriseId
    """ID of the enterprise that owns this microgrid."""

    name: str
    """Human-readable name for the microgrid."""

    delivery_area: DeliveryArea | None
    """Delivery area served by the microgrid, if applicable."""

    location: Location | None
    """Geographical location of the microgrid, if applicable."""

    status: int
    """Current operational status of the microgrid, represented as an integer."""

    create_time: datetime
    """Timestamp when the microgrid was created, in UTC."""

    @staticmethod
    def from_protobuf(pb: PBMicrogrid) -> "Microgrid":
        """Create a Microgrid instance from a protobuf message.

        Args:
            pb: The protobuf Microgrid message.

        Returns:
            A new Microgrid instance populated with data from the protobuf message.
        """
        delivery_area: DeliveryArea | None = None
        if pb.HasField("delivery_area"):
            delivery_area = DeliveryArea.from_protobuf(pb.delivery_area)

        location: Location | None = None
        if pb.HasField("location"):
            location = Location.from_protobuf(pb.location)

        return Microgrid(
            id=MicrogridId(pb.id),
            enterprise_id=EnterpriseId(pb.enterprise_id),
            name=pb.name,
            delivery_area=delivery_area,
            location=location,
            status=pb.status,
            create_time=pb.create_timestamp.ToDatetime().replace(tzinfo=timezone.utc),
        )


class BatteryType(Enum):
    """Enum representing the type of battery."""

    UNSPECIFIED = PBBatteryType.BATTERY_TYPE_UNSPECIFIED
    """Unspecified type of battery."""

    LI_ION = PBBatteryType.BATTERY_TYPE_LI_ION
    """Lithium-ion battery."""

    NA_ION = PBBatteryType.BATTERY_TYPE_NA_ION
    """Sodium-ion battery."""


@dataclass(frozen=True)
class Battery:
    """A wrapper class for the protobuf Battery message."""

    type: BatteryType
    """The type of battery."""


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


@dataclass(frozen=True)
class EvCharger:
    """A wrapper class for the protobuf EvCharger message."""

    type: EvChargerType
    """The type of EV charger."""


@dataclass(frozen=True)
class GridConnectionPoint:
    """A wrapper class for the protobuf GridConnectionPoint message."""

    rated_fuse_current: int
    """The rated fuse current of the grid connection point."""


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


@dataclass(frozen=True)
class Inverter:
    """A wrapper class for the protobuf Inverter message."""

    type: InverterType
    """The type of inverter."""


@dataclass(frozen=True)
class PowerTransformer:
    """A wrapper class for the protobuf PowerTransformer message."""

    primary: float
    """The primary of the power transformer."""

    secondary: float
    """The secondary of the power transformer."""


ElectricalComponentCategorySpecificInfo = (
    Battery | EvCharger | GridConnectionPoint | Inverter | PowerTransformer
)


@dataclass(frozen=True)
class Lifetime:
    """A wrapper class for the protobuf Lifetime message."""

    start_time: datetime
    """The start time of the operational lifetime."""

    end_time: datetime
    """The end time of the operational lifetime."""


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


@dataclass(frozen=True)
class ElectricalComponent:
    """A wrapper class for the protobuf ElectricalComponent message.

    An electrical component is a physical device that can be used to generate or consume
    electricity.
    """

    id: ElectricalComponentId
    """Unique identifier for the electrical component."""

    microgrid_id: MicrogridId
    """Unique identifier for the microgrid that the electrical component belongs to."""

    name: str
    """Human-readable name for the electrical component."""

    category: ElectricalComponentCategory
    """The component category. E.g., Inverter, Battery, etc."""

    category_specific_info: ElectricalComponentCategorySpecificInfo | None
    """Category-specific information for the electrical component."""

    manufacturer: str
    """The manufacturer of the electrical component."""

    model_name: str
    """The model name of the electrical component."""

    operational_lifetime: str | None
    """The operational lifetime of the electrical component."""

    @staticmethod
    def from_protobuf(pb: PBElectricalComponent) -> "ElectricalComponent":
        """Create a ElectricalComponent instance from a protobuf message."""
        category_specific_info: ElectricalComponentCategorySpecificInfo | None = None
        if pb.HasField("category_specific_info"):
            if pb.category_specific_info.WhichOneof("kind") == "battery":
                category_specific_info = Battery(
                    type=enum_proto.enum_from_proto(
                        pb.category_specific_info.battery.type,
                        BatteryType,
                        allow_invalid=False,
                    )
                )
            elif pb.category_specific_info.WhichOneof("kind") == "ev_charger":
                category_specific_info = EvCharger(
                    type=enum_proto.enum_from_proto(
                        pb.category_specific_info.ev_charger.type,
                        EvChargerType,
                        allow_invalid=False,
                    )
                )
            elif pb.category_specific_info.WhichOneof("kind") == "inverter":
                category_specific_info = Inverter(
                    type=enum_proto.enum_from_proto(
                        pb.category_specific_info.inverter.type,
                        InverterType,
                        allow_invalid=False,
                    )
                )
            elif pb.category_specific_info.WhichOneof("kind") == "power_transformer":
                category_specific_info = PowerTransformer(
                    primary=pb.category_specific_info.power_transformer.primary,
                    secondary=pb.category_specific_info.power_transformer.secondary,
                )
            elif (
                pb.category_specific_info.WhichOneof("kind") == "grid_connection_point"
            ):
                grid_connection_point = pb.category_specific_info.grid_connection_point
                category_specific_info = GridConnectionPoint(
                    rated_fuse_current=grid_connection_point.rated_fuse_current,
                )

        operational_lifetime: Lifetime | None = None
        if pb.HasField("operational_lifetime"):
            operational_lifetime = Lifetime(
                start_time=pb.operational_lifetime.start_timestamp.ToDatetime().replace(
                    tzinfo=timezone.utc
                ),
                end_time=pb.operational_lifetime.end_timestamp.ToDatetime().replace(
                    tzinfo=timezone.utc
                ),
            )

        return ElectricalComponent(
            id=ElectricalComponentId(pb.id),
            microgrid_id=MicrogridId(pb.microgrid_id),
            name=pb.name,
            category=ElectricalComponentCategory(pb.category),
            category_specific_info=category_specific_info,
            manufacturer=pb.manufacturer,
            model_name=pb.model_name,
            operational_lifetime=operational_lifetime,
        )
