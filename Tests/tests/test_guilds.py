import pytest

from ..payloads import *
################################################################################
def assert_guild_default_values(guild, expected_id):

    assert guild is not None, "Guild should not be None"
    assert "guild_id" in guild, "Guild should have a guild_id field"
    assert guild["guild_id"] == expected_id, f"Guild ID should be {expected_id}, got {guild['guild_id']}"
    assert "data" in guild, "Guild should have a data field"
    assert isinstance(guild["data"], dict), "Guild data should be a dictionary"
    data = guild["data"]
    assert "configuration" in data, "Guild data should have a configuration field"
    assert isinstance(data["configuration"], dict), "Guild configuration should be a dictionary"
    assert "embeds" in data, "Guild data should have a embeds field"
    assert isinstance(data["embeds"], list), "Guild embeds should be a list"

################################################################################
def test_register_guild(client):
    """Test guild registration with valid payload."""

    res = client.post("/guilds/", json={"guild_id": TEST_GUILD_ID2})
    assert res.status_code == 201, "Should return 201 for successful registration"
    confirmation = res.json()
    assert_guild_default_values(confirmation, TEST_GUILD_ID2)

################################################################################
def test_register_guild_duplicate(client):
    """Test guild registration with a duplicate ID."""

    test_register_guild(client)
    res = client.post("/guilds/", json={"guild_id": TEST_GUILD_ID2})
    assert res.status_code == 409, "Should return 409 for duplicate guild ID"

################################################################################
def test_register_guild_invalid_payload(client):
    """Test guild registration with an invalid payload."""

    res = client.post("/guilds/", json=INVALID_PAYLOAD)
    assert res.status_code == 422, "Should return 422 for invalid payload"

################################################################################
def test_get_guild(client):
    """Test retrieving a guild by ID."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}")
    assert res.status_code == 200, "Should return 200 for valid guild ID"
    guild = res.json()
    assert_guild_default_values(guild, TEST_GUILD_ID)

################################################################################
def test_get_guild_not_found(client):
    """Test retrieving a guild that does not exist."""

    res = client.get(f"/guilds/{TEST_GUILD_ID2}")
    assert res.status_code == 404, "Should return 404 for non-existent guild ID"

################################################################################

GUILD_CONFIGURATION_PATCHABLE_FIELDS = {
    "timezone": DEFAULT_TIMEZONE + 1,
    "log_channel_id": TEST_CHANNEL_ID
}

################################################################################
def test_patch_guild_configuration_full(client):
    """Test updating the full guild configuration."""

    payload = {
        "editor_id": TEST_USER_ID,
        **GUILD_CONFIGURATION_PATCHABLE_FIELDS
    }

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/configuration", json=payload)
    assert res.status_code == 200, "Should return 200 for successful configuration update"
    config = res.json()
    assert "log_channel_id" in config, "Configuration should have a log_channel_id field"
    assert config["log_channel_id"] == payload["log_channel_id"], "Log channel ID should match the payload"
    assert "timezone" in config, "Configuration should have a timezone field"
    assert config["timezone"] == payload["timezone"], "Timezone should match the payload"

################################################################################
@pytest.mark.parametrize("payload", GUILD_CONFIGURATION_PATCHABLE_FIELDS.keys())
def test_patch_guild_configuration_partial(client, payload):
    """Test updating a single field in the guild configuration."""

    update_payload = {
        "editor_id": TEST_USER_ID,
        payload: GUILD_CONFIGURATION_PATCHABLE_FIELDS[payload]
    }

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/configuration", json=update_payload)
    assert res.status_code == 200, "Should return 200 for successful configuration update"
    config = res.json()
    assert config[payload] == GUILD_CONFIGURATION_PATCHABLE_FIELDS[payload], f"{payload} should match the payload"

################################################################################
def test_patch_guild_configuration_invalid_guild(client):
    """Test updating the configuration of a non-existent guild."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID2}/configuration", json={
        "editor_id": TEST_USER_ID,
        "log_channel_id": TEST_CHANNEL_ID
    })
    assert res.status_code == 404, "Should return 404 for non-existent guild ID"

################################################################################
def test_patch_guild_configuration_invalid_payload(client):
    """Test updating the guild configuration with an invalid payload."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/configuration", json=INVALID_PAYLOAD)
    assert res.status_code == 422, "Should return 422 for invalid payload"

################################################################################
