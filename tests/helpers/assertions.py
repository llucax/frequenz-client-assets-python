# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Helper functions for common assertions."""

from frequenz.client.assets._microgrid import Microgrid
from frequenz.client.assets.enums import BatteryType, Metric
from frequenz.client.assets.types import Battery, ElectricalComponent

from .test_data import MockData


def assert_microgrid_basic_fields(
    result: Microgrid,
    expected_id: int = MockData.microgrid_id,
    expected_enterprise_id: int = MockData.enterprise_id,
    expected_name: str = MockData.microgrid_name,
) -> None:
    """Assert basic microgrid fields are correct."""
    assert str(result.id) == f"MID{expected_id}"
    assert str(result.enterprise_id) == f"EID{expected_enterprise_id}"
    assert result.name == expected_name


def assert_delivery_area_present(
    result: Microgrid, expected_code: str = MockData.delivery_area_code
) -> None:
    """Assert delivery area is present and correct."""
    assert result.delivery_area is not None
    assert result.delivery_area.code == expected_code


def assert_delivery_area_absent(result: Microgrid) -> None:
    """Assert delivery area is not present."""
    assert result.delivery_area is None


def assert_location_present(
    result: Microgrid,
    expected_country: str = MockData.country_code,
    expected_latitude: float = MockData.latitude,
) -> None:
    """Assert location is present and correct."""
    assert result.location is not None
    assert result.location.country_code == expected_country
    assert result.location.latitude == expected_latitude


def assert_location_absent(result: Microgrid) -> None:
    """Assert location is not present."""
    assert result.location is None


def assert_electrical_component_basic_fields(  # pylint: disable=too-many-arguments
    result: ElectricalComponent,
    expected_id: int = MockData.component_id,
    *,
    expected_microgrid_id: int = MockData.microgrid_id,
    expected_name: str = MockData.component_name,
    expected_manufacturer: str = MockData.component_manufacturer,
    expected_model_name: str = MockData.component_model_name,
) -> None:
    """Assert basic electrical component fields are correct."""
    assert str(result.id) == f"CID{expected_id}"
    assert str(result.microgrid_id) == f"MID{expected_microgrid_id}"
    assert result.name == expected_name
    assert result.manufacturer == expected_manufacturer
    assert result.model_name == expected_model_name


def assert_electrical_component_category_specific_info_present(
    result: ElectricalComponent,
    expected_battery_type: BatteryType = BatteryType.LI_ION,
) -> None:
    """Assert category specific info is present and correct."""
    assert result.category_specific_info is not None

    assert isinstance(result.category_specific_info, Battery)
    assert result.category_specific_info.type == expected_battery_type


def assert_electrical_component_category_specific_info_absent(
    result: ElectricalComponent,
) -> None:
    """Assert category specific info is not present."""
    assert result.category_specific_info is None


def assert_electrical_component_operational_lifetime_present(
    result: ElectricalComponent,
) -> None:
    """Assert operational lifetime is present and correct."""
    assert result.operational_lifetime is not None
    assert result.operational_lifetime.start_time == MockData.start_time
    assert result.operational_lifetime.end_time == MockData.end_time


def assert_electrical_component_operational_lifetime_absent(
    result: ElectricalComponent,
) -> None:
    """Assert operational lifetime is not present."""
    assert result.operational_lifetime is None


def assert_electrical_component_metric_config_bounds(
    result: ElectricalComponent,
    expected_metric: Metric = Metric.BATTERY_SOC_PCT,
    expected_lower: float = MockData.metric_lower_bound,
    expected_upper: float = MockData.metric_upper_bound,
) -> None:
    """Assert metric config bounds are correct."""
    assert len(result.metric_config_bounds) > 0
    metric_bounds = result.metric_config_bounds[0]
    assert metric_bounds.metric == expected_metric
    assert metric_bounds.config_bounds is not None
    assert metric_bounds.config_bounds.lower == expected_lower
    assert metric_bounds.config_bounds.upper == expected_upper
