import pytest

from ..payloads import *

from App import limits, Models
################################################################################
### Fixtures ###
################################################################################
@pytest.fixture(scope="function")
def new_reaction_role_message_id(client):
    """Fixture to create a new reaction role message for testing."""

    res = client.post(f"/guilds/{TEST_GUILD_ID}/reaction-roles/")
    assert res.status_code == 201, f"Failed to create reaction role message: {res.json()}"
    message = res.json()
    assert_reaction_role_message_default_data(message)
    return message["id"]

################################################################################
@pytest.fixture(scope="function")
def new_reaction_role_id(client, new_reaction_role_message_id):
    """Fixture to create a new reaction role for a reaction role message."""

    res = client.post(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}/roles")
    assert res.status_code == 201, f"Failed to create reaction role: {res.json()}"
    role = res.json()
    assert_reaction_role_default_data(role)
    return role["id"]

################################################################################
### Assert Group Functions ###
################################################################################
def assert_reaction_role_manager_default_data(mgr):

    assert mgr is not None, "Reaction role manager should not be None"
    assert isinstance(mgr, dict), "Reaction role manager should be a dictionary"
    assert "channel_id" in mgr, "Response should contain 'channel_id'"
    assert mgr["channel_id"] is None, "Channel ID should be None by default"
    assert "messages" in mgr, "Response should contain 'messages'"
    assert isinstance(mgr["messages"], list), "Messages should be a list"
    for msg in mgr["messages"]:
        assert_reaction_role_message_default_data(msg)

################################################################################
def assert_reaction_role_message_default_data(m):

    assert m is not None, "Reaction role message should not be None"
    assert isinstance(m, dict), "Reaction role message should be a dictionary"
    assert "id" in m, "Reaction role message should have an 'id' field"
    assert isinstance(m["id"], int), "Reaction role message ID should be an integer"
    assert m["id"] >= 0, "Reaction role message ID should be >= than 0"
    assert "title" in m, "Reaction role message should have a 'title' field"
    assert m["title"] is None, "Reaction role message title should be None by default"
    assert "description" in m, "Reaction role message should have a 'description' field"
    assert m["description"] is None, "Reaction role message description should be None by default"
    assert "color" in m, "Reaction role message should have a 'color' field"
    assert m["color"] is None, "Reaction role message color should be None by default"
    assert "thumbnail_url" in m, "Reaction role message should have a 'thumbnail_url' field"
    assert m["thumbnail_url"] is None, "Reaction role message thumbnail_url should be None by default"
    assert "post_url" in m, "Reaction role message should have a 'post_url' field"
    assert m["post_url"] is None, "Reaction role message post_url should be None by default"
    assert "msg_type" in m, "Reaction role message should have a 'msg_type' field"
    assert isinstance(m["msg_type"], int), "Reaction role message msg_type should be an integer"
    assert m["msg_type"] == 1, "Reaction role message msg_type should be 1 by default"
    assert "type_param" in m, "Reaction role message should have a 'type_params' field"
    assert m["type_param"] is None, "Reaction role message type_param should be None by default"
    assert "roles" in m, "Reaction role message should have a 'roles' field"
    for role in m["roles"]:
        assert_reaction_role_default_data(role)

################################################################################
def assert_reaction_role_default_data(r):
    """Assert that the reaction role has the default data structure."""

    assert r is not None, "Reaction role should not be None"
    assert isinstance(r, dict), "Reaction role should be a dictionary"
    assert "id" in r, "Reaction role should have an 'id' field"
    assert isinstance(r["id"], int), "Reaction role ID should be an integer"
    assert r["id"] >= 0, "Reaction role ID should be >= than 0"
    assert "emoji" in r, "Reaction role should have an 'emoji' field"
    assert r["emoji"] is None, "Reaction role emoji should be None by default"
    assert "role_id" in r, "Reaction role should have a 'role_id' field"
    assert r["role_id"] is None, "Reaction role role_id should be None by default"
    assert "label" in r, "Reaction role should have a 'label' field"
    assert r["label"] is None, "Reaction role label should be None by default"

