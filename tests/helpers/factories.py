# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Factory functions for creating test objects."""

from typing import Any
from unittest.mock import AsyncMock, MagicMock

from frequenz.client.common.microgrid.electrical_components import (
    ElectricalComponentCategory,
)

from frequenz.client.assets._delivery_area import DeliveryArea
from frequenz.client.assets._location import Location
from frequenz.client.assets._microgrid import Microgrid
from frequenz.client.assets.enums import BatteryType, Metric
from frequenz.client.assets.types import ElectricalComponent

from .test_data import MockData


def create_microgrid_mock(
    microgrid_id: int = MockData.microgrid_id,
    enterprise_id: int = MockData.enterprise_id,
    name: str = MockData.microgrid_name,
    status: int = MockData.microgrid_status,
    **overrides: Any,
) -> AsyncMock:
    """Create microgrid mocks with defaults."""
    mock = AsyncMock(name="microgrid_mock", spec=Microgrid)
    mock.id = microgrid_id
    mock.enterprise_id = enterprise_id
    mock.name = name
    mock.status = status
    # Configure create_timestamp mock to return a datetime directly (not async)
    mock_timestamp = MagicMock()
    mock_timestamp.ToDatetime.return_value = MockData.create_date
    mock.create_timestamp = mock_timestamp

    # Configure HasField to be synchronous (not async)
    mock.HasField = MagicMock(return_value=False)

    # Apply any overrides
    for key, value in overrides.items():
        setattr(mock, key, value)

    return mock


def create_delivery_area_mock(
    code: str = MockData.delivery_area_code,
    code_type: str = MockData.delivery_area_type,
) -> AsyncMock:
    """Create delivery area mocks."""
    mock = AsyncMock(name="delivery_area_mock", spec=DeliveryArea)
    mock.code = code
    mock.code_type = code_type
    return mock


def create_location_mock(
    latitude: float = MockData.latitude,
    longitude: float = MockData.longitude,
    country_code: str = MockData.country_code,
) -> AsyncMock:
    """Create location mocks."""
    mock = AsyncMock(name="location_mock", spec=Location)
    mock.latitude = latitude
    mock.longitude = longitude
    mock.country_code = country_code
    return mock


def create_response_mock() -> AsyncMock:
    """Create response mocks."""
    return AsyncMock()


def create_electrical_component_mock(  # pylint: disable=too-many-arguments
    component_id: int = MockData.component_id,
    microgrid_id: int = MockData.microgrid_id,
    name: str = MockData.component_name,
    *,
    manufacturer: str = MockData.component_manufacturer,
    model_name: str = MockData.component_model_name,
    has_category_specific_info: bool = True,
    has_operational_lifetime: bool = True,
    **overrides: Any,
) -> AsyncMock:
    """Create electrical component mocks with defaults."""
    mock = AsyncMock(name="electrical_component_mock", spec=ElectricalComponent)
    mock.id = component_id
    mock.microgrid_id = microgrid_id
    mock.name = name
    mock.manufacturer = manufacturer
    mock.model_name = model_name
    mock.category = ElectricalComponentCategory.BATTERY

    # Configure HasField to be synchronous (not async)
    def has_field_side_effect(field_name: str) -> bool:
        if field_name == "category_specific_info":
            return has_category_specific_info
        if field_name == "operational_lifetime":
            return has_operational_lifetime
        return False

    mock.HasField = MagicMock(side_effect=has_field_side_effect)

    # Create category specific info
    if has_category_specific_info:
        mock.category_specific_info = MagicMock()
        mock.category_specific_info.WhichOneof.return_value = "battery"
        mock.category_specific_info.battery = MagicMock()
        mock.category_specific_info.battery.type = BatteryType.LI_ION.value

    # Create operational lifetime
    if has_operational_lifetime:
        mock.operational_lifetime = MagicMock()
        mock_start_timestamp = MagicMock()
        mock_start_timestamp.ToDatetime.return_value = MockData.start_time
        mock.operational_lifetime.start_timestamp = mock_start_timestamp

        mock_end_timestamp = MagicMock()
        mock_end_timestamp.ToDatetime.return_value = MockData.end_time
        mock.operational_lifetime.end_timestamp = mock_end_timestamp

    # Create metric config bounds
    mock_metric_config_bounds = MagicMock()
    mock_metric_config_bounds.metric = Metric.BATTERY_SOC_PCT.value
    mock_metric_config_bounds.config_bounds = MagicMock()
    mock_metric_config_bounds.config_bounds.lower = MockData.metric_lower_bound
    mock_metric_config_bounds.config_bounds.upper = MockData.metric_upper_bound
    mock.metric_config_bounds = [mock_metric_config_bounds]

    # Apply any overrides
    for key, value in overrides.items():
        setattr(mock, key, value)

    return mock


def create_electrical_components_response_mock(
    components: list[AsyncMock] | None = None,
) -> AsyncMock:
    """Create electrical components response mock."""
    mock_response = AsyncMock()
    if components is None:
        components = [create_electrical_component_mock()]
    mock_response.components = components
    return mock_response
