import pytest

from ..payloads import *

from App import limits, Models
################################################################################
### Fixtures ###
################################################################################
@pytest.fixture(scope="function")
def new_giveaway_id(client):

    res = client.post(f"/guilds/{TEST_GUILD_ID}/giveaways")
    assert res.status_code == 201, f"Failed to create giveaway: {res.json()}"
    data = res.json()
    assert_giveaway_default_data(data)
    yield data["id"]

################################################################################
@pytest.fixture(scope="function")
def new_giveaway_entry_id(client, new_giveaway_id):

    res = client.post(f"/guilds/{TEST_GUILD_ID}/giveaways/{new_giveaway_id}/entries", json=BASE_USER_ID_PAYLOAD)
    assert res.status_code == 201, f"Failed to create giveaway entry: {res.json()}"
    data = res.json()
    assert_giveaway_entry_default_data(data)
    yield data["id"]

################################################################################
### Assert Group Functions ###
################################################################################
def assert_giveaway_manager_default_data(mgr):

    assert mgr is not None, "Giveaway manager should not be None"
    assert "channel_id" in mgr, "Giveaway manager should have a channel_id"
    assert mgr["channel_id"] is None, "Default channel_id should be None by default"
    assert "giveaways" in mgr, "Giveaway manager should have a giveaways property"
    assert isinstance(mgr["giveaways"], list), "Giveaways should be a list"
    for giveaway in mgr["giveaways"]:
        assert_giveaway_default_data(giveaway)

################################################################################
def assert_giveaway_default_data(g):

    assert g is not None, "Giveaway should not be None"
    assert "id" in g, "Giveaway should have an id"
    assert isinstance(g["id"], int), "Giveaway id should be an integer"
    assert g["id"] >= 0, "Giveaway id should be a non-negative integer"
    assert "winners" in g, "Giveaway should have a winners property"
    assert isinstance(g["winners"], list), "Winners should be a list"
    assert "post_url" in g, "Giveaway should have a post_url property"
    assert g["post_url"] is None, "Default post_url should be None"
    assert "rolled_at" in g, "Giveaway should have a rolled_at property"
    assert g["rolled_at"] is None, "Default rolled_at should be None"
    assert "rolled_by" in g, "Giveaway should have a rolled_by property"
    assert g["rolled_by"] is None, "Default rolled_by should be None"
    assert "details" in g, "Giveaway should have a details property"
    assert_giveaway_details_default_data(g["details"])
    assert "entries" in g, "Giveaway should have an entries property"
    assert isinstance(g["entries"], list), "Entries should be a list"
    for entry in g["entries"]:
        assert_giveaway_entry_default_data(entry)

################################################################################
def assert_giveaway_details_default_data(d):

    assert d is not None, "Giveaway details should not be None"
    assert "name" in d, "Giveaway details should have a name property"
    assert d["name"] is None, "Default giveaway name should be None by default"
    assert "prize" in d, "Giveaway details should have a prize property"
    assert d["prize"] is None, "Default giveaway prize should be None by default"
    assert "num_winners" in d, "Giveaway details should have a num_winners property"
    assert d["num_winners"] == 1, "Default num_winners should be 1 by default"
    assert "auto_notify" in d, "Giveaway details should have an auto_notify property"
    assert isinstance(d["auto_notify"], bool), "auto_notify should be a boolean"
    assert d["auto_notify"] is True, "Default auto_notify should be True by default"
    assert "description" in d, "Giveaway details should have a description property"
    assert d["description"] is None, "Default giveaway description should be None by default"
    assert "thumbnail_url" in d, "Giveaway details should have a thumbnail_url property"
    assert d["thumbnail_url"] is None, "Default giveaway thumbnail_url should be None by default"
    assert "color" in d, "Giveaway details should have a color property"
    assert d["color"] is None, "Default giveaway color should be None by default"
    assert "end_dt" in d, "Giveaway details should have an end_dt property"
    assert d["end_dt"] is None, "Default giveaway end_dt should be None by default"
    assert "emoji" in d, "Giveaway details should have an emoji property"
    assert d["emoji"] is None, "Default giveaway emoji should be None by default"

