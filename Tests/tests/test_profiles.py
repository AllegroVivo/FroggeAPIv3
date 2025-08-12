import pytest

from ..payloads import *

from App import limits, Models
################################################################################

_requirements_keys = (
    "url", "color", "jobs", "rates", "gender", "race", "orientation", "height",
    "age", "mare", "world", "likes", "dislikes", "personality", "aboutme",
    "thumbnail", "main_image"
)

################################################################################
### Fixtures ###
################################################################################
@pytest.fixture(scope="function")
def new_profile_id(client):
    """Fixture to create a new profile and return its ID."""

    res = client.post(f"/guilds/{TEST_GUILD_ID}/profiles", json=BASE_USER_ID_PAYLOAD)
    assert res.status_code == 201, f"Failed to create profile: {res.json()}"
    profile = res.json()
    assert_profile_default_data(profile)
    yield profile["id"]

################################################################################
@pytest.fixture(scope="function")
def new_profile_additional_image_id(client, new_profile_id):
    """Fixture to create a new additional image for a profile and return its ID."""

    res = client.post(
        f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/images/additional",
        json=ADDITIONAL_IMAGE_CREATE_PAYLOAD
    )
    assert res.status_code == 201, f"Failed to create additional image: {res.json()}"
    additional_image = res.json()
    assert_profile_additional_image_default_data(additional_image)
    yield additional_image["id"]

################################################################################
@pytest.fixture(scope="function")
def new_profile_channel_group_id(client):
    """Fixture to create a new profile channel group and return its ID."""

    res = client.post(f"/guilds/{TEST_GUILD_ID}/profiles/channel-groups")
    assert res.status_code == 201, f"Failed to create profile channel group: {res.json()}"
    group = res.json()
    assert_profile_channel_group_default_data(group)
    yield group["id"]

################################################################################
### Assert Group Functions ###
################################################################################
def assert_profile_default_data(p):

    assert p is not None, "Profile should not be None"
    assert isinstance(p, dict), "Profile should be a dictionary"
    assert "id" in p, "Profile should have an 'id' field"
    assert isinstance(p["id"], int), "Profile id should be an integer"
    assert p["id"] >= 0, "Profile id should be >= 0"
    assert "user_id" in p, "Profile should have a 'user_id' field"
    assert isinstance(p["user_id"], int), "Profile user_id should be an integer"
    assert p["user_id"] == TEST_USER_ID, "Profile user_id should be an integer"
    assert "post_url" in p, "Profile should have a 'post_url' field"
    assert p["post_url"] is None, "Profile post_url should be None by default"
    assert "details" in p, "Profile should have a 'details' field"
    assert_profile_details_default_data(p["details"])
    assert "ataglance" in p, "Profile should have an 'ataglance' field"
    assert_profile_ataglance_default_data(p["ataglance"])
    assert "personality" in p, "Profile should have a 'personality' field"
    assert_profile_personality_default_data(p["personality"])
    assert "images" in p, "Profile should have an 'images' field"
    assert_profile_images_default_data(p["images"])

################################################################################
def assert_profile_details_default_data(d):

    assert d is not None, "Profile details should not be None"
    assert isinstance(d, dict), "Profile details should be a dictionary"
    assert "name" in d, "Profile details should have a 'name' field"
    assert d["name"] is None, "Profile details name should be None by default"
    assert "custom_url" in d, "Profile details should have a 'custom_url' field"
    assert d["custom_url"] is None, "Profile details custom_url should be None by default"
    assert "color" in d, "Profile details should have a 'color' field"
    assert d["color"] is None, "Profile details color should be None by default"
    assert "jobs" in d, "Profile details should have a 'jobs' field"
    assert isinstance(d["jobs"], list), "Profile details jobs should be a list"
    assert len(d["jobs"]) == 0, "Profile details jobs should be an empty list by default"
    assert "rates" in d, "Profile details should have a 'rates' field"
    assert d["rates"] is None, "Profile details rates should be None by default"

