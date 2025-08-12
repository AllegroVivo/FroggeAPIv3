import pytest

from ..payloads import *

from App import limits, Models
################################################################################
### Fixtures ###
################################################################################
@pytest.fixture(scope="function")
def new_raffle_id(client):

    res = client.post(f"/guilds/{TEST_GUILD_ID}/raffles")
    assert res.status_code == 201, f"Failed to create raffle: {res.json()}"
    raffle = res.json()
    assert_raffle_default_data(raffle)
    yield raffle["id"]

################################################################################
@pytest.fixture(scope="function")
def new_raffle_entry_id(client, new_raffle_id):

    res = client.post(
        f"/guilds/{TEST_GUILD_ID}/raffles/{new_raffle_id}/entries",
        json=CREATE_RAFFLE_ENTRY_PAYLOAD
    )
    assert res.status_code == 201, f"Failed to create raffle entry: {res.json()}"
    entry = res.json()
    assert_raffle_entry_default_data(entry)
    yield entry["id"]

################################################################################
### Assert Group Functions ###
################################################################################
def assert_raffle_default_data(raffle):

    assert raffle is not None, "Raffle should not be None"
    assert "id" in raffle, "Raffle should have an 'id' field"
    assert isinstance(raffle["id"], int), "Raffle id should be an integer"
    assert raffle["id"] >= 0, "Raffle id should be >= 0"
    assert "winners" in raffle, "Raffle should have 'winners' field"
    assert isinstance(raffle["winners"], list), "Raffle winners should be a list"
    assert len(raffle["winners"]) == 0, "Raffle winners should be empty by default"
    assert "is_active" in raffle, "Raffle should have 'is_active' field"
    assert isinstance(raffle["is_active"], bool), "Raffle is_active should be a boolean"
    assert raffle["is_active"] is False, "Raffle is_active should be False by default"
    assert "post_url" in raffle, "Raffle should have 'post_url' field"
    assert raffle["post_url"] is None, "Raffle post_url should be None by default"
    assert "name" in raffle, "Raffle should have 'name' field"
    assert raffle["name"] is None, "Raffle name should be None by default"
    assert "prize" in raffle, "Raffle should have 'prize' field"
    assert raffle["prize"] is None, "Raffle prize should be None by default"
    assert "num_winners" in raffle, "Raffle should have 'num_winners' field"
    assert isinstance(raffle["num_winners"], int), "Raffle num_winners should be an integer"
    assert raffle["num_winners"] == 1, "Raffle num_winners should be 1 by default"
    assert "auto_notify" in raffle, "Raffle should have 'auto_notify' field"
    assert isinstance(raffle["auto_notify"], bool), "Raffle auto_notify should be a boolean"
    assert raffle["auto_notify"] is True, "Raffle auto_notify should be True by default"
    assert "cost" in raffle, "Raffle should have 'cost' field"
    assert isinstance(raffle["cost"], int), "Raffle cost should be an integer"
    assert raffle["cost"] == 100000, "Raffle cost should be 100000 by default"
    assert "rolled_at" in raffle, "Raffle should have 'rolled_at' field"
    assert raffle["rolled_at"] is None, "Raffle rolled_at should be None by default"
    assert "rolled_by" in raffle, "Raffle should have 'rolled_by' field"
    assert raffle["rolled_by"] is None, "Raffle rolled_by should be None by default"
    assert "entries" in raffle, "Raffle should have 'entries' field"
    for entry in raffle["entries"]:
        assert_raffle_entry_default_data(entry)

################################################################################
def assert_raffle_entry_default_data(e):

    assert e is not None, "Raffle entry should not be None"
    assert "id" in e, "Raffle entry should have an 'id' field"
    assert isinstance(e["id"], int), "Raffle entry id should be an integer"
    assert e["id"] >= 0, "Raffle entry id should be >= 0"
    assert "user_id" in e, "Raffle entry should have 'user_id' field"
    assert isinstance(e["user_id"], int), "Raffle entry user_id should be an integer"
    assert e["user_id"] >= 0, "Raffle entry user_id should be >= 0"
    assert "quantity" in e, "Raffle entry should have 'quantity' field"
    assert isinstance(e["quantity"], int), "Raffle entry quantity should be an integer"
    assert e["quantity"] == 1, "Raffle entry quantity should be 1 by default"