################################################################################
def assert_giveaway_entry_default_data(e):

    assert e is not None, "Giveaway entry should not be None"
    assert "id" in e, "Giveaway entry should have an id"
    assert isinstance(e["id"], int), "Giveaway entry id should be an integer"
    assert e["id"] >= 0, "Giveaway entry id should be a non-negative integer"
    assert "user_id" in e, "Giveaway entry should have a user_id property"
    assert isinstance(e["user_id"], int), "Giveaway entry user_id should be an integer"
    assert e["user_id"] >= 0, "Giveaway entry user_id should be a non-negative integer"
    assert "timestamp" in e, "Giveaway entry should have a timestamp property"
    assert isinstance(e["timestamp"], str), "Giveaway entry timestamp should be a string"
    assert e["timestamp"] is not None, "Giveaway entry timestamp should not be None"

################################################################################
### Tests ###
################################################################################
# POST Tests
################################################################################

################################################################################
# GET Tests
################################################################################
def test_get_giveaway_manager(client):

    response = client.get(f"/guilds/{TEST_GUILD_ID}/giveaways")
    assert response.status_code == 200
    data = response.json()
    assert_giveaway_manager_default_data(data)

################################################################################
def test_get_giveaway_manager_invalid_guild(client):

    response = client.get(f"/guilds/{INVALID_GUILD_ID}/giveaways")
    assert response.status_code == 404, "Expected 404 for invalid guild ID"

################################################################################
def test_get_giveaway_by_id(client, new_giveaway_id):

    response = client.get(f"/guilds/{TEST_GUILD_ID}/giveaways/{new_giveaway_id}")
    assert response.status_code == 200
    data = response.json()
    assert_giveaway_default_data(data)

################################################################################
def test_get_giveaway_by_id_invalid_guild(client, new_giveaway_id):

    response = client.get(f"/guilds/{INVALID_GUILD_ID}/giveaways/{new_giveaway_id}")
    assert response.status_code == 404, "Expected 404 for invalid guild ID"

################################################################################
def test_get_giveaway_by_id_invalid_giveaway(client, new_giveaway_id):

    response = client.get(f"/guilds/{TEST_GUILD_ID}/giveaways/{INVALID_ID}")
    assert response.status_code == 404, "Expected 404 for invalid giveaway ID"

################################################################################
# DELETE Tests
################################################################################
def test_delete_giveaway(client, db_session, new_giveaway_id, new_giveaway_entry_id):

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/giveaways/{new_giveaway_id}")
    assert res.status_code == 204, f"Failed to delete giveaway: {res.json()}"

    giveaway = db_session.query(Models.GiveawayModel).filter_by(id=new_giveaway_id).first()
    assert giveaway is None, "Giveaway should be deleted from the database"
    details = db_session.query(Models.GiveawayDetailsModel).filter_by(giveaway_id=new_giveaway_id).first()
    assert details is None, "Giveaway details should also be deleted from the database"
    entries = db_session.query(Models.GiveawayEntryModel).filter_by(giveaway_id=new_giveaway_id).all()
    assert len(entries) == 0, "All giveaway entries should be deleted from the database"

################################################################################
def test_delete_giveaway_invalid_guild(client, new_giveaway_id):

    res = client.delete(f"/guilds/{INVALID_GUILD_ID}/giveaways/{new_giveaway_id}")
    assert res.status_code == 404, "Expected 404 for invalid guild ID"

################################################################################
def test_delete_giveaway_invalid_giveaway(client):

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/giveaways/{INVALID_ID}")
    assert res.status_code == 404, "Expected 404 for invalid giveaway ID"

################################################################################
def test_delete_giveaway_entry(client, db_session, new_giveaway_id, new_giveaway_entry_id):

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/giveaways/{new_giveaway_id}/entries/{new_giveaway_entry_id}")
    assert res.status_code == 204, f"Failed to delete giveaway entry: {res.json()}"

    entry = db_session.query(Models.GiveawayEntryModel).filter_by(id=new_giveaway_entry_id).first()
    assert entry is None, "Giveaway entry should be deleted from the database"