################################################################################
def assert_profile_ataglance_default_data(aag):

    assert aag is not None, "Profile ataglance should not be None"
    assert isinstance(aag, dict), "Profile ataglance should be a dictionary"
    assert "world" in aag, "Profile ataglance should have a 'world' field"
    assert aag["world"] is None, "Profile ataglance world should be None by default"
    assert "gender_enum" in aag, "Profile ataglance should have a gender_enum field"
    assert aag["gender_enum"] is None, "Profile ataglance gender_enum should be None by default"
    assert "pronouns" in aag, "Profile ataglance should have a 'pronouns' field"
    assert isinstance(aag["pronouns"], list), "Profile ataglance pronouns should be a list"
    assert len(aag["pronouns"]) == 0, "Profile ataglance pronouns should be an empty list by default"
    assert "race_enum" in aag, "Profile ataglance should have a race_enum field"
    assert aag["race_enum"] is None, "Profile ataglance race_enum should be None by default"
    assert "clan_enum" in aag, "Profile ataglance should have a clan_enum field"
    assert aag["clan_enum"] is None, "Profile ataglance clan enum should be None by default"
    assert "orientation_enum" in aag, "Profile ataglance should have an orientation_enum field"
    assert aag["orientation_enum"] is None, "Profile ataglance orientation_enum should be None by default"
    assert "race_custom" in aag, "Profile ataglance should have a race_custom field"
    assert aag["race_custom"] is None, "Profile ataglance race_custom should be None by default"
    assert "clan_custom" in aag, "Profile ataglance should have a clan_custom field"
    assert aag["clan_custom"] is None, "Profile ataglance clan_custom should be None by default"
    assert "orientation_custom" in aag, "Profile ataglance should have an orientation_custom field"
    assert aag["orientation_custom"] is None, "Profile ataglance orientation_custom should be None by default"
    assert "height" in aag, "Profile ataglance should have a height field"
    assert aag["height"] is None, "Profile ataglance height should be None by default"
    assert "age" in aag, "Profile ataglance should have an age field"
    assert aag["age"] is None, "Profile ataglance age should be None by default"
    assert "mare" in aag, "Profile ataglance should have a mare field"
    assert aag["mare"] is None, "Profile ataglance mare should be None by default"

################################################################################
def assert_profile_personality_default_data(p):

    assert p is not None, "Profile personality should not be None"
    assert isinstance(p, dict), "Profile personality should be a dictionary"
    assert "likes" in p, "Profile personality should have a 'likes' field"
    assert isinstance(p["likes"], list), "Profile personality likes should be a list"
    assert len(p["likes"]) == 0, "Profile personality likes should be an empty list by default"
    assert "dislikes" in p, "Profile personality should have a 'dislikes' field"
    assert isinstance(p["dislikes"], list), "Profile personality dislikes should be a list"
    assert len(p["dislikes"]) == 0, "Profile personality dislikes should be an empty list by default"
    assert "personality" in p, "Profile personality should have a 'personality' field"
    assert p["personality"] is None, "Profile personality should be None by default"
    assert "aboutme" in p, "Profile personality should have an 'aboutme' field"
    assert p["aboutme"] is None, "Profile personality aboutme should be None by default"

################################################################################
def assert_profile_images_default_data(i):

    assert i is not None, "Profile images should not be None"
    assert isinstance(i, dict), "Profile images should be a dictionary"
    assert "thumbnail_url" in i, "Profile images should have a 'thumbnail_url' field"
    assert i["thumbnail_url"] is None, "Profile images thumbnail_url should be None by default"
    assert "main_image_url" in i, "Profile images should have a 'main_image_url' field"
    assert i["main_image_url"] is None, "Profile images main_image_url should be None by default"
    assert "addl_images" in i, "Profile images should have an 'addl_images' field"
    assert isinstance(i["addl_images"], list), "Profile images addl_images should be a list"
    for addl in i["addl_images"]:
        assert_profile_additional_image_default_data(addl)

################################################################################
def assert_profile_additional_image_default_data(ai):

    assert ai is not None, "Profile additional image should not be None"
    assert isinstance(ai, dict), "Profile additional image should be a dictionary"
    assert "id" in ai, "Profile additional image should have an 'id' field"
    assert isinstance(ai["id"], int), "Profile additional image id should be an integer"
    assert ai["id"] >= 0, "Profile additional image id should be >= 0"
    assert "url" in ai, "Profile additional image should have a 'url' field"
    assert ai["url"] == TEST_IMAGE_URL_CLOUDINARY, "Profile additional image url should be None by default"
    assert "caption" in ai, "Profile additional image should have a 'caption' field"
    assert ai["caption"] is None, "Profile additional image caption should be None by default"

################################################################################
def assert_profile_channel_group_default_data(cg):

    assert cg is not None, "Profile channel group should not be None"
    assert isinstance(cg, dict), "Profile channel group should be a dictionary"
    assert "id" in cg, "Profile channel group should have an 'id' field"
    assert isinstance(cg["id"], int), "Profile channel group id should be an integer"
    assert cg["id"] >= 0, "Profile channel group id should be >= 0"
    assert "channel_ids" in cg, "Profile channel group should have a 'channel_ids' field"
    assert isinstance(cg["channel_ids"], list), "Profile channel group channel_ids should be a list"
    assert len(cg["channel_ids"]) == 0, "Profile channel group channel_ids should be an empty list by default"
    assert "role_ids" in cg, "Profile channel group should have a 'role_ids' field"
    assert isinstance(cg["role_ids"], list), "Profile channel group role_ids should be a list"
    assert len(cg["role_ids"]) == 0, "Profile channel group role_ids should be an empty list by default"

