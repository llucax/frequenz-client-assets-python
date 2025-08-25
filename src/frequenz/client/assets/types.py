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

    category_specific_info: ElectricalComponentCategorySpecificInfo
    """Category-specific information for the electrical component."""

    manufacturer: str
    """The manufacturer of the electrical component."""

    model_name: str
    """The model name of the electrical component."""

    @staticmethod
    def from_protobuf(pb: PBElectricalComponent) -> "ElectricalComponent":
        """Create a ElectricalComponent instance from a protobuf message."""
        return ElectricalComponent(
            id=ElectricalComponentId(pb.id),
            microgrid_id=MicrogridId(pb.microgrid_id),
            name=pb.name,
            category=ElectricalComponentCategory.UNSPECIFIED,
            category_specific_info=Battery(type=BatteryType.UNSPECIFIED),
            manufacturer=pb.manufacturer,
            model_name=pb.model_name,
        )
