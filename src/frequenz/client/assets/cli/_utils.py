"""Utility functions for the CLI."""

import json
from dataclasses import asdict
from typing import Any

import asyncclick as click

from frequenz.client.assets._microgrid import Microgrid
from frequenz.client.assets._microgrid_json import microgrid_to_json
from frequenz.client.assets.types import (
    Battery,
    ElectricalComponent,
    EvCharger,
    GridConnectionPoint,
    Inverter,
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
        result: dict[str, Any] = {
            "id": str(component.id),
            "microgrid_id": str(component.microgrid_id),
            "name": component.name,
            "category": component.category.name,
            "manufacturer": component.manufacturer,
            "model_name": component.model_name,
            "metric_config_bounds": [
                {
                    "metric": metric_config_bound.metric.name,
                    "config_bounds": {
                        "lower": (
                            metric_config_bound.config_bounds.lower
                            if metric_config_bound.config_bounds
                            else None
                        ),
                        "upper": (
                            metric_config_bound.config_bounds.upper
                            if metric_config_bound.config_bounds
                            else None
                        ),
                    },
                }
                for metric_config_bound in component.metric_config_bounds
            ],
        }

        # Handle category_specific_info
        if component.category_specific_info:
            result["category_specific_info"] = self._serialize_category_specific_info(
                component.category_specific_info
            )

        if component.operational_lifetime:
            result["operational_lifetime"] = {
                "start_time": component.operational_lifetime.start_time.isoformat(),
                "end_time": component.operational_lifetime.end_time.isoformat(),
            }

        return result

    def _serialize_category_specific_info(self, info: Any) -> dict[str, Any]:
        """Serialize category specific info based on its type."""
        if isinstance(info, Battery):
            return {"type": info.type.name}
        if isinstance(info, EvCharger):
            return {"type": info.type.name}
        if isinstance(info, GridConnectionPoint):
            return {"rated_fuse_current": info.rated_fuse_current}
        if isinstance(info, Inverter):
            return {"type": info.type.name}
        if isinstance(info, PowerTransformer):
            return {"primary": info.primary, "secondary": info.secondary}

        # Fallback to default serialization
        return asdict(info)


def print_microgrid_details(microgrid: Microgrid) -> None:
    """
    Print microgrid details to console in JSON format using custom encoder.

    This function converts the Microgrid instance to JSON using a custom
    encoder and outputs it as formatted JSON to the console. The output is
    designed to be machine-readable and can be piped to tools like jq for
    further processing.

    Args:
        microgrid: The Microgrid instance to print to console.
    """
    click.echo(microgrid_to_json(microgrid))


def print_electrical_components(
    electrical_components: list[ElectricalComponent],
) -> None:
    """
    Print electrical components to console in JSON format using custom encoder.

    This function converts the ElectricalComponent instances to JSON using a custom
    encoder and outputs it as formatted JSON to the console. The output is
    designed to be machine-readable and can be piped to tools like jq for
    further processing.

    Args:
        electrical_components: The list of ElectricalComponent instances to print to console.
    """
    click.echo(
        json.dumps(
            electrical_components,
            cls=ElectricalComponentJSONEncoder,
            indent=2,
        )
    )