################################################################################
def assert_profile_requirement_default_data(r):

    assert r is not None, "Profile requirement should not be None"
    assert isinstance(r, dict), "Profile requirement should be a dictionary"
    for key in _requirements_keys:
        assert key in r, f"Profile requirement should have a '{key}' field"
        assert isinstance(r[key], bool), "Profile requirement url should be a boolean"
        assert r[key] is False, f"Profile requirement {key} should be False by default"

################################################################################
# GET Tests
################################################################################
def test_get_profile_manager(client, new_profile_id):
    """Test getting the profile manager."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/")
    assert res.status_code == 200, f"Failed to get profile manager: {res.json()}"
    mgr = res.json()
    assert isinstance(mgr, dict), "Profile manager should be a dictionary"
    assert "requirements" in mgr, "Profile manager should have a 'requirements' field"
    assert_profile_requirement_default_data(mgr["requirements"])
    assert "profiles" in mgr, "Profile manager should have a 'profiles' field"
    assert isinstance(mgr["profiles"], list), "Profile manager profiles should be a list"
    assert len(mgr["profiles"]) == 1, "Profile manager should have one profile"
    assert_profile_default_data(mgr["profiles"][0])
    assert "channel_groups" in mgr, "Profile manager should have a 'channel_groups' field"
    assert isinstance(mgr["channel_groups"], list), "Profile manager channel_groups should be a list"
    assert len(mgr["channel_groups"]) == 0, "Profile manager should have no channel groups by default"

################################################################################
def test_get_profile_manager_invalid_guild(client):
    """Test getting the profile manager for an invalid guild."""

    res = client.get(f"/guilds/{INVALID_GUILD_ID}/profiles/")
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_get_profile_by_id(client, new_profile_id):
    """Test getting a profile by ID."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}")
    assert res.status_code == 200, f"Failed to get profile by ID: {res.json()}"
    profile = res.json()
    assert_profile_default_data(profile)

################################################################################
def test_get_profile_by_id_invalid_guild(client, new_profile_id):
    """Test getting a profile by ID for an invalid guild."""

    res = client.get(f"/guilds/{INVALID_GUILD_ID}/profiles/{new_profile_id}")
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_get_profile_by_id_invalid_id(client, new_profile_id):
    """Test getting a profile by ID that does not exist."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/{INVALID_ID}")
    assert res.status_code == 404, f"Expected 404 for non-existent profile, got {res.status_code}: {res.json()}"

################################################################################
# DELETE Tests
################################################################################
def test_delete_profile_by_id(client, db_session, new_profile_id):
    """Test deleting a profile by ID."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}")
    assert res.status_code == 204, f"Failed to delete profile: {res.json()}"

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}")
    assert res.status_code == 404, f"Expected 404 for deleted profile, got {res.status_code}: {res.json()}"

    # Ensure all subtables are also deleted
    details = db_session.query(Models.ProfileDetailsModel).filter_by(profile_id=new_profile_id).first()
    assert details is None, "Profile details should be deleted when profile is deleted"
    ataglance = db_session.query(Models.ProfileAtAGlanceModel).filter_by(profile_id=new_profile_id).first()
    assert ataglance is None, "Profile ataglance should be deleted when profile is deleted"
    personality = db_session.query(Models.ProfilePersonalityModel).filter_by(profile_id=new_profile_id).first()
    assert personality is None, "Profile personality should be deleted when profile is deleted"
    images = db_session.query(Models.ProfileImagesModel).filter_by(profile_id=new_profile_id).first()
    assert images is None, "Profile images should be deleted when profile is deleted"

################################################################################
def test_delete_profile_by_id_invalid_guild(client, new_profile_id):
    """Test deleting a profile by ID for an invalid guild."""

    res = client.delete(f"/guilds/{INVALID_GUILD_ID}/profiles/{new_profile_id}")
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_delete_profile_by_id_invalid_id(client, new_profile_id):
    """Test deleting a profile by ID that does not exist."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/profiles/{INVALID_ID}")
    assert res.status_code == 404, f"Expected 404 for non-existent profile, got {res.status_code}: {res.json()}"

################################################################################
def test_delete_profile_additional_image_by_id(
    client, db_session, new_profile_id, new_profile_additional_image_id
):
    """Test deleting an additional image from a profile by ID."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/images/additional/{new_profile_additional_image_id}")
    assert res.status_code == 204, f"Failed to delete additional image: {res.json()}"

    # Ensure the image is deleted from the database
    image = db_session.query(Models.ProfileAdditionalImageModel).filter_by(id=new_profile_additional_image_id).first()
    assert image is None, "Additional image should be deleted when profile additional image is deleted"

