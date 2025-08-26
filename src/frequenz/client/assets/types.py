# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Type definitions for the Assets API client.

This module contains the core data types used by the Assets API client,
including data classes for representing assets, microgrids, and related entities.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from frequenz.api.common.v1alpha8.grid.delivery_area_pb2 import (
    DeliveryArea as PBDeliveryArea,
)
from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    ElectricalComponent as PBElectricalComponent,
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

from frequenz.client.assets.enums import (
    BatteryType,
    EvChargerType,
    InverterType,
    Metric,
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
