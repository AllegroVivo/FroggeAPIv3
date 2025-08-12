import pytest

from ..payloads import *

from App import limits
################################################################################
### Fixtures ###
################################################################################
@pytest.fixture(scope="function")
def new_glyph_message_id(client):

    res = client.post(f"/guilds/{TEST_GUILD_ID}/glyph-messages")
    assert res.status_code == 201, f"Failed to create glyph message: {res.json()}"
    message = res.json()
    assert_glyph_message_default_data(message)
    yield message["id"]

################################################################################
### Assert Group Functions ###
################################################################################
def assert_glyph_message_default_data(gm):

    assert gm is not None, "Glyph message should not be None"
    assert "id" in gm, "Glyph message should have an 'id' field"
    assert isinstance(gm["id"], int), "Glyph message id should be an integer"
    assert gm["id"] >= 0, "Glyph message id should be >= 0"
    assert "name" in gm, "Glyph message should have a 'name' field"
    assert gm["name"] is None, "Glyph message name should be None by default"
    assert "message" in gm, "Glyph message should have a 'message' field"
    assert gm["message"] is None, "Glyph message content should be None by default"

################################################################################
# POST Tests
################################################################################

################################################################################
# GET Tests
################################################################################
def test_get_all_glyph_messages(client, new_glyph_message_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/glyph-messages")
    assert res.status_code == 200, f"Failed to get glyph messages: {res.json()}"
    messages = res.json()
    assert isinstance(messages, list), "Response should be a list of glyph messages"
    for message in messages:
        assert_glyph_message_default_data(message)

################################################################################
def test_get_all_glyph_messages_invalid_guild(client):

    res = client.get(f"/guilds/{INVALID_GUILD_ID}/glyph-messages")
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_get_glyph_message_by_id(client, new_glyph_message_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/glyph-messages/{new_glyph_message_id}")
    assert res.status_code == 200, f"Failed to get glyph message by ID: {res.json()}"
    message = res.json()
    assert_glyph_message_default_data(message)

################################################################################
def test_get_glyph_message_by_id_invalid_guild(client, new_glyph_message_id):

    res = client.get(f"/guilds/{INVALID_GUILD_ID}/glyph-messages/{new_glyph_message_id}")
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_get_glyph_message_by_id_not_found(client, new_glyph_message_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/glyph-messages/{INVALID_ID}")
    assert res.status_code == 404, f"Expected 404 for non-existent glyph message, got {res.status_code}: {res.json()}"

################################################################################
# DELETE Tests
################################################################################
def test_delete_glyph_message(client, new_glyph_message_id):

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/glyph-messages/{new_glyph_message_id}")
    assert res.status_code == 204, f"Failed to delete glyph message: {res.json()}"

    res = client.get(f"/guilds/{TEST_GUILD_ID}/glyph-messages/{new_glyph_message_id}")
    assert res.status_code == 404, f"Expected 404 for deleted glyph message, got {res.status_code}: {res.json()}"

################################################################################
# PATCH Tests
################################################################################

GLYPH_MESSAGE_PATCHABLE_FIELDS = {
    "name": TEST_TITLE,
    "message": TEST_STRING_WITH_UNICODE
}

################################################################################
def test_patch_glyph_message_full(client, new_glyph_message_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/glyph-messages/{new_glyph_message_id}")
    assert res.status_code == 200, f"Failed to get glyph message by ID: {res.json()}"
    existing = res.json()
    assert_glyph_message_default_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/glyph-messages/{new_glyph_message_id}", json=GLYPH_MESSAGE_PATCHABLE_FIELDS)
    assert res.status_code == 200, f"Failed to patch glyph message: {res.json()}"
    current = res.json()

    for key, value in GLYPH_MESSAGE_PATCHABLE_FIELDS.items():
        assert key in current, f"Glyph message should have field '{key}' after patching"
        assert current[key] == value, f"Glyph message {key} did not update correctly: expected {value}, got {current[key]}"

################################################################################
@pytest.mark.parametrize("field", GLYPH_MESSAGE_PATCHABLE_FIELDS.keys())
def test_patch_glyph_message_partial(client, new_glyph_message_id, field):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/glyph-messages/{new_glyph_message_id}")
    assert res.status_code == 200, f"Failed to get glyph message by ID: {res.json()}"
    existing = res.json()
    assert_glyph_message_default_data(existing)

    partial_update = {field: GLYPH_MESSAGE_PATCHABLE_FIELDS[field]}
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/glyph-messages/{new_glyph_message_id}", json=partial_update)
    assert res.status_code == 200, f"Failed to patch glyph message: {res.json()}"
    current = res.json()

    for key, value in GLYPH_MESSAGE_PATCHABLE_FIELDS.items():
        if key == field:
            assert current[key] == value, f"Glyph message {key} did not update correctly: expected {value}, got {current[key]}"
        else:
            assert current[key] == existing[key], f"Glyph message {key} should not have changed: expected {existing[key]}, got {current[key]}"

################################################################################
def test_patch_glyph_message_invalid_guild(client, new_glyph_message_id):

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/glyph-messages/{new_glyph_message_id}", json=GLYPH_MESSAGE_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_glyph_message_invalid_message(client, new_glyph_message_id):

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/glyph-messages/{INVALID_ID}", json=GLYPH_MESSAGE_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for non-existent glyph message, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_glyph_message_invalid_payload(client, new_glyph_message_id):

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/glyph-messages/{new_glyph_message_id}", json=INVALID_PAYLOAD)
    assert res.status_code == 422, f"Expected 422 for invalid fields, got {res.status_code}: {res.json()}"

################################################################################