################################################################################
def test_delete_profile_additional_image_by_id_invalid_guild(
    client, new_profile_id, new_profile_additional_image_id
):
    """Test deleting an additional image from a profile by ID for an invalid guild."""

    res = client.delete(f"/guilds/{INVALID_GUILD_ID}/profiles/{new_profile_id}/images/additional/{new_profile_additional_image_id}")
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_delete_profile_additional_image_by_id_invalid_profile(
    client, new_profile_additional_image_id
):
    """Test deleting an additional image from a profile by ID for an invalid profile."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/profiles/{INVALID_ID}/images/additional/{new_profile_additional_image_id}")
    assert res.status_code == 404, f"Expected 404 for non-existent profile, got {res.status_code}: {res.json()}"

################################################################################
def test_delete_profile_additional_image_by_id_invalid_id(
    client, new_profile_id, new_profile_additional_image_id
):
    """Test deleting an additional image from a profile by ID that does not exist."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/images/additional/{INVALID_ID}")
    assert res.status_code == 404, f"Expected 404 for non-existent additional image, got {res.status_code}: {res.json()}"

################################################################################
# PATCH Tests
################################################################################

PROFILE_REQUIREMENTS_PATCHABLE_FIELDS = {k: True for k in _requirements_keys}

################################################################################
def test_patch_profile_requirements(client):
    """Test patching profile requirements."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/")
    assert res.status_code == 200, f"Failed to get profile manager: {res.json()}"
    mgr = res.json()
    assert "requirements" in mgr, "Profile manager should have a 'requirements' field"
    assert_profile_requirement_default_data(mgr["requirements"])
    previous = mgr["requirements"]

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/requirements", json=PROFILE_REQUIREMENTS_PATCHABLE_FIELDS)
    assert res.status_code == 200, f"Failed to patch profile requirements: {res.json()}"
    current = res.json()
    for key in _requirements_keys:
        assert current[key] != previous[key], "Profile requirements should be updated after patch"

################################################################################
@pytest.mark.parametrize("field", _requirements_keys)
def test_patch_profile_requirements_single_field(client, field):
    """Test patching a single field in profile requirements."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/")
    assert res.status_code == 200, f"Failed to get profile manager: {res.json()}"
    mgr = res.json()
    assert "requirements" in mgr, "Profile manager should have a 'requirements' field"
    assert_profile_requirement_default_data(mgr["requirements"])
    previous = mgr["requirements"]

    payload = {field: True}
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/requirements", json=payload)
    assert res.status_code == 200, f"Failed to patch profile requirements: {res.json()}"
    current = res.json()

    for key in _requirements_keys:
        if key == field:
            assert current[key] != previous[key], f"Profile requirement {key} should be updated after patch"
        else:
            assert current[key] == previous[key], f"Profile requirement {key} should remain unchanged after patch"

################################################################################
def test_patch_profile_requirements_invalid_guild(client):
    """Test patching profile requirements for an invalid guild."""

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/profiles/requirements", json=PROFILE_REQUIREMENTS_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_profile_requirements_invalid_payload(client):
    """Test patching profile requirements with invalid data."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/requirements", json=INVALID_PAYLOAD)
    assert res.status_code == 422, f"Expected 422 for invalid data, got {res.status_code}: {res.json()}"

################################################################################

PROFILE_PATCHABLE_FIELDS = {
    "post_url": TEST_DISCORD_POST_URL
}

################################################################################
def test_patch_profile_full(client, new_profile_id):
    """Test patching a profile with all fields."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}")
    assert res.status_code == 200, f"Failed to get profile by ID: {res.json()}"
    existing = res.json()
    assert_profile_default_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}", json=PROFILE_PATCHABLE_FIELDS)
    assert res.status_code == 200, f"Failed to patch profile: {res.json()}"
    current = res.json()

    for key, value in PROFILE_PATCHABLE_FIELDS.items():
        assert key in current, f"Profile should have field '{key}' after patching"
        assert current[key] == value, f"Profile {key} did not update correctly: expected {value}, got {current[key]}"