################################################################################
# GET Tests
################################################################################
def test_get_raffle_manager(client, new_raffle_id):
    """Test getting the raffle manager for a specific guild."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/raffles")
    assert res.status_code == 200, f"Failed to get raffle manager: {res.json()}"
    mgr = res.json()
    assert isinstance(mgr, dict), "Response should be a dictionary of mgr"
    assert len(mgr) > 0, "There should be at least one raffle"
    assert "channel_id" in mgr, "Raffle manager should have 'channel_id' field"
    assert mgr["channel_id"] is None, "Raffle manager channel_id should be None by default"
    assert "raffles" in mgr, "Raffle manager should have 'raffles' field"
    for raffle in mgr["raffles"]:
        assert_raffle_default_data(raffle)

################################################################################
def test_get_raffle_manager_invalid_guild(client):
    """Test getting the raffle manager for an invalid guild."""

    res = client.get(f"/guilds/{INVALID_GUILD_ID}/raffles")
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_get_raffle_by_id(client, new_raffle_id):
    """Test getting a specific raffle by ID."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/raffles/{new_raffle_id}")
    assert res.status_code == 200, f"Failed to get raffle by ID: {res.json()}"
    raffle = res.json()
    assert_raffle_default_data(raffle)

################################################################################
def test_get_raffle_by_id_invalid_guild(client, new_raffle_id):
    """Test getting a raffle by ID in an invalid guild."""

    res = client.get(f"/guilds/{INVALID_GUILD_ID}/raffles/{new_raffle_id}")
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_get_raffle_by_id_not_found(client, new_raffle_id):
    """Test getting a raffle by ID that does not exist."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/raffles/{INVALID_ID}")
    assert res.status_code == 404, f"Expected 404 for non-existent raffle, got {res.status_code}: {res.json()}"

################################################################################
# DELETE Tests
################################################################################
def test_delete_raffle_by_id(client, new_raffle_id):
    """Test deleting a raffle by ID."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/raffles/{new_raffle_id}")
    assert res.status_code == 204, f"Failed to delete raffle: {res.json()}"

    res = client.get(f"/guilds/{TEST_GUILD_ID}/raffles/{new_raffle_id}")
    assert res.status_code == 404, f"Expected 404 after deletion, got {res.status_code}: {res.json()}"

################################################################################
def test_delete_raffle_by_id_invalid_guild(client, new_raffle_id):
    """Test deleting a raffle by ID in an invalid guild."""

    res = client.delete(f"/guilds/{INVALID_GUILD_ID}/raffles/{new_raffle_id}")
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_delete_raffle_by_id_not_found(client, new_raffle_id):
    """Test deleting a raffle by ID that does not exist."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/raffles/{INVALID_ID}")
    assert res.status_code == 404, f"Expected 404 for non-existent raffle, got {res.status_code}: {res.json()}"

################################################################################
def test_delete_raffle_entry_by_id(client, db_session, new_raffle_id, new_raffle_entry_id):
    """Test deleting a raffle entry by ID."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/raffles/{new_raffle_id}/entries/{new_raffle_entry_id}")
    assert res.status_code == 204, f"Failed to delete raffle entry: {res.json()}"

    present = db_session.query(Models.RaffleEntryModel).filter_by(id=new_raffle_entry_id).first()
    assert present is None, "Raffle entry should be deleted from the database"

################################################################################
def test_delete_raffle_entry_by_id_invalid_guild(client, new_raffle_id, new_raffle_entry_id):
    """Test deleting a raffle entry by ID in an invalid guild."""

    res = client.delete(f"/guilds/{INVALID_GUILD_ID}/raffles/{new_raffle_id}/entries/{new_raffle_entry_id}")
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"
################################################################################
def test_delete_raffle_entry_by_id_raffle_not_found(client, new_raffle_id, new_raffle_entry_id):
    """Test deleting a raffle entry by ID that does not exist."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/raffles/{INVALID_ID}/entries/{new_raffle_entry_id}")
    assert res.status_code == 404, f"Expected 404 for non-existent raffle entry, got {res.status_code}: {res.json()}"

################################################################################
def test_delete_raffle_entry_by_id_entry_not_found(client, new_raffle_id, new_raffle_entry_id):
    """Test deleting a raffle entry by ID that does not exist."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/raffles/{new_raffle_id}/entries/{INVALID_ID}")
    assert res.status_code == 404, f"Expected 404 for non-existent raffle entry, got {res.status_code}: {res.json()}"

################################################################################
# PATCH Tests
################################################################################

RAFFLE_MANAGER_PATCHABLE_FIELDS = {
    "channel_id": TEST_CHANNEL_ID,
}

