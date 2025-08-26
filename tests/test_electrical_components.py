# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for electrical components functionality."""

from unittest.mock import AsyncMock

import pytest

from tests.conftest import ClientSetup
from tests.helpers.assertions import (
    assert_electrical_component_basic_fields,
    assert_electrical_component_category_specific_info_absent,
    assert_electrical_component_category_specific_info_present,
    assert_electrical_component_metric_config_bounds,
    assert_electrical_component_operational_lifetime_absent,
    assert_electrical_component_operational_lifetime_present,
)
from tests.helpers.factories import (
    create_electrical_component_mock,
    create_electrical_components_response_mock,
)


def setup_electrical_component_with_fields(
    mock_component: AsyncMock,
    has_category_specific_info: bool = False,
    has_operational_lifetime: bool = False,
) -> None:
    """Set up electrical component mock with optional fields."""

    def has_field_side_effect(field_name: str) -> bool:
        if field_name == "category_specific_info":
            return has_category_specific_info
        if field_name == "operational_lifetime":
            return has_operational_lifetime
        return False

    mock_component.HasField.side_effect = has_field_side_effect


@pytest.mark.parametrize(
    "has_category_specific_info,has_operational_lifetime",
    [
        (False, False),
        (True, False),
        (False, True),
        (True, True),
    ],
    ids=[
        "without optional fields",
        "with category specific info only",
        "with operational lifetime only",
        "with all optional fields",
    ],
)
async def test_get_electrical_components_optional_fields(
    client_setup: ClientSetup,
    has_category_specific_info: bool,
    has_operational_lifetime: bool,
) -> None:
    """Test get_electrical_components with different combinations of optional fields."""
    client, mock_stub = client_setup.client, client_setup.mock_stub

    # Setup
    mock_component = create_electrical_component_mock(
        has_category_specific_info=has_category_specific_info,
        has_operational_lifetime=has_operational_lifetime,
    )
    setup_electrical_component_with_fields(
        mock_component,
        has_category_specific_info=has_category_specific_info,
        has_operational_lifetime=has_operational_lifetime,
    )
    response = create_electrical_components_response_mock([mock_component])
    mock_stub.ListMicrogridElectricalComponents.return_value = response

    # Execute
    result = await client.get_electrical_components(client_setup.microgrid_id)

    # Assert we got a list with one component
    assert len(result) == 1
    component = result[0]

    # Assert basic fields always present
    assert_electrical_component_basic_fields(component)
    assert_electrical_component_metric_config_bounds(component)

    # Assert optional fields based on parameters
    if has_category_specific_info:
        assert_electrical_component_category_specific_info_present(component)
    else:
        assert_electrical_component_category_specific_info_absent(component)

    if has_operational_lifetime:
        assert_electrical_component_operational_lifetime_present(component)
    else:
        assert_electrical_component_operational_lifetime_absent(component)

    # Verify stub was called correctly
    mock_stub.ListMicrogridElectricalComponents.assert_called_once()


async def test_get_electrical_components_basic_functionality(
    client_setup: ClientSetup,
) -> None:
    """Test basic successful electrical components retrieval functionality."""
    client, mock_stub = client_setup.client, client_setup.mock_stub

    # Setup basic response without optional fields
    mock_component = create_electrical_component_mock(
        has_category_specific_info=False,
        has_operational_lifetime=False,
    )
    setup_electrical_component_with_fields(
        mock_component,
        has_category_specific_info=False,
        has_operational_lifetime=False,
    )
    response = create_electrical_components_response_mock([mock_component])
    mock_stub.ListMicrogridElectricalComponents.return_value = response

    # Execute
    result = await client.get_electrical_components(client_setup.microgrid_id)

    # Assert we got a list with one component
    assert len(result) == 1
    component = result[0]

    # Assert basic fields
    assert_electrical_component_basic_fields(component)
    assert_electrical_component_metric_config_bounds(component)
    assert_electrical_component_category_specific_info_absent(component)
    assert_electrical_component_operational_lifetime_absent(component)

    # Verify stub was called correctly
    mock_stub.ListMicrogridElectricalComponents.assert_called_once()


async def test_get_electrical_components_multiple_components(
    client_setup: ClientSetup,
) -> None:
    """Test retrieving multiple electrical components."""
    client, mock_stub = client_setup.client, client_setup.mock_stub

    # Setup multiple components
    mock_component1 = create_electrical_component_mock(
        component_id=1,
        name="Component 1",
        has_category_specific_info=True,
        has_operational_lifetime=True,
    )
    mock_component2 = create_electrical_component_mock(
        component_id=2,
        name="Component 2",
        has_category_specific_info=False,
        has_operational_lifetime=False,
    )

    setup_electrical_component_with_fields(
        mock_component1,
        has_category_specific_info=True,
        has_operational_lifetime=True,
    )
    setup_electrical_component_with_fields(
        mock_component2,
        has_category_specific_info=False,
        has_operational_lifetime=False,
    )

    response = create_electrical_components_response_mock(
        [mock_component1, mock_component2]
    )
    mock_stub.ListMicrogridElectricalComponents.return_value = response

    # Execute
    result = await client.get_electrical_components(client_setup.microgrid_id)

    # Assert we got a list with two components
    assert len(result) == 2

    # Assert first component
    component1 = result[0]
    assert str(component1.id) == "CID1"
    assert component1.name == "Component 1"
    assert_electrical_component_category_specific_info_present(component1)
    assert_electrical_component_operational_lifetime_present(component1)

    # Assert second component
    component2 = result[1]
    assert str(component2.id) == "CID2"
    assert component2.name == "Component 2"
    assert_electrical_component_category_specific_info_absent(component2)
    assert_electrical_component_operational_lifetime_absent(component2)

    # Verify stub was called correctly
    mock_stub.ListMicrogridElectricalComponents.assert_called_once()


async def test_get_electrical_components_empty_list(
    client_setup: ClientSetup,
) -> None:
    """Test retrieving electrical components when none are found."""
    client, mock_stub = client_setup.client, client_setup.mock_stub

    # Setup empty response
    response = create_electrical_components_response_mock([])
    mock_stub.ListMicrogridElectricalComponents.return_value = response

    # Execute
    result = await client.get_electrical_components(client_setup.microgrid_id)

    # Assert we got an empty list
    assert len(result) == 0
    assert result == []

    # Verify stub was called correctly
    mock_stub.ListMicrogridElectricalComponents.assert_called_once()


async def test_get_electrical_components_with_all_features(
    client_setup: ClientSetup,
) -> None:
    """Test electrical component with all features enabled."""
    client, mock_stub = client_setup.client, client_setup.mock_stub

    # Setup component with all features
    mock_component = create_electrical_component_mock(
        has_category_specific_info=True,
        has_operational_lifetime=True,
    )
    setup_electrical_component_with_fields(
        mock_component,
        has_category_specific_info=True,
        has_operational_lifetime=True,
    )
    response = create_electrical_components_response_mock([mock_component])
    mock_stub.ListMicrogridElectricalComponents.return_value = response

    # Execute
    result = await client.get_electrical_components(client_setup.microgrid_id)

    # Assert we got a list with one component
    assert len(result) == 1
    component = result[0]

    # Assert all fields
    assert_electrical_component_basic_fields(component)
    assert_electrical_component_category_specific_info_present(component)
    assert_electrical_component_operational_lifetime_present(component)
    assert_electrical_component_metric_config_bounds(component)

    # Verify stub was called correctly
    mock_stub.ListMicrogridElectricalComponents.assert_called_once()
