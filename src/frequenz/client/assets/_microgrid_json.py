# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""JSON encoder for Microgrid objects."""

import json
from dataclasses import asdict
from typing import Any

from ._delivery_area import EnergyMarketCodeType
from ._microgrid import Microgrid, MicrogridStatus


class MicrogridJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for Microgrid objects."""

    def default(self, o: Any) -> Any:
        """Convert Microgrid objects to JSON-serializable format."""
        if isinstance(o, Microgrid):
            return self._serialize_microgrid(o)
        # Let the base class handle other types
        return super().default(o)

    def _serialize_microgrid(self, microgrid: Microgrid) -> dict[str, Any]:
        """Serialize a Microgrid to a dictionary."""
        microgrid_dict = asdict(microgrid)
        microgrid_dict["id"] = str(microgrid.id)
        microgrid_dict["enterprise_id"] = str(microgrid.enterprise_id)
        microgrid_dict["create_timestamp"] = microgrid.create_timestamp.isoformat()

        microgrid_dict["status"] = (
            microgrid.status.name
            if isinstance(microgrid.status, MicrogridStatus)
            else microgrid.status
        )

        if microgrid.delivery_area:
            microgrid_dict["delivery_area"] = {
                "code": microgrid.delivery_area.code,
                "code_type": (
                    microgrid.delivery_area.code_type.name
                    if isinstance(
                        microgrid.delivery_area.code_type, EnergyMarketCodeType
                    )
                    else str(microgrid.delivery_area.code_type)
                ),
            }

        return microgrid_dict


def microgrid_to_json(microgrid: Microgrid) -> str:
    """Convert a Microgrid object to a JSON string."""
    return json.dumps(microgrid, cls=MicrogridJSONEncoder, indent=2)