################################################################################
@pytest.mark.parametrize("field", PROFILE_PATCHABLE_FIELDS.keys())
def test_patch_profile_partial(client, new_profile_id, field):
    """Test patching a profile with a single field."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}")
    assert res.status_code == 200, f"Failed to get profile by ID: {res.json()}"
    existing = res.json()
    assert_profile_default_data(existing)

    partial_update = {field: PROFILE_PATCHABLE_FIELDS[field]}
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}", json=partial_update)
    assert res.status_code == 200, f"Failed to patch profile: {res.json()}"
    current = res.json()

    for key, value in PROFILE_PATCHABLE_FIELDS.items():
        if key == field:
            assert current[key] == value, f"Profile {key} did not update correctly: expected {value}, got {current[key]}"
        else:
            assert current[key] == existing[key], f"Profile {key} should not have changed: expected {existing[key]}, got {current[key]}"

################################################################################
def test_patch_profile_invalid_guild(client, new_profile_id):
    """Test patching a profile for an invalid guild."""

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/profiles/{new_profile_id}", json=PROFILE_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_profile_invalid_profile(client, new_profile_id):
    """Test patching a profile that does not exist."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{INVALID_ID}", json=PROFILE_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for non-existent profile, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_profile_invalid_payload(client, new_profile_id):
    """Test patching a profile with invalid data."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}", json=INVALID_PAYLOAD)
    assert res.status_code == 422, f"Expected 422 for invalid fields, got {res.status_code}: {res.json()}"

################################################################################

PROFILE_DETAILS_PATCHABLE_FIELDS = {
    "name": TEST_TITLE,
    "custom_url": TEST_URL,
    "color": TEST_COLOR,
    "jobs": TEST_STRING_LIST,
    "rates": TEST_DESCRIPTION
}

################################################################################
def test_patch_profile_details_full(client, new_profile_id):
    """Test patching profile details with all fields."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}")
    assert res.status_code == 200, f"Failed to get profile by ID: {res.json()}"
    existing = res.json()
    assert_profile_default_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/details", json=PROFILE_DETAILS_PATCHABLE_FIELDS)
    assert res.status_code == 200, f"Failed to patch profile details: {res.json()}"
    current = res.json()

    for key, value in PROFILE_DETAILS_PATCHABLE_FIELDS.items():
        assert key in current, f"Profile details should have field '{key}' after patching"
        assert current[key] == value, f"Profile details {key} did not update correctly: expected {value}, got {current[key]}"
        assert current[key] != existing["details"][key], f"Profile details {key} should be updated after patching"

################################################################################
@pytest.mark.parametrize("field", PROFILE_DETAILS_PATCHABLE_FIELDS.keys())
def test_patch_profile_details_partial(client, new_profile_id, field):
    """Test patching profile details with a single field."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}")
    assert res.status_code == 200, f"Failed to get profile by ID: {res.json()}"
    existing = res.json()
    assert_profile_default_data(existing)

    partial_update = {field: PROFILE_DETAILS_PATCHABLE_FIELDS[field]}
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/details", json=partial_update)
    assert res.status_code == 200, f"Failed to patch profile details: {res.json()}"
    current = res.json()

    for key, value in PROFILE_DETAILS_PATCHABLE_FIELDS.items():
        if key == field:
            assert current[key] == value, f"Profile details {key} did not update correctly: expected {value}, got {current[key]}"
        else:
            assert current[key] == existing["details"][key], f"Profile details {key} should not have changed: expected {existing['details'][key]}, got {current[key]}"

################################################################################
def test_patch_profile_details_invalid_guild(client, new_profile_id):
    """Test patching profile details for an invalid guild."""

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/profiles/{new_profile_id}/details", json=PROFILE_DETAILS_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_profile_details_invalid_profile(client, new_profile_id):
    """Test patching profile details for a profile that does not exist."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{INVALID_ID}/details", json=PROFILE_DETAILS_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for non-existent profile, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_profile_details_invalid_payload(client, new_profile_id):
    """Test patching profile details with invalid data."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/details", json=INVALID_PAYLOAD)
    assert res.status_code == 422, f"Expected 422 for invalid fields, got {res.status_code}: {res.json()}"

################################################################################

PROFILE_ATAGLANCE_PATCHABLE_FIELDS = {
    "world": 5,
    "gender_enum": 2,
    "pronouns": [4, 5, 6],
    "race_enum": 3,
    "clan_enum": 1,
    "orientation_enum": 2,
    "race_custom": TEST_TITLE,
    "clan_custom": TEST_TITLE,
    "orientation_custom": TEST_TITLE,
    "height": 133,
    "age": "Older than you think",
    "mare": "Frogge"
}

################################################################################
def test_patch_profile_ataglance_full(client, new_profile_id):
    """Test patching profile ataglance with all fields."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}")
    assert res.status_code == 200, f"Failed to get profile by ID: {res.json()}"
    existing = res.json()
    assert_profile_default_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/at-a-glance", json=PROFILE_ATAGLANCE_PATCHABLE_FIELDS)
    assert res.status_code == 200, f"Failed to patch profile ataglance: {res.json()}"
    current = res.json()

    for key, value in PROFILE_ATAGLANCE_PATCHABLE_FIELDS.items():
        assert key in current, f"Profile ataglance should have field '{key}' after patching"
        assert current[key] == value, f"Profile ataglance {key} did not update correctly: expected {value}, got {current[key]}"
        assert current[key] != existing["ataglance"][key], f"Profile ataglance {key} should be updated after patching"

