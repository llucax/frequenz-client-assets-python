# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""JSON encoder for ElectricalComponent objects."""

import enum
import json
from dataclasses import asdict
from typing import Any

from .._lifetime import Lifetime
from ._electrical_component import ElectricalComponent


class ElectricalComponentJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for ElectricalComponent objects."""

    def default(self, o: Any) -> Any:
        """Convert supported objects to JSON-serializable format."""
        if isinstance(o, ElectricalComponent):
            return self._serialize_electrical_component(o)
        if isinstance(o, Lifetime):
            return self._serialize_lifetime(o)
        # Let the base class handle other types
        return super().default(o)

    def _serialize_electrical_component(
        self, component: ElectricalComponent
    ) -> dict[str, Any]:
        """Serialize an ElectricalComponent to a dictionary.

        - IDs are stringified.
        - Enums (category/type) are converted to their names; unrecognized ints are kept.
        - Lifetime timestamps are serialized as ISO-8601 strings.
        """
        data = asdict(component)

        data["id"] = str(component.id)
        data["microgrid_id"] = str(component.microgrid_id)
        data["operational_lifetime"] = self._serialize_lifetime(
            component.operational_lifetime
        )

        if "rated_bounds" in data and data["rated_bounds"]:
            data["rated_bounds"] = {
                key.name if isinstance(key, enum.Enum) else str(key): value
                for key, value in data["rated_bounds"].items()
            }

        if "category" in data and data["category"]:
            data["category"] = (
                data["category"].name
                if isinstance(data["category"], enum.Enum)
                else data["category"]
            )

        if "type" in data and data["type"]:
            data["type"] = (
                data["type"].name
                if isinstance(data["type"], enum.Enum)
                else data["type"]
            )

        return data

    @staticmethod
    def _serialize_lifetime(lifetime: Lifetime) -> dict[str, Any]:
        """Serialize Lifetime to a JSON-friendly dict."""
        return {
            "start": lifetime.start.isoformat() if lifetime.start else None,
            "end": lifetime.end.isoformat() if lifetime.end else None,
        }


def electrical_components_to_json(
    electrical_components: list[ElectricalComponent],
) -> str:
    """Convert a list of ElectricalComponent objects to a JSON string."""
    return json.dumps(
        electrical_components, cls=ElectricalComponentJSONEncoder, indent=2
    )