################################################################################
def test_delete_giveaway_entry_invalid_guild(client, new_giveaway_id, new_giveaway_entry_id):

    res = client.delete(f"/guilds/{INVALID_GUILD_ID}/giveaways/{new_giveaway_id}/entries/{new_giveaway_entry_id}")
    assert res.status_code == 404, "Expected 404 for invalid guild ID"

################################################################################
def test_delete_giveaway_entry_invalid_giveaway(client, new_giveaway_entry_id):

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/giveaways/{INVALID_ID}/entries/{new_giveaway_entry_id}")
    assert res.status_code == 404, "Expected 404 for invalid giveaway ID"

################################################################################
def test_delete_giveaway_entry_invalid_entry(client, new_giveaway_id):

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/giveaways/{new_giveaway_id}/entries/{INVALID_ID}")
    assert res.status_code == 404, "Expected 404 for invalid giveaway entry ID"

################################################################################
# PATCH Tests
################################################################################

GIVEAWAY_MANAGER_PATCHABLE_FIELDS = {
    "channel_id": TEST_CHANNEL_ID
}

################################################################################
def test_patch_giveaway_manager(client):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/giveaways/")
    assert res.status_code == 200, f"Failed to get giveaway manager: {res.json()}"
    current = res.json()
    assert_giveaway_manager_default_data(current)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/giveaways/", json=GIVEAWAY_MANAGER_PATCHABLE_FIELDS)
    assert res.status_code == 200, f"Failed to patch giveaway manager: {res.json()}"
    updated = res.json()

    for key, value in GIVEAWAY_MANAGER_PATCHABLE_FIELDS.items():
        assert key in updated, f"Key {key} should be present in the updated giveaway manager"
        assert updated[key] == value, f"Key {key} should be updated to {value}"

################################################################################
def test_patch_giveaway_manager_invalid_guild(client):

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/giveaways/", json=GIVEAWAY_MANAGER_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Expected 404 for invalid guild ID"

################################################################################
def test_patch_giveaway_manager_invalid_payload(client):

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/giveaways/", json=INVALID_PAYLOAD)
    assert res.status_code == 422, "Expected 422 for invalid payload in giveaway manager patch"

################################################################################

GIVEAWAY_PATCHABLE_FIELDS = {
    "winners": [TEST_USER_ID],
    "post_url": TEST_DISCORD_POST_URL,
    "rolled_at": TEST_TIMESTAMP,
    "rolled_by": TEST_USER_ID
}

