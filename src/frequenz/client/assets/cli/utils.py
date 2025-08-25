"""Utility functions for the CLI."""

import json
from dataclasses import asdict
from typing import Any

import asyncclick as click

from frequenz.client.assets.types import (
    Battery,
    ElectricalComponent,
    EvCharger,
    GridConnectionPoint,
    Inverter,
    Microgrid,
    PowerTransformer,
)


class ElectricalComponentJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for ElectricalComponent objects."""

    def default(self, o: Any) -> Any:
        """Convert ElectricalComponent objects to JSON-serializable format."""
        if isinstance(o, ElectricalComponent):
            return self._serialize_electrical_component(o)
        # Let the base class handle other types
        return super().default(o)

    def _serialize_electrical_component(
        self, component: ElectricalComponent
    ) -> dict[str, Any]:
        """Serialize an ElectricalComponent to a dictionary."""
        result = {
            "id": str(component.id),
            "microgrid_id": str(component.microgrid_id),
            "name": component.name,
            "category": component.category.name,
            "manufacturer": component.manufacturer,
            "model_name": component.model_name,
        }

        # Handle category_specific_info
        if component.category_specific_info:
            result["category_specific_info"] = self._serialize_category_specific_info(
                component.category_specific_info
            )

        return result

    def _serialize_category_specific_info(self, info: Any) -> dict[str, Any]:
        """Serialize category specific info based on its type."""
        if isinstance(info, Battery):
            return {"type": info.type.name}
        elif isinstance(info, EvCharger):
            return {"type": info.type.name}
        elif isinstance(info, GridConnectionPoint):
            return {"rated_fuse_current": info.rated_fuse_current}
        elif isinstance(info, Inverter):
            return {"type": info.type.name}
        elif isinstance(info, PowerTransformer):
            return {"primary": info.primary, "secondary": info.secondary}
        else:
            # Fallback to default serialization
            return asdict(info)


def print_microgrid_details(microgrid: Microgrid) -> None:
    """
    Print microgrid details to console in JSON format.

    This function converts the Microgrid instance to a dictionary and
    outputs it as formatted JSON to the console. The output is designed
    to be machine-readable and can be piped to tools like jq for further
    processing.

    Args:
        microgrid: The Microgrid instance to print to console.
    """
    microgrid_dict = asdict(microgrid)
    microgrid_dict["id"] = int(microgrid.id)
    microgrid_dict["enterprise_id"] = int(microgrid.enterprise_id)
    microgrid_dict["create_time"] = microgrid.create_time.isoformat()

    click.echo(json.dumps(microgrid_dict, indent=2))


def print_electrical_components(
    electrical_components: list[ElectricalComponent],
) -> None:
    """Print electrical components to console in JSON format using custom encoder."""
    click.echo(
        json.dumps(
            electrical_components,
            cls=ElectricalComponentJSONEncoder,
            indent=2,
        )
    )
