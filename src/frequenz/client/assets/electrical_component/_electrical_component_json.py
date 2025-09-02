# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""JSON encoder for ElectricalComponent objects."""

import json
from dataclasses import asdict

from .._utils import AssetsJSONEncoder
from ._electrical_component import ElectricalComponent


def electrical_components_to_json(
    electrical_components: list[ElectricalComponent],
) -> str:
    """Convert a list of ElectricalComponent objects to a JSON string."""
    component_list = []

    for component in electrical_components:
        data = asdict(component)

        if "rated_bounds" in data and data["rated_bounds"]:
            data["rated_bounds"] = {
                key.value if hasattr(key, "value") else str(key): value
                for key, value in data["rated_bounds"].items()
            }

        component_list.append(data)

    return json.dumps(component_list, cls=AssetsJSONEncoder, indent=2)