################################################################################
def test_patch_giveaway_full(client, new_giveaway_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/giveaways/{new_giveaway_id}")
    assert res.status_code == 200, f"Failed to get giveaway: {res.json()}"
    current = res.json()
    assert_giveaway_default_data(current)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/giveaways/{new_giveaway_id}", json=GIVEAWAY_PATCHABLE_FIELDS)
    assert res.status_code == 200, f"Failed to patch giveaway: {res.json()}"
    updated = res.json()

    for key, value in GIVEAWAY_PATCHABLE_FIELDS.items():
        assert key in updated, f"Key {key} should be present in the updated giveaway"
        assert updated[key] == value, f"Key {key} should be updated to {value}"

################################################################################
def test_patch_giveaway_invalid_guild(client, new_giveaway_id):

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/giveaways/{new_giveaway_id}", json=GIVEAWAY_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Expected 404 for invalid guild ID"

################################################################################
def test_patch_giveaway_invalid_giveaway(client, new_giveaway_id):

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/giveaways/{INVALID_ID}", json=GIVEAWAY_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Expected 404 for invalid giveaway ID"

################################################################################
def test_patch_giveaway_invalid_payload(client, new_giveaway_id):

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/giveaways/{new_giveaway_id}", json=INVALID_PAYLOAD)
    assert res.status_code == 422, "Expected 422 for invalid payload in giveaway patch"

################################################################################
@pytest.mark.parametrize("field", GIVEAWAY_PATCHABLE_FIELDS.keys())
def test_patch_giveaway_by_field(client, new_giveaway_id, field):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/giveaways/{new_giveaway_id}")
    assert res.status_code == 200, f"Failed to get giveaway: {res.json()}"
    current = res.json()
    assert_giveaway_default_data(current)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/giveaways/{new_giveaway_id}", json={field: GIVEAWAY_PATCHABLE_FIELDS[field]})
    assert res.status_code == 200, f"Failed to patch giveaway by field {field}: {res.json()}"
    updated = res.json()

    for key, value in GIVEAWAY_PATCHABLE_FIELDS.items():
        if key == field:
            assert key in updated, f"Key {key} should be present in the updated giveaway"
            assert updated[key] == value, f"Key {key} should be updated to {value}"
        else:
            assert key in current, f"Key {key} should remain unchanged in the giveaway"
            assert current[key] == updated[key], f"Key {key} should not change when patching by field {field}"

################################################################################

GIVEAWAY_DETAILS_PATCHABLE_FIELDS = {
    "name": TEST_TITLE,
    "prize": TEST_DESCRIPTION,
    "num_winners": 2,
    "auto_notify": False,
    "description": TEST_DESCRIPTION,
    "thumbnail_url": TEST_IMAGE_URL_DISCORD,
    "color": TEST_COLOR,
    "end_dt": TEST_TIMESTAMP2,
    "emoji": TEST_EMOJI
}

################################################################################
def test_patch_giveaway_details(client, new_giveaway_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/giveaways/{new_giveaway_id}")
    assert res.status_code == 200, f"Failed to get giveaway: {res.json()}"
    current = res.json()
    assert_giveaway_default_data(current)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/giveaways/{new_giveaway_id}/details", json=GIVEAWAY_DETAILS_PATCHABLE_FIELDS)
    assert res.status_code == 200, f"Failed to patch giveaway details: {res.json()}"
    updated = res.json()

    for key, value in GIVEAWAY_DETAILS_PATCHABLE_FIELDS.items():
        assert key in updated, f"Key {key} should be present in the updated giveaway details"
        assert updated[key] == value, f"Key {key} should be updated to {value}"

################################################################################
def test_patch_giveaway_details_invalid_guild(client, new_giveaway_id):

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/giveaways/{new_giveaway_id}/details", json=GIVEAWAY_DETAILS_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Expected 404 for invalid guild ID"

################################################################################
def test_patch_giveaway_details_invalid_giveaway(client, new_giveaway_id):

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/giveaways/{INVALID_ID}/details", json=GIVEAWAY_DETAILS_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Expected 404 for invalid giveaway ID"

################################################################################
def test_patch_giveaway_details_invalid_payload(client, new_giveaway_id):

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/giveaways/{new_giveaway_id}/details", json=INVALID_PAYLOAD)
    assert res.status_code == 422, "Expected 422 for invalid payload in giveaway details"

################################################################################
@pytest.mark.parametrize("field", GIVEAWAY_DETAILS_PATCHABLE_FIELDS.keys())
def test_patch_giveaway_details_by_field(client, new_giveaway_id, field):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/giveaways/{new_giveaway_id}")
    assert res.status_code == 200, f"Failed to get giveaway: {res.json()}"
    current = res.json()
    assert_giveaway_default_data(current)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/giveaways/{new_giveaway_id}/details", json={field: GIVEAWAY_DETAILS_PATCHABLE_FIELDS[field]})
    assert res.status_code == 200, f"Failed to patch giveaway details by field {field}: {res.json()}"
    updated = res.json()

    for key, value in GIVEAWAY_DETAILS_PATCHABLE_FIELDS.items():
        if key == field:
            assert key in updated, f"Key {key} should be present in the updated giveaway details"
            assert updated[key] == value, f"Key {key} should be updated to {value}"
        else:
            assert key in current["details"], f"Key {key} should remain unchanged in the giveaway details"
            assert current["details"][key] == updated[key], f"Key {key} should not change when patching by field {field}"

################################################################################