################################################################################
@pytest.mark.parametrize("field", PROFILE_ATAGLANCE_PATCHABLE_FIELDS.keys())
def test_patch_profile_ataglance_partial(client, new_profile_id, field):
    """Test patching profile ataglance with a single field."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}")
    assert res.status_code == 200, f"Failed to get profile by ID: {res.json()}"
    existing = res.json()
    assert_profile_default_data(existing)

    partial_update = {field: PROFILE_ATAGLANCE_PATCHABLE_FIELDS[field]}
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/at-a-glance", json=partial_update)
    assert res.status_code == 200, f"Failed to patch profile ataglance: {res.json()}"
    current = res.json()

    for key, value in PROFILE_ATAGLANCE_PATCHABLE_FIELDS.items():
        if key == field:
            assert current[key] == value, f"Profile ataglance {key} did not update correctly: expected {value}, got {current[key]}"
        else:
            assert current[key] == existing["ataglance"][key], f"Profile ataglance {key} should not have changed: expected {existing['ataglance'][key]}, got {current[key]}"

################################################################################
def test_patch_profile_ataglance_invalid_guild(client, new_profile_id):
    """Test patching profile ataglance for an invalid guild."""

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/profiles/{new_profile_id}/at-a-glance", json=PROFILE_ATAGLANCE_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_profile_ataglance_invalid_profile(client, new_profile_id):
    """Test patching profile ataglance for a profile that does not exist."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{INVALID_ID}/at-a-glance", json=PROFILE_ATAGLANCE_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for non-existent profile, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_profile_ataglance_invalid_payload(client, new_profile_id):
    """Test patching profile ataglance with invalid data."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/at-a-glance", json=INVALID_PAYLOAD)
    assert res.status_code == 422, f"Expected 422 for invalid fields, got {res.status_code}: {res.json()}"

################################################################################

PROFILE_PERSONALITY_PATCHABLE_FIELDS = {
    "likes": TEST_STRING_LIST,
    "dislikes": TEST_STRING_LIST,
    "personality": TEST_DESCRIPTION,
    "aboutme": TEST_DESCRIPTION
}

################################################################################
def test_patch_profile_personality_full(client, new_profile_id):
    """Test patching profile personality with all fields."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}")
    assert res.status_code == 200, f"Failed to get profile by ID: {res.json()}"
    existing = res.json()
    assert_profile_default_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/personality", json=PROFILE_PERSONALITY_PATCHABLE_FIELDS)
    assert res.status_code == 200, f"Failed to patch profile personality: {res.json()}"
    current = res.json()

    for key, value in PROFILE_PERSONALITY_PATCHABLE_FIELDS.items():
        assert key in current, f"Profile personality should have field '{key}' after patching"
        assert current[key] == value, f"Profile personality {key} did not update correctly: expected {value}, got {current[key]}"
        assert current[key] != existing["personality"][key], f"Profile personality {key} should be updated after patching"

################################################################################
@pytest.mark.parametrize("field", PROFILE_PERSONALITY_PATCHABLE_FIELDS.keys())
def test_patch_profile_personality_partial(client, new_profile_id, field):
    """Test patching profile personality with a single field."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}")
    assert res.status_code == 200, f"Failed to get profile by ID: {res.json()}"
    existing = res.json()
    assert_profile_default_data(existing)

    partial_update = {field: PROFILE_PERSONALITY_PATCHABLE_FIELDS[field]}
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/personality", json=partial_update)
    assert res.status_code == 200, f"Failed to patch profile personality: {res.json()}"
    current = res.json()

    for key, value in PROFILE_PERSONALITY_PATCHABLE_FIELDS.items():
        if key == field:
            assert current[key] == value, f"Profile personality {key} did not update correctly: expected {value}, got {current[key]}"
        else:
            assert current[key] == existing["personality"][key], f"Profile personality {key} should not have changed: expected {existing['personality'][key]}, got {current[key]}"

################################################################################
def test_patch_profile_personality_invalid_guild(client, new_profile_id):
    """Test patching profile personality for an invalid guild."""

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/profiles/{new_profile_id}/personality", json=PROFILE_PERSONALITY_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_profile_personality_invalid_profile(client, new_profile_id):
    """Test patching profile personality for a profile that does not exist."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{INVALID_ID}/personality", json=PROFILE_PERSONALITY_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for non-existent profile, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_profile_personality_invalid_payload(client, new_profile_id):
    """Test patching profile personality with invalid data."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/personality", json=INVALID_PAYLOAD)
    assert res.status_code == 422, f"Expected 422 for invalid fields, got {res.status_code}: {res.json()}"

################################################################################

PROFILE_IMAGES_PATCHABLE_FIELDS = {
    "thumbnail_url": TEST_IMAGE_URL_DISCORD,
    "main_image_url": TEST_IMAGE_URL_DISCORD,
}

################################################################################
def test_patch_profile_images_full(client, new_profile_id):
    """Test patching profile images with all fields."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}")
    assert res.status_code == 200, f"Failed to get profile by ID: {res.json()}"
    existing = res.json()
    assert_profile_default_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/images", json=PROFILE_IMAGES_PATCHABLE_FIELDS)
    assert res.status_code == 200, f"Failed to patch profile images: {res.json()}"
    current = res.json()

    for key, value in PROFILE_IMAGES_PATCHABLE_FIELDS.items():
        assert key in current, f"Profile images should have field '{key}' after patching"
        assert current[key] == value, f"Profile images {key} did not update correctly: expected {value}, got {current[key]}"
        assert current[key] != existing["images"][key], f"Profile images {key} should be updated after patching"

