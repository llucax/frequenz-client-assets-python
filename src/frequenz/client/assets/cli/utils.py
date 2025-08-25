"""Utility functions for the CLI."""

import json
from dataclasses import asdict

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
        component_dict["id"] = str(component.id)
        component_dict["microgrid_id"] = str(component.microgrid_id)
        component_dict["category"] = component.category.name

        # Handle category_specific_info serialization
        if component.category_specific_info:
            if isinstance(component.category_specific_info, Battery):
                component_dict["category_specific_info"] = {
                    "type": component.category_specific_info.type.name,
                }
            elif isinstance(component.category_specific_info, EvCharger):
                component_dict["category_specific_info"] = {
                    "type": component.category_specific_info.type.name,
                }
            elif isinstance(component.category_specific_info, GridConnectionPoint):
                component_dict["category_specific_info"] = {
                    "rated_fuse_current": component.category_specific_info.rated_fuse_current,
                }
            elif isinstance(component.category_specific_info, Inverter):
                component_dict["category_specific_info"] = {
                    "type": component.category_specific_info.type.name,
                }
            elif isinstance(component.category_specific_info, PowerTransformer):
                component_dict["category_specific_info"] = {
                    "primary": component.category_specific_info.primary,
                    "secondary": component.category_specific_info.secondary,
                }

        electrical_components_dict.append(component_dict)

    click.echo(json.dumps(electrical_components_dict, indent=2))
