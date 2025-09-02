# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Utility functions for the Assets API client."""

import enum
import json
from datetime import datetime, timezone
from typing import Any

from frequenz.core.id import BaseId


class AssetsJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for assets-related objects.

    Handles common types used in the assets package:
    - BaseId objects → integers
    - Enum objects → their values
    - Datetime objects → UTC ISO format strings
    """

    def default(self, o: Any) -> Any:
        """Convert supported objects to JSON-serializable format."""
        if isinstance(o, BaseId):
            return int(o)

        if isinstance(o, enum.Enum):
            return o.value

        if isinstance(o, datetime):
            if o.tzinfo is None:
                o = o.replace(tzinfo=timezone.utc)
            else:
                o = o.astimezone(timezone.utc)
            return o.isoformat()

        return super().default(o)