################################################################################
@pytest.mark.parametrize("field", PROFILE_IMAGES_PATCHABLE_FIELDS.keys())
def test_patch_profile_images_partial(client, new_profile_id, field):
    """Test patching profile images with a single field."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}")
    assert res.status_code == 200, f"Failed to get profile by ID: {res.json()}"
    existing = res.json()
    assert_profile_default_data(existing)

    partial_update = {field: PROFILE_IMAGES_PATCHABLE_FIELDS[field]}
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/images", json=partial_update)
    assert res.status_code == 200, f"Failed to patch profile images: {res.json()}"
    current = res.json()

    for key, value in PROFILE_IMAGES_PATCHABLE_FIELDS.items():
        if key == field:
            assert current[key] == value, f"Profile images {key} did not update correctly: expected {value}, got {current[key]}"
        else:
            assert current[key] == existing["images"][key], f"Profile images {key} should not have changed: expected {existing['images'][key]}, got {current[key]}"

################################################################################
def test_patch_profile_images_invalid_guild(client, new_profile_id):
    """Test patching profile images for an invalid guild."""

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/profiles/{new_profile_id}/images", json=PROFILE_IMAGES_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_profile_images_invalid_profile(client, new_profile_id):
    """Test patching profile images for a profile that does not exist."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{INVALID_ID}/images", json=PROFILE_IMAGES_PATCHABLE_FIELDS)
    assert res.status_code == 404, f"Expected 404 for non-existent profile, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_profile_images_invalid_payload(client, new_profile_id):
    """Test patching profile images with invalid data."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/images", json=INVALID_PAYLOAD)
    assert res.status_code == 422, f"Expected 422 for invalid fields, got {res.status_code}: {res.json()}"

################################################################################

PROFILE_ADDITIONAL_IMAGE_PATCHABLE_FIELDS = {
    "caption": TEST_TITLE,
}

################################################################################
def test_patch_profile_additional_image_full(client, new_profile_id, new_profile_additional_image_id):
    """Test patching an additional image for a profile with all fields."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/")
    assert res.status_code == 200, f"Failed to get additional image by ID: {res.json()}"
    existing = res.json()["images"]["addl_images"][0]
    assert_profile_additional_image_default_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/images/additional/{new_profile_additional_image_id}", json=PROFILE_ADDITIONAL_IMAGE_PATCHABLE_FIELDS)
    assert res.status_code == 200, f"Failed to patch additional image: {res.json()}"
    current = res.json()

    for key, value in PROFILE_ADDITIONAL_IMAGE_PATCHABLE_FIELDS.items():
        assert key in current, f"Additional image should have field '{key}' after patching"
        assert current[key] == value, f"Additional image {key} did not update correctly: expected {value}, got {current[key]}"
        assert current[key] != existing[key], f"Additional image {key} should be updated after patching"