################################################################################
def test_patch_raffle_manager_full(client, new_raffle_id):
    """Test patching the raffle manager."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/raffles", json=RAFFLE_MANAGER_PATCHABLE_FIELDS)
    assert res.status_code == 200, f"Failed to patch raffle manager: {res.json()}"
    mgr = res.json()
    assert isinstance(mgr, dict), "Response should be a dictionary of mgr"
    assert "channel_id" in mgr, "Raffle manager should have 'channel_id' field"
    for k, v in RAFFLE_MANAGER_PATCHABLE_FIELDS.items():
        assert mgr[k] == v, f"Raffle manager {k} should be updated to {v}"

################################################################################
@pytest.mark.parametrize("field", RAFFLE_MANAGER_PATCHABLE_FIELDS.keys())
def test_patch_raffle_manager_by_field(client, new_raffle_id, field):
    """Test patching the raffle manager by a specific field."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/raffles")
    assert res.status_code == 200, f"Failed to get raffle manager: {res.json()}"
    existing = res.json()

    payload = {field: RAFFLE_MANAGER_PATCHABLE_FIELDS[field]}
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/raffles", json=payload)
    assert res.status_code == 200, f"Failed to patch raffle manager: {res.json()}"
    mgr = res.json()
    assert isinstance(mgr, dict), "Response should be a dictionary of mgr"
    assert "channel_id" in mgr, "Raffle manager should have 'channel_id' field"
    for k in RAFFLE_MANAGER_PATCHABLE_FIELDS.keys():
        if k == field:
            assert mgr[k] == RAFFLE_MANAGER_PATCHABLE_FIELDS[k], f"Raffle manager {k} should be updated to {RAFFLE_MANAGER_PATCHABLE_FIELDS[k]}"
        else:
            assert mgr[k] == existing[k], f"Raffle manager {k} should remain unchanged"

################################################################################
def test_patch_raffle_manager_invalid_guild(client):
    """Test patching the raffle manager in an invalid guild."""

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/raffles", json=RAFFLE_MANAGER_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_raffle_manager_invalid_payload(client, new_raffle_id):
    """Test patching the raffle manager with an invalid payload."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/raffles", json=INVALID_PAYLOAD)
    assert res.status_code == 422, f"Expected 422 for invalid field, got {res.status_code}: {res.json()}"

################################################################################

RAFFLE_PATCHABLE_ITEMS = {
    "winners": [TEST_USER_ID, TEST_USER_ID2],
    "is_active": True,
    "post_url": TEST_DISCORD_POST_URL,
    "name": TEST_TITLE,
    "prize": TEST_TITLE,
    "num_winners": 2,
    "auto_notify": False,
    "cost": 500000,
    "rolled_at": TEST_TIMESTAMP,
    "rolled_by": TEST_USER_ID,
}

################################################################################
def test_patch_raffle(client, new_raffle_id):
    """Test patching a specific raffle."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/raffles/{new_raffle_id}")
    assert res.status_code == 200, f"Failed to get raffle by ID: {res.json()}"
    existing = res.json()
    assert_raffle_default_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/raffles/{new_raffle_id}", json=RAFFLE_PATCHABLE_ITEMS)
    assert res.status_code == 200, f"Failed to patch raffle: {res.json()}"
    raffle = res.json()
    for k, v in RAFFLE_PATCHABLE_ITEMS.items():
        assert k in raffle, f"Raffle {k} should be updated to {v}"
        assert raffle[k] == v, f"Raffle {k} should be updated to {v}"
        assert raffle[k] != existing[k], f"Raffle {k} should have changed from {existing[k]} to {v}"

