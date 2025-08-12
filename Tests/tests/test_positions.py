import pytest

from ..payloads import *

from App import limits
################################################################################
### Fixtures ###
################################################################################
@pytest.fixture(scope="function")
def new_position_id(client):

    res = client.post(f"/guilds/{TEST_GUILD_ID}/positions")
    assert res.status_code == 201, f"Failed to create Position: {res.json()}"
    message = res.json()
    assert_position_default_data(message)
    yield message["id"]

################################################################################
### Assert Group Functions ###
################################################################################
def assert_position_default_data(p):

    assert p is not None, "Position should not be None"
    assert "id" in p, "Position should have an 'id' field"
    assert isinstance(p["id"], int), "Position id should be an integer"
    assert p["id"] >= 0, "Position id should be >= 0"
    assert "name" in p, "Position should have a 'name' field"
    assert p["name"] is None, "Position name should be None by default"
    assert "role_id" in p, "Position should have a 'role_id' field"
    assert p["role_id"] is None, "Position role_id should be None by default"

################################################################################
# POST Tests
################################################################################

################################################################################
# GET Tests
################################################################################
def test_get_all_positions(client, new_position_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/positions")
    assert res.status_code == 200, f"Failed to get Positions: {res.json()}"
    positions = res.json()
    assert isinstance(positions, list), "Response should be a list of Positions"
    for pos in positions:
        assert_position_default_data(pos)

################################################################################
def test_get_all_positions_invalid_guild(client):

    res = client.get(f"/guilds/{INVALID_GUILD_ID}/positions")
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_get_position_by_id(client, new_position_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/positions/{new_position_id}")
    assert res.status_code == 200, f"Failed to get Position by ID: {res.json()}"
    message = res.json()
    assert_position_default_data(message)

################################################################################
def test_get_position_by_id_invalid_guild(client, new_position_id):

    res = client.get(f"/guilds/{INVALID_GUILD_ID}/positions/{new_position_id}")
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_get_position_by_id_not_found(client, new_position_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/positions/{INVALID_ID}")
    assert res.status_code == 404, f"Expected 404 for non-existent Position, got {res.status_code}: {res.json()}"

################################################################################
# DELETE Tests
################################################################################
def test_delete_position(client, new_position_id):

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/positions/{new_position_id}")
    assert res.status_code == 204, f"Failed to delete Position: {res.json()}"

    res = client.get(f"/guilds/{TEST_GUILD_ID}/positions/{new_position_id}")
    assert res.status_code == 404, f"Expected 404 for deleted Position, got {res.status_code}: {res.json()}"

################################################################################
# PATCH Tests
################################################################################

POSITION_PATCHABLE_FIELDS = {
    "name": TEST_TITLE,
    "role_id": TEST_ROLE_ID
}

################################################################################
def test_patch_position_full(client, new_position_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/positions/{new_position_id}")
    assert res.status_code == 200, f"Failed to get Position by ID: {res.json()}"
    existing = res.json()
    assert_position_default_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/positions/{new_position_id}", json=POSITION_PATCHABLE_FIELDS)
    assert res.status_code == 200, f"Failed to patch Position: {res.json()}"
    current = res.json()

    for key, value in POSITION_PATCHABLE_FIELDS.items():
        assert key in current, f"Position should have field '{key}' after patching"
        assert current[key] == value, f"Position {key} did not update correctly: expected {value}, got {current[key]}"

################################################################################
@pytest.mark.parametrize("field", POSITION_PATCHABLE_FIELDS.keys())
def test_patch_position_partial(client, new_position_id, field):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/positions/{new_position_id}")
    assert res.status_code == 200, f"Failed to get Position by ID: {res.json()}"
    existing = res.json()
    assert_position_default_data(existing)

    partial_update = {field: POSITION_PATCHABLE_FIELDS[field]}
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/positions/{new_position_id}", json=partial_update)
    assert res.status_code == 200, f"Failed to patch Position: {res.json()}"
    current = res.json()

    for key, value in POSITION_PATCHABLE_FIELDS.items():
        if key == field:
            assert current[key] == value, f"Position {key} did not update correctly: expected {value}, got {current[key]}"
        else:
            assert current[key] == existing[key], f"Position {key} should not have changed: expected {existing[key]}, got {current[key]}"

################################################################################
def test_patch_position_invalid_guild(client, new_position_id):

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/positions/{new_position_id}", json=POSITION_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_position_invalid_message(client, new_position_id):

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/positions/{INVALID_ID}", json=POSITION_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for non-existent Position, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_position_invalid_payload(client, new_position_id):

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/positions/{new_position_id}", json=INVALID_PAYLOAD)
    assert res.status_code == 422, f"Expected 422 for invalid fields, got {res.status_code}: {res.json()}"

################################################################################