################################################################################
@pytest.mark.parametrize("field", PROFILE_ADDITIONAL_IMAGE_PATCHABLE_FIELDS.keys())
def test_patch_profile_additional_image_partial(client, new_profile_id, new_profile_additional_image_id, field):
    """Test patching an additional image for a profile with a single field."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/")
    assert res.status_code == 200, f"Failed to get additional image by ID: {res.json()}"
    existing = res.json()["images"]["addl_images"][0]
    assert_profile_additional_image_default_data(existing)

    partial_update = {field: PROFILE_ADDITIONAL_IMAGE_PATCHABLE_FIELDS[field]}
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/images/additional/{new_profile_additional_image_id}", json=partial_update)
    assert res.status_code == 200, f"Failed to patch additional image: {res.json()}"
    current = res.json()

    for key, value in PROFILE_ADDITIONAL_IMAGE_PATCHABLE_FIELDS.items():
        if key == field:
            assert current[key] == value, f"Additional image {key} did not update correctly: expected {value}, got {current[key]}"
        else:
            assert current[key] == existing[key], f"Additional image {key} should not have changed: expected {existing[key]}, got {current[key]}"

################################################################################
def test_patch_profile_additional_image_invalid_guild(client, new_profile_id, new_profile_additional_image_id):
    """Test patching an additional image for a profile with an invalid guild."""

    res = client.patch(
        f"/guilds/{INVALID_GUILD_ID}/profiles/{new_profile_id}/images/additional/{new_profile_additional_image_id}",
        json=PROFILE_ADDITIONAL_IMAGE_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_profile_additional_image_invalid_profile(client, new_profile_additional_image_id):
    """Test patching an additional image for a profile that does not exist."""

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/profiles/{INVALID_ID}/images/additional/{new_profile_additional_image_id}",
        json=PROFILE_ADDITIONAL_IMAGE_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, f"Expected 404 for non-existent profile, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_profile_additional_image_invalid_id(client, new_profile_id, new_profile_additional_image_id):
    """Test patching an additional image for a profile with an invalid ID."""

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/images/additional/{INVALID_ID}",
        json=PROFILE_ADDITIONAL_IMAGE_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, f"Expected 404 for non-existent additional image, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_profile_additional_image_invalid_payload(client, new_profile_id, new_profile_additional_image_id):
    """Test patching an additional image for a profile with invalid data."""

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/profiles/{new_profile_id}/images/additional/{new_profile_additional_image_id}",
        json=INVALID_PAYLOAD
    )
    assert res.status_code == 422, f"Expected 422 for invalid fields, got {res.status_code}: {res.json()}"

################################################################################

PROFILE_CHANNEL_GROUP_PATCHABLE_FIELDS = {
    "channel_ids": [TEST_CHANNEL_ID, TEST_CHANNEL_ID2],
    "role_ids": [TEST_ROLE_ID, TEST_ROLE_ID2],
}

################################################################################
def test_patch_profile_channel_group_full(client, new_profile_channel_group_id):
    """Test patching profile channel group with all fields."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/")
    assert res.status_code == 200, f"Failed to get profile by ID: {res.json()}"
    existing = res.json()["channel_groups"][0]
    assert_profile_channel_group_default_data(existing)

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/profiles/channel-groups/{new_profile_channel_group_id}",
        json=PROFILE_CHANNEL_GROUP_PATCHABLE_FIELDS
    )
    assert res.status_code == 200, f"Failed to patch profile channel group: {res.json()}"
    current = res.json()

    for key, value in PROFILE_CHANNEL_GROUP_PATCHABLE_FIELDS.items():
        assert key in current, f"Profile channel group should have field '{key}' after patching"
        assert current[key] == value, f"Profile channel group {key} did not update correctly: expected {value}, got {current[key]}"
        assert current[key] != existing[key], f"Profile channel group {key} should be updated after patching"

################################################################################
@pytest.mark.parametrize("field", PROFILE_CHANNEL_GROUP_PATCHABLE_FIELDS.keys())
def test_patch_profile_channel_group_partial(client, new_profile_channel_group_id, field):
    """Test patching profile channel group with a single field."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/profiles/")
    assert res.status_code == 200, f"Failed to get profile by ID: {res.json()}"
    existing = res.json()["channel_groups"][0]
    assert_profile_channel_group_default_data(existing)

    partial_update = {field: PROFILE_CHANNEL_GROUP_PATCHABLE_FIELDS[field]}
    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/profiles/channel-groups/{new_profile_channel_group_id}/",
        json=partial_update
    )
    assert res.status_code == 200, f"Failed to patch profile channel group: {res.json()}"
    current = res.json()

    for key, value in PROFILE_CHANNEL_GROUP_PATCHABLE_FIELDS.items():
        if key == field:
            assert current[key] == value, f"Profile channel group {key} did not update correctly: expected {value}, got {current[key]}"
        else:
            assert current[key] == existing[key], f"Profile channel group {key} should not have changed: expected {existing[key]}, got {current[key]}"

################################################################################
def test_patch_profile_channel_group_invalid_guild(client, new_profile_channel_group_id):
    """Test patching profile channel group for an invalid guild."""

    res = client.patch(
        f"/guilds/{INVALID_GUILD_ID}/profiles/channel-groups/{new_profile_channel_group_id}",
        json=PROFILE_CHANNEL_GROUP_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, f"Expected 404 for invalid guild, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_profile_channel_group_invalid_id(client, new_profile_channel_group_id):
    """Test patching profile channel group with an invalid ID."""

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/profiles/channel-groups/{INVALID_ID}",
        json=PROFILE_CHANNEL_GROUP_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, f"Expected 404 for non-existent channel group, got {res.status_code}: {res.json()}"

################################################################################
def test_patch_profile_channel_group_invalid_payload(client, new_profile_channel_group_id):
    """Test patching profile channel group with invalid data."""

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/profiles/channel-groups/{new_profile_channel_group_id}",
        json=INVALID_PAYLOAD
    )
    assert res.status_code == 422, f"Expected 422 for invalid fields, got {res.status_code}: {res.json()}"

################################################################################