################################################################################
# GET Tests
################################################################################
def test_get_role_manager(client, new_reaction_role_message_id):
    """Test retrieving the reaction role manager for a guild."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/reaction-roles/")
    assert res.status_code == 200, f"Failed to get reaction role manager: {res.json()}"
    mgr = res.json()
    assert_reaction_role_manager_default_data(mgr)

################################################################################
def test_get_role_manager_invalid_guild(client):
    """Test retrieving the reaction role manager for an invalid guild ID."""

    res = client.get(f"/guilds/{INVALID_GUILD_ID}/reaction-roles/")
    assert res.status_code == 404, f"Expected 404 for invalid guild ID, got {res.status_code}: {res.json()}"

################################################################################
def test_get_role_message_by_id(client, new_reaction_role_message_id):
    """Test retrieving a specific reaction role message by ID."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}")
    assert res.status_code == 200, f"Failed to get reaction role message: {res.json()}"
    msg = res.json()
    assert_reaction_role_message_default_data(msg)
    assert msg["id"] == new_reaction_role_message_id, "Message ID should match the requested ID"

################################################################################
def test_get_role_message_by_id_invalid_guild(client, new_reaction_role_message_id):
    """Test retrieving a reaction role message with an invalid guild ID."""

    res = client.get(f"/guilds/{INVALID_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}")
    assert res.status_code == 404, f"Expected 404 for invalid guild ID, got {res.status_code}: {res.json()}"

################################################################################
def test_get_role_message_by_id_invalid_id(client):
    """Test retrieving a reaction role message with an invalid ID."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{INVALID_ID}")
    assert res.status_code == 404, f"Expected 404 for invalid message ID, got {res.status_code}: {res.json()}"

################################################################################
# DELETE Tests
################################################################################
def test_delete_role_message(client, new_reaction_role_message_id):
    """Test deleting a reaction role message."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}")
    assert res.status_code == 204, f"Failed to delete reaction role message: {res.json()}"

    # Verify the message is deleted
    res = client.get(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}")
    assert res.status_code == 404, f"Expected 404 after deletion, got {res.status_code}: {res.json()}"

################################################################################
def test_delete_role_message_invalid_guild(client, new_reaction_role_message_id):
    """Test deleting a reaction role message with an invalid guild ID."""

    res = client.delete(f"/guilds/{INVALID_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}")
    assert res.status_code == 404, f"Expected 404 for invalid guild ID, got {res.status_code}: {res.json()}"

################################################################################
def test_delete_role_message_invalid_id(client, new_reaction_role_message_id):
    """Test deleting a reaction role message with an invalid ID."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{INVALID_ID}")
    assert res.status_code == 404, f"Expected 404 for invalid message ID, got {res.status_code}: {res.json()}"

################################################################################
def test_delete_reaction_role(client, db_session, new_reaction_role_message_id, new_reaction_role_id):
    """Test deleting a reaction role from a message."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}/roles/{new_reaction_role_id}")
    assert res.status_code == 204, f"Failed to delete reaction role: {res.json()}"

    # Verify the role is deleted
    role = db_session.query(Models.ReactionRoleModel).filter_by(id=new_reaction_role_id).first()
    assert role is None, "Reaction role should be deleted from the database"

################################################################################
def test_delete_reaction_role_invalid_guild(client, new_reaction_role_message_id, new_reaction_role_id):
    """Test deleting a reaction role with an invalid guild ID."""

    res = client.delete(f"/guilds/{INVALID_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}/roles/{new_reaction_role_id}")
    assert res.status_code == 404, f"Expected 404 for invalid guild ID, got {res.status_code}: {res.json()}"

################################################################################
def test_delete_reaction_role_invalid_message(client, new_reaction_role_id):
    """Test deleting a reaction role with an invalid message ID."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{INVALID_ID}/roles/{new_reaction_role_id}")
    assert res.status_code == 404, f"Expected 404 for invalid message ID, got {res.status_code}: {res.json()}"

################################################################################
def test_delete_reaction_role_invalid_role(client, new_reaction_role_message_id):
    """Test deleting a reaction role with an invalid role ID."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}/roles/{INVALID_ID}")
    assert res.status_code == 404, f"Expected 404 for invalid role ID, got {res.status_code}: {res.json()}"

