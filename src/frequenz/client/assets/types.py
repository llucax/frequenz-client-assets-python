# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Type definitions for the Assets API client.

This module contains the core data types used by the Assets API client,
including data classes for representing assets, microgrids, and related entities.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    ElectricalComponent as PBElectricalComponent,
)
from frequenz.client.common import enum_proto
from frequenz.client.common.microgrid import MicrogridId
from frequenz.client.common.microgrid.electrical_components import (
    ElectricalComponentCategory,
    ElectricalComponentId,
)

from frequenz.client.assets.enums import (
    BatteryType,
    EvChargerType,
    InverterType,
    Metric,
)


@dataclass(frozen=True)
class Battery:
    """A wrapper class for the protobuf Battery message."""

    type: BatteryType
    """The type of battery."""


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


@dataclass(frozen=True)
class Bound:
    """A wrapper class for the protobuf Bound message."""

    lower: float | None
    """The lower bound of the bound."""

    upper: float | None
    """The upper bound of the bound."""


@dataclass(frozen=True)
class MetricConfigBounds:
    """A wrapper class for the protobuf MetricConfigBounds message."""

    metric: Metric
    """The metric."""

    config_bounds: Bound | None
    """The config bounds of the metric."""


@dataclass(frozen=True)
class ElectricalComponent:  # pylint: disable=too-many-instance-attributes
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

    operational_lifetime: Lifetime | None
    """The operational lifetime of the electrical component."""

    metric_config_bounds: list[MetricConfigBounds]
    """The metric config bounds of the electrical component."""

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

        metric_config_bounds: list[MetricConfigBounds] = [
            MetricConfigBounds(
                metric=enum_proto.enum_from_proto(
                    pb_metric_config_bounds.metric, Metric, allow_invalid=False
                ),
                config_bounds=Bound(
                    lower=pb_metric_config_bounds.config_bounds.lower,
                    upper=pb_metric_config_bounds.config_bounds.upper,
                ),
            )
            for pb_metric_config_bounds in pb.metric_config_bounds
        ]

        return ElectricalComponent(
            id=ElectricalComponentId(pb.id),
            microgrid_id=MicrogridId(pb.microgrid_id),
            name=pb.name,
            category=ElectricalComponentCategory(pb.category),
            category_specific_info=category_specific_info,
            manufacturer=pb.manufacturer,
            model_name=pb.model_name,
            operational_lifetime=operational_lifetime,
            metric_config_bounds=metric_config_bounds,
        )