################################################################################
@pytest.mark.parametrize("field", RAFFLE_PATCHABLE_ITEMS.keys())
def test_patch_raffle_by_field(client, new_raffle_id, field):
    """Test patching a specific raffle by a specific field."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/raffles/{new_raffle_id}")
    assert res.status_code == 200, f"Failed to get raffle by ID: {res.json()}"
    existing = res.json()
    assert_raffle_default_data(existing)

    payload = {field: RAFFLE_PATCHABLE_ITEMS[field]}
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/raffles/{new_raffle_id}", json=payload)
    assert res.status_code == 200, f"Failed to patch raffle: {res.json()}"
    raffle = res.json()
    for k in RAFFLE_PATCHABLE_ITEMS.keys():
        if k == field:
            assert raffle[k] == RAFFLE_PATCHABLE_ITEMS[k], f"Raffle {k} should be updated to {RAFFLE_PATCHABLE_ITEMS[k]}"
        else:
            assert raffle[k] == existing[k], f"Raffle {k} should remain unchanged"

################################################################################
def test_patch_raffle_invalid_guild(client, new_raffle_id):
    """Test patching a raffle in an invalid guild."""

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/raffles/{new_raffle_id}", json=RAFFLE_PATCHABLE_ITEMS)
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_raffle_invalid_raffle(client, new_raffle_id):
    """Test patching a raffle that does not exist."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/raffles/{INVALID_ID}", json=RAFFLE_PATCHABLE_ITEMS)
    assert res.status_code == 404, f"Expected 404 for non-existent raffle, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_raffle_invalid_payload(client, new_raffle_id):
    """Test patching a raffle with an invalid payload."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/raffles/{new_raffle_id}", json=INVALID_PAYLOAD)
    assert res.status_code == 422, f"Expected 422 for invalid field, got {res.status_code}: {res.json()}"

################################################################################

RAFFLE_ENTRY_PATCHABLE_FIELDS = {
    "quantity": 2,
}

################################################################################
def test_patch_raffle_entry(client, new_raffle_id, new_raffle_entry_id):
    """Test patching a specific raffle entry."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/raffles/{new_raffle_id}/")
    assert res.status_code == 200, f"Failed to get raffle entry by ID: {res.json()}"
    existing = res.json()["entries"][0]
    assert_raffle_entry_default_data(existing)

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/raffles/{new_raffle_id}/entries/{new_raffle_entry_id}",
        json=RAFFLE_ENTRY_PATCHABLE_FIELDS
    )
    assert res.status_code == 200, f"Failed to patch raffle entry: {res.json()}"
    entry = res.json()
    for k, v in RAFFLE_ENTRY_PATCHABLE_FIELDS.items():
        assert k in entry, f"Raffle entry {k} should be updated to {v}"
        assert entry[k] == v, f"Raffle entry {k} should be updated to {v}"
        assert entry[k] != existing[k], f"Raffle entry {k} should have changed from {existing[k]} to {v}"

################################################################################
@pytest.mark.parametrize("field", RAFFLE_ENTRY_PATCHABLE_FIELDS.keys())
def test_patch_raffle_entry_by_field(client, new_raffle_id, new_raffle_entry_id, field):
    """Test patching a specific raffle entry by a specific field."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/raffles/{new_raffle_id}/")
    assert res.status_code == 200, f"Failed to get raffle entry by ID: {res.json()}"
    existing = res.json()["entries"][0]
    assert_raffle_entry_default_data(existing)

    payload = {field: RAFFLE_ENTRY_PATCHABLE_FIELDS[field]}
    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/raffles/{new_raffle_id}/entries/{new_raffle_entry_id}",
        json=payload
    )
    assert res.status_code == 200, f"Failed to patch raffle entry: {res.json()}"
    entry = res.json()
    for k in RAFFLE_ENTRY_PATCHABLE_FIELDS.keys():
        if k == field:
            assert entry[k] == RAFFLE_ENTRY_PATCHABLE_FIELDS[k], f"Raffle entry {k} should be updated to {RAFFLE_ENTRY_PATCHABLE_FIELDS[k]}"
        else:
            assert entry[k] == existing[k], f"Raffle entry {k} should remain unchanged"

################################################################################
def test_patch_raffle_entry_invalid_guild(client, new_raffle_id, new_raffle_entry_id):
    """Test patching a raffle entry in an invalid guild."""

    res = client.patch(
        f"/guilds/{INVALID_GUILD_ID}/raffles/{new_raffle_id}/entries/{new_raffle_entry_id}",
        json=RAFFLE_ENTRY_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_raffle_entry_invalid_raffle(client, new_raffle_id, new_raffle_entry_id):
    """Test patching a raffle entry that does not exist."""

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/raffles/{INVALID_ID}/entries/{new_raffle_entry_id}",
        json=RAFFLE_ENTRY_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, f"Expected 404 for non-existent raffle, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_raffle_entry_invalid_entry(client, new_raffle_id, new_raffle_entry_id):
    """Test patching a raffle entry that does not exist."""

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/raffles/{new_raffle_id}/entries/{INVALID_ID}",
        json=RAFFLE_ENTRY_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, f"Expected 404 for non-existent raffle entry, got {res.status_code}: {res.json()}"

################################################################################
