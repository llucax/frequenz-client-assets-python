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
from typing import final

from frequenz.api.common.v1alpha8.grid.delivery_area_pb2 import (
    DeliveryArea as PBDeliveryArea,
)
from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    ElectricalComponentCategory as PBComponentCategory,
)
from frequenz.api.common.v1alpha8.microgrid.microgrid_pb2 import (
    Microgrid as PBMicrogrid,
)
from frequenz.api.common.v1alpha8.types.location_pb2 import Location as PBLocation
from frequenz.client.common.microgrid import EnterpriseId, MicrogridId
from frequenz.core.id import BaseId


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


@final
class ElectricalComponentId(BaseId, str_prefix="ECID"):
    """A unique identifier for an electrical component."""


class ElectricalComponentCategory(Enum):
    """Enumeration of electrical component categories."""

    UNSPECIFIED = PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_UNSPECIFIED
    """Unspecified component category."""

    GRID_CONNECTION_POINT = (
        PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_GRID_CONNECTION_POINT
    )
    """A grid connection point electrical component."""

    METER = PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_METER
    """A meter electrical component."""

    INVERTER = PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_INVERTER
    """An inverter electrical component."""

    CONVERTER = PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_CONVERTER
    """A converter electrical component."""

    BATTERY = PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_BATTERY
    """A battery electrical component."""

    EV_CHARGER = PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_EV_CHARGER
    """An electric vehicle charger electrical component."""

    BREAKER = PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_BREAKER
    """A breaker electrical component."""

    PRECHARGER = PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_PRECHARGER
    """A precharger electrical component."""

    CHP = PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_CHP
    """A combined heat and power unit electrical component."""

    ELECTROLYZER = PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_ELECTROLYZER
    """An electrolyzer electrical component."""

    POWER_TRANSFORMER = (
        PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_POWER_TRANSFORMER
    )
    """A power transformer electrical component."""

    HVAC = PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_HVAC
    """An HVAC system electrical component."""

    PLC = PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_PLC
    """A programmable logic controller electrical component."""

    CRYPTO_MINER = PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_CRYPTO_MINER
    """A crypto miner electrical component."""

    STATIC_TRANSFER_SWITCH = (
        PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_STATIC_TRANSFER_SWITCH
    )
    """A static transfer switch electrical component."""

    UNINTERRUPTIBLE_POWER_SUPPLY = (
        PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_UNINTERRUPTIBLE_POWER_SUPPLY
    )
    """An uninterruptible power supply electrical component."""

    CAPACITOR_BANK = PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_CAPACITOR_BANK
    """A capacitor bank electrical component."""

    WIND_TURBINE = PBComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_WIND_TURBINE
    """A wind turbine electrical component."""


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

    manufacturer: str
    """The manufacturer of the electrical component."""

    model_name: str
    """The model name of the electrical component."""
