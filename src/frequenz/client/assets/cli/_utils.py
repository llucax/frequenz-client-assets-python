"""Utility functions for the CLI."""

import json

# from dataclasses import asdict
from typing import Any

import asyncclick as click

from frequenz.client.assets._microgrid import Microgrid
from frequenz.client.assets._microgrid_json import microgrid_to_json
from frequenz.client.assets.electrical_component._electrical_component import (
    ElectricalComponent,
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
        # print(asdict(component))
        return {}


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