################################################################################
# PATCH Tests
################################################################################

REACTION_ROLE_MANAGER_PATCHABLE_FIELDS = {
    "channel_id": TEST_CHANNEL_ID,
}

################################################################################
def test_patch_reaction_role_manager_full(client):
    """Test patching the reaction role manager for a guild."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/reaction-roles/")
    assert res.status_code == 200, f"Failed to get reaction roles: {res.json()}"
    existing = res.json()
    assert_reaction_role_manager_default_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/reaction-roles/", json=REACTION_ROLE_MANAGER_PATCHABLE_FIELDS)
    assert res.status_code == 200, f"Failed to patch reaction role manager: {res.json()}"
    updated = res.json()

    for key, value in REACTION_ROLE_MANAGER_PATCHABLE_FIELDS.items():
        assert key in updated, f"Response should contain '{key}' field"
        assert updated[key] == value, f"Field '{key}' should be updated to {value}"

################################################################################
@pytest.mark.parametrize("field", REACTION_ROLE_MANAGER_PATCHABLE_FIELDS.keys())
def test_patch_reaction_role_manager_partial(client, field):
    """Test patching the reaction role manager with a single field."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/reaction-roles/")
    assert res.status_code == 200, f"Failed to get reaction roles: {res.json()}"
    existing = res.json()
    assert_reaction_role_manager_default_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/reaction-roles/", json={field: REACTION_ROLE_MANAGER_PATCHABLE_FIELDS[field]})
    assert res.status_code == 200, f"Failed to patch reaction role manager: {res.json()}"
    updated = res.json()

    for key, value in REACTION_ROLE_MANAGER_PATCHABLE_FIELDS.items():
        if key == field:
            assert key in updated, f"Response should contain '{key}' field"
            assert updated[key] == value, f"Field '{key}' should be updated to {value}"
        else:
            assert key in existing, f"Response should not contain '{key}' field"
            assert updated[key] == existing[key], f"Field '{key}' should remain unchanged"

################################################################################
def test_patch_reaction_role_manager_invalid_guild(client):
    """Test patching the reaction role manager with an invalid guild ID."""

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/reaction-roles/", json=REACTION_ROLE_MANAGER_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for invalid guild ID, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_reaction_role_manager_invalid_payload(client):
    """Test patching the reaction role manager with an invalid payload."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/reaction-roles/", json=INVALID_PAYLOAD)
    assert res.status_code == 422, f"Expected 422 for invalid field, got {res.status_code}: {res.json()}"

################################################################################

REACTION_ROLE_MESSAGE_PATCHABLE_FIELDS = {
    "title": TEST_TITLE,
    "description": TEST_DESCRIPTION,
    "color": TEST_COLOR,
    "thumbnail_url": TEST_IMAGE_URL_DISCORD,
    "post_url": TEST_DISCORD_POST_URL,
    "msg_type": 2,
    "type_param": 1
}

################################################################################
def test_patch_reation_role_message_full(client, new_reaction_role_message_id):
    """Test patching a reaction role message with all fields."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}")
    assert res.status_code == 200, f"Failed to get reaction role message: {res.json()}"
    existing = res.json()
    assert_reaction_role_message_default_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}", json=REACTION_ROLE_MESSAGE_PATCHABLE_FIELDS)
    assert res.status_code == 200, f"Failed to patch reaction role message: {res.json()}"
    updated = res.json()

    for key, value in REACTION_ROLE_MESSAGE_PATCHABLE_FIELDS.items():
        assert key in updated, f"Response should contain '{key}' field"
        assert updated[key] == value, f"Field '{key}' should be updated to {value}"

