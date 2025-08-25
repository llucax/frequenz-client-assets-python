"""Utility functions for the CLI."""

import json
from dataclasses import asdict

import asyncclick as click

from frequenz.client.assets.types import ElectricalComponent, Microgrid


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
    """Print electrical components to console in JSON format."""
    electrical_components_dict = []
    for component in electrical_components:
        component_dict = asdict(component)
        # Convert non-serializable objects to serializable formats
        component_dict["id"] = int(component.id)
        component_dict["microgrid_id"] = int(component.microgrid_id)
        component_dict["category"] = component.category.value

        # Handle category_specific_info serialization
        if component.category_specific_info:
            if hasattr(component.category_specific_info, "type"):
                component_dict["category_specific_info"][
                    "type"
                ] = component.category_specific_info.type.value

        electrical_components_dict.append(component_dict)

    click.echo(json.dumps(electrical_components_dict, indent=2))
