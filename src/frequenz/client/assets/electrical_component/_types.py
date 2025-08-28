# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Electrical component types."""

from typing import TypeAlias

from ._battery import BatteryTypes
from ._ev_charger import EvChargerTypes
from ._grid_connection_point import GridConnectionPoint
from ._inverter import InverterTypes
from ._power_transformer import PowerTransformer

ElectricalComponentType: TypeAlias = (
    BatteryTypes
    | InverterTypes
    | PowerTransformer
    | EvChargerTypes
    | GridConnectionPoint
)
"""The type of the electrical component."""