################################################################################
@pytest.mark.parametrize("field", REACTION_ROLE_MESSAGE_PATCHABLE_FIELDS.keys())
def test_patch_reaction_role_message_partial(client, new_reaction_role_message_id, field):
    """Test patching a reaction role message with a single field."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}")
    assert res.status_code == 200, f"Failed to get reaction role message: {res.json()}"
    existing = res.json()
    assert_reaction_role_message_default_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}", json={field: REACTION_ROLE_MESSAGE_PATCHABLE_FIELDS[field]})
    assert res.status_code == 200, f"Failed to patch reaction role message: {res.json()}"
    updated = res.json()

    for key, value in REACTION_ROLE_MESSAGE_PATCHABLE_FIELDS.items():
        if key == field:
            assert key in updated, f"Response should contain '{key}' field"
            assert updated[key] == value, f"Field '{key}' should be updated to {value}"
        else:
            assert key in existing, f"Response should not contain '{key}' field"
            assert updated[key] == existing[key], f"Field '{key}' should remain unchanged"

################################################################################
def test_patch_reaction_role_message_invalid_guild(client, new_reaction_role_message_id):
    """Test patching a reaction role message with an invalid guild ID."""

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}", json=REACTION_ROLE_MESSAGE_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for invalid guild ID, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_reaction_role_message_invalid_id(client):
    """Test patching a reaction role message with an invalid ID."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{INVALID_ID}", json=REACTION_ROLE_MESSAGE_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for invalid message ID, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_reaction_role_message_invalid_payload(client, new_reaction_role_message_id):
    """Test patching a reaction role message with an invalid payload."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}", json=INVALID_PAYLOAD)
    assert res.status_code == 422, f"Expected 422 for invalid field, got {res.status_code}: {res.json()}"

################################################################################

REACTION_ROLE_PATCHABLE_FIELDS = {
    "emoji": TEST_EMOJI,
    "role_id": TEST_ROLE_ID,
    "label": TEST_TITLE
}

################################################################################
def test_patch_reaction_role_full(client, new_reaction_role_message_id, new_reaction_role_id):
    """Test patching a reaction role with all fields."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}/roles/{new_reaction_role_id}", json=REACTION_ROLE_PATCHABLE_FIELDS)
    assert res.status_code == 200, f"Failed to patch reaction role: {res.json()}"
    updated = res.json()

    for key, value in REACTION_ROLE_PATCHABLE_FIELDS.items():
        assert key in updated, f"Response should contain '{key}' field"
        assert updated[key] == value, f"Field '{key}' should be updated to {value}"

################################################################################
@pytest.mark.parametrize("field", REACTION_ROLE_PATCHABLE_FIELDS.keys())
def test_patch_reaction_role_partial(client, new_reaction_role_message_id, new_reaction_role_id, field):
    """Test patching a reaction role with a single field."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}/")
    assert res.status_code == 200, f"Failed to get reaction role: {res.json()}"
    existing = res.json()["roles"][0]
    assert_reaction_role_default_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}/roles/{new_reaction_role_id}", json={field: REACTION_ROLE_PATCHABLE_FIELDS[field]})
    assert res.status_code == 200, f"Failed to patch reaction role: {res.json()}"
    updated = res.json()

    for key, value in REACTION_ROLE_PATCHABLE_FIELDS.items():
        if key == field:
            assert key in updated, f"Response should contain '{key}' field"
            assert updated[key] == value, f"Field '{key}' should be updated to {value}"
        else:
            assert key in existing, f"Response should not contain '{key}' field"
            assert updated[key] == existing[key], f"Field '{key}' should remain unchanged"

################################################################################
def test_patch_reaction_role_invalid_guild(client, new_reaction_role_message_id, new_reaction_role_id):
    """Test patching a reaction role with an invalid guild ID."""

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}/roles/{new_reaction_role_id}", json=REACTION_ROLE_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for invalid guild ID, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_reaction_role_invalid_message(client, new_reaction_role_id):
    """Test patching a reaction role with an invalid message ID."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{INVALID_ID}/roles/{new_reaction_role_id}", json=REACTION_ROLE_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for invalid message ID, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_reaction_role_invalid_role(client, new_reaction_role_message_id):
    """Test patching a reaction role with an invalid role ID."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}/roles/{INVALID_ID}", json=REACTION_ROLE_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for invalid role ID, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_reaction_role_invalid_payload(client, new_reaction_role_message_id, new_reaction_role_id):
    """Test patching a reaction role with an invalid payload."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/reaction-roles/{new_reaction_role_message_id}/roles/{new_reaction_role_id}", json=INVALID_PAYLOAD)
    assert res.status_code == 422, f"Expected 422 for invalid field, got {res.status_code}: {res.json()}"

################################################################################
