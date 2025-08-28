# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""JSON encoder for ElectricalComponent objects."""

import enum
import json
from dataclasses import asdict
from typing import Any, assert_never

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

        match component.category:
            case int():
                data["category"] = component.category
            case enum.Enum() as e:
                data["category"] = e.name
            case unexpected_category:
                assert_never(unexpected_category)

        if component_type := getattr(component, "type", None):
            match component_type:
                case int():
                    data["type"] = component_type
                case enum.Enum() as e:
                    data["type"] = e.name
                case unexpected_type:
                    assert_never(unexpected_type)

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
