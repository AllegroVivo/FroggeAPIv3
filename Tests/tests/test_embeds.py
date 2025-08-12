import pytest

from ..payloads import *

from App import limits
################################################################################
@pytest.fixture(scope="function")
def new_embed_id(client):
    """Create a new embed for testing purposes. Asserts the "happy path" of creating an embed."""

    res = client.post(f"/guilds/{TEST_GUILD_ID}/embeds/", json=BASE_CREATE_ITEM_PAYLOAD)
    assert res.status_code == 201, "Should create a new embed successfully"
    embed = res.json()
    assert_default_embed_data(embed)
    yield embed["id"]

################################################################################
@pytest.fixture(scope="function")
def new_embed_field_id(client, new_embed_id):
    """
    Create a new embed field for testing purposes. Asserts the "happy path"
    of creating an embed field.
    """

    res = client.post(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/fields/", json=BASE_CREATE_ITEM_PAYLOAD)
    assert res.status_code == 201, "Should create a new embed field successfully"
    field = res.json()
    assert_default_embed_field_data(field)
    yield field["id"]

################################################################################
def assert_default_embed_data(e):
    """Assert that the embed has the required fields."""

    assert "id" in e, "Embed should have an ID"
    assert isinstance(e["id"], int), "Embed ID should be an integer"
    assert "title" in e, "Embed should have a title field"
    assert e["title"] is None, "Title should be None by default"
    assert "description" in e, "Embed should have a description field"
    assert e["description"] is None, "Description should be None by default"
    assert "color" in e, "Embed should have a color field"
    assert e["color"] is None, "Color should be None by default"
    assert "url" in e, "Embed should have a URL field"
    assert e["url"] is None, "URL should be None by default"
    assert "timestamp" in e, "Embed should have a timestamp field"
    assert e["timestamp"] is None, "Timestamp should be None by default"
    assert "images" in e, "Embed should have an images field"
    assert_default_embed_images_data(e["images"])
    assert "header" in e, "Embed should have a header field"
    assert_default_embed_header_data(e["header"])
    assert "footer" in e, "Embed should have a footer field"
    assert_default_embed_footer_data(e["footer"])
    assert "fields" in e, "Embed should have a fields field"
    assert isinstance(e["fields"], list), "Embed fields should be a list"
    assert len(e["fields"]) == 0, "Embed fields should be an empty list by default"

################################################################################
def assert_default_embed_images_data(images):
    """Assert that the embed images have the required fields."""

    assert images is not None, "Embed images should not be None"
    assert isinstance(images, dict), "Embed images should be a dict"
    assert "thumbnail_url" in images, "Embed images should have a thumbnail_url field"
    assert images["thumbnail_url"] is None, "Thumbnail URL should be None by default"
    assert "main_image_url" in images, "Embed images should have a main_image_url field"
    assert images["main_image_url"] is None, "Main image URL should be None by default"

################################################################################
def assert_default_embed_header_data(header):
    """Assert that the embed header has the required fields."""

    assert header is not None, "Embed header should not be None"
    assert isinstance(header, dict), "Embed header should be a dictionary"
    assert "text" in header, "Embed header should have a text field"
    assert header["text"] is None, "Header text should be None by default"
    assert "icon_url" in header, "Embed header should have an icon_url field"
    assert header["icon_url"] is None, "Header icon URL should be None by default"
    assert "url" in header, "Embed header should have a url field"
    assert header["url"] is None, "Header URL should be None by default"

################################################################################
def assert_default_embed_footer_data(footer):
    """Assert that the embed footer has the required fields."""

    assert footer is not None, "Embed footer should not be None"
    assert isinstance(footer, dict), "Embed footer should be a dictionary"
    assert "text" in footer, "Embed footer should have a text field"
    assert footer["text"] is None, "Footer text should be None by default"
    assert "icon_url" in footer, "Embed footer should have an icon_url field"
    assert footer["icon_url"] is None, "Footer icon URL should be None by default"

################################################################################
def assert_default_embed_field_data(f):
    """Assert that the embed field has the required fields."""

    assert "id" in f, "Embed field should have an ID"
    assert isinstance(f["id"], int), "Embed field ID should be an integer"
    assert "name" in f, "Embed field should have a name"
    assert f["name"] is None, "Embed field name should be None by default"
    assert "value" in f, "Embed field should have a value"
    assert f["value"] is None, "Embed field value should be None by default"
    assert "inline" in f, "Embed field should have an inline field"
    assert f["inline"] is False, "Embed field inline should be False by default"
    assert "sort_order" in f, "Embed field should have a sort_order field"
    assert isinstance(f["sort_order"], int), "Embed field sort_order should be an integer"
    assert f["sort_order"] == 0, "Embed field sort_order should be zero by default"

################################################################################
def test_get_all_embeds(client, new_embed_id):
    """Test retrieving all embeds for a guild."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/embeds/")
    assert res.status_code == 200, "Should retrieve all embeds successfully"
    embeds = res.json()
    assert isinstance(embeds, list), "Response should be a list of embeds"
    assert len(embeds) == 1, "Should have one embed"
    assert_default_embed_data(embeds[0])

################################################################################
def test_get_all_embeds_invalid_guild(client):
    """Test retrieving all embeds for an invalid guild ID."""

    res = client.get(f"/guilds/{INVALID_GUILD_ID}/embeds/")
    assert res.status_code == 404, "Should return 404 for invalid guild ID"

################################################################################
def test_get_embed(client, new_embed_id):
    """Test retrieving an embed by ID."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/")
    assert res.status_code == 200, "Should retrieve the embed successfully"
    embed = res.json()
    assert_default_embed_data(embed)

################################################################################
def test_get_embed_invalid_guild(client, new_embed_id):
    """Test retrieving an embed by ID with an invalid guild ID."""

    res = client.get(f"/guilds/{INVALID_GUILD_ID}/embeds/{new_embed_id}/")
    assert res.status_code == 404, "Should return 404 for invalid guild ID"

################################################################################
def test_get_embed_invalid_embed(client, new_embed_id):
    """Test retrieving an embed by ID with an invalid embed ID."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/embeds/{INVALID_ID}/")
    assert res.status_code == 404, "Should return 404 for invalid embed ID"

################################################################################
def test_post_embed(client):
    """Test creating a new embed."""

    res = client.post(f"/guilds/{TEST_GUILD_ID}/embeds/")
    assert res.status_code == 201, "Should create a new embed successfully"
    embed = res.json()
    assert_default_embed_data(embed)

################################################################################
def test_post_embed_invalid_guild(client):
    """Test creating a new embed with an invalid guild ID."""

    res = client.post(f"/guilds/{INVALID_GUILD_ID}/embeds/")
    assert res.status_code == 404, "Should return 404 for invalid guild ID"

################################################################################
def test_post_embed_field(client, new_embed_id):
    """Test creating a new embed field."""

    res = client.post(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/fields/")
    assert res.status_code == 201, "Should create a new embed field successfully"
    field = res.json()
    assert_default_embed_field_data(field)

################################################################################
def test_post_embed_field_invalid_guild(client, new_embed_id):
    """Test creating a new embed field with an invalid guild ID."""

    res = client.post(f"/guilds/{INVALID_GUILD_ID}/embeds/{new_embed_id}/fields/")
    assert res.status_code == 404, "Should return 404 for invalid guild ID"

################################################################################
def test_post_embed_field_invalid_embed(client, new_embed_id):
    """Test creating a new embed field with an invalid embed ID."""

    res = client.post(f"/guilds/{TEST_GUILD_ID}/embeds/{INVALID_ID}/fields/")
    assert res.status_code == 404, "Should return 404 for invalid embed ID"

################################################################################
def test_delete_embed(client, new_embed_id):
    """Test deleting an embed by ID."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/")
    assert res.status_code == 204, "Should delete the embed successfully"

    res = client.get(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/")
    assert res.status_code == 404, "Should return 404 for deleted embed"

################################################################################
def test_delete_embed_invalid_guild(client, new_embed_id):
    """Test deleting an embed by ID with an invalid guild ID."""

    res = client.delete(f"/guilds/{INVALID_GUILD_ID}/embeds/{new_embed_id}/")
    assert res.status_code == 404, "Should return 404 for invalid guild ID"

################################################################################
def test_delete_embed_invalid_embed(client, new_embed_id):
    """Test deleting an embed by ID with an invalid embed ID."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/embeds/{INVALID_ID}/")
    assert res.status_code == 404, "Should return 404 for invalid embed ID"

################################################################################
def test_delete_embed_field(client, new_embed_id, new_embed_field_id):
    """Test deleting an embed field by ID."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/fields/{new_embed_field_id}/")
    assert res.status_code == 204, "Should delete the embed field successfully"

    res = client.get(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/fields/{new_embed_field_id}/")
    assert res.status_code == 404, "Should return 404 for deleted embed field"

################################################################################
def test_delete_embed_field_invalid_guild(client, new_embed_id, new_embed_field_id):
    """Test deleting an embed field by ID with an invalid guild ID."""

    res = client.delete(f"/guilds/{INVALID_GUILD_ID}/embeds/{new_embed_id}/fields/{new_embed_field_id}/")
    assert res.status_code == 404, "Should return 404 for invalid guild ID"

################################################################################
def test_delete_embed_field_invalid_embed(client, new_embed_id, new_embed_field_id):
    """Test deleting an embed field by ID with an invalid embed ID."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/embeds/{INVALID_ID}/fields/{new_embed_field_id}/")
    assert res.status_code == 404, "Should return 404 for invalid embed ID"

################################################################################
def test_delete_embed_field_invalid_field(client, new_embed_id, new_embed_field_id):
    """Test deleting an embed field by ID with an invalid field ID."""

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/fields/{INVALID_ID}/")
    assert res.status_code == 404, "Should return 404 for invalid field ID"

################################################################################

EMBED_PATCHABLE_FIELDS = {
    "title": TEST_TITLE,
    "description": TEST_DESCRIPTION,
    "color": TEST_COLOR,
    "url": TEST_URL,
    "timestamp": TEST_TIMESTAMP,
}

################################################################################
def test_patch_embed_full(client, new_embed_id):
    """Test updating an embed by ID."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/")
    assert res.status_code == 200, "Should retrieve the existing embed successfully"
    existing = res.json()
    assert_default_embed_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/", json=EMBED_PATCHABLE_FIELDS)
    assert res.status_code == 200, "Should update the embed successfully"
    updated = res.json()
    for key in EMBED_PATCHABLE_FIELDS.keys():
        assert updated[key] == EMBED_PATCHABLE_FIELDS[key], f"Embed {key} should be updated correctly"
        assert existing[key] != updated[key], f"Embed {key} should be changed from {existing[key]} to {updated[key]}"

################################################################################
@pytest.mark.parametrize("field", EMBED_PATCHABLE_FIELDS.keys())
def test_patch_embed_partial(client, new_embed_id, field):
    """Test updating a single field of an embed by ID."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/")
    assert res.status_code == 200, "Should retrieve the existing embed successfully"
    existing = res.json()
    assert_default_embed_data(existing)

    payload = {field: EMBED_PATCHABLE_FIELDS[field]}
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/", json=payload)
    assert res.status_code == 200, "Should update the embed successfully"
    updated = res.json()
    assert updated[field] == EMBED_PATCHABLE_FIELDS[field], f"Embed {field} should be updated correctly"
    assert existing[field] != updated[field], f"Embed {field} should be changed from {existing[field]} to {updated[field]}"

################################################################################
def test_patch_embed_invalid_guild(client, new_embed_id):
    """Test updating an embed by ID with an invalid guild ID."""

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/embeds/{new_embed_id}/", json=EMBED_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Should return 404 for invalid guild ID"

################################################################################
def test_patch_embed_invalid_embed(client, new_embed_id):
    """Test updating an embed by ID with an invalid embed ID."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{INVALID_ID}/", json=EMBED_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Should return 404 for invalid embed ID"

################################################################################
def test_patch_embed_invalid_payload(client, new_embed_id):
    """Test updating an embed by ID with an invalid payload."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/", json=INVALID_PAYLOAD)
    assert res.status_code == 422, "Should return 422 for invalid payload"

################################################################################

EMBED_IMAGES_PATCHABLE_FIELDS = {
    "thumbnail_url": TEST_IMAGE_URL_DISCORD,
    "main_image_url": TEST_IMAGE_URL_DISCORD,
}

################################################################################
def teat_patch_embed_images_full(client, new_embed_id):
    """Test updating embed images."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/")
    assert res.status_code == 200, "Should retrieve the existing embed successfully"
    existing = res.json()
    assert_default_embed_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/images/", json=EMBED_IMAGES_PATCHABLE_FIELDS)
    assert res.status_code == 200, "Should update the embed images successfully"
    updated = res.json()
    for key in EMBED_IMAGES_PATCHABLE_FIELDS.keys():
        assert updated["images"][key] == EMBED_IMAGES_PATCHABLE_FIELDS[key], f"Embed image {key} should be updated correctly"
        assert existing["images"][key] != updated["images"][key], f"Embed image {key} should be changed from {existing['images'][key]} to {updated['images'][key]}"

################################################################################
@pytest.mark.parametrize("field", EMBED_IMAGES_PATCHABLE_FIELDS.keys())
def test_patch_embed_images_partial(client, new_embed_id, field):
    """Test updating a single field of embed images."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/")
    assert res.status_code == 200, "Should retrieve the existing embed successfully"
    existing = res.json()
    assert_default_embed_data(existing)

    payload = {field: EMBED_IMAGES_PATCHABLE_FIELDS[field]}
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/images/", json=payload)
    assert res.status_code == 200, "Should update the embed images successfully"
    updated = res.json()
    assert updated[field] == EMBED_IMAGES_PATCHABLE_FIELDS[field], f"Embed image {field} should be updated correctly"
    assert existing["images"][field] != updated[field], f"Embed image {field} should be changed from {existing['images'][field]} to {updated[field]}"

################################################################################
def test_patch_embed_images_invalid_guild(client, new_embed_id):
    """Test updating embed images with an invalid guild ID."""

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/embeds/{new_embed_id}/images/", json=EMBED_IMAGES_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Should return 404 for invalid guild ID"

################################################################################
def test_patch_embed_images_invalid_embed(client, new_embed_id):
    """Test updating embed images with an invalid embed ID."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{INVALID_ID}/images/", json=EMBED_IMAGES_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Should return 404 for invalid embed ID"

################################################################################
def test_patch_embed_images_invalid_payload(client, new_embed_id):
    """Test updating embed images with an invalid payload."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/images/", json=INVALID_PAYLOAD)
    assert res.status_code == 422, "Should return 422 for invalid payload"

################################################################################

EMBED_HEADER_PATCHABLE_FIELDS = {
    "text": TEST_TITLE,
    "icon_url": TEST_IMAGE_URL_DISCORD,
    "url": TEST_URL,
}

################################################################################
def test_patch_embed_header_full(client, new_embed_id):
    """Test updating embed header."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/")
    assert res.status_code == 200, "Should retrieve the existing embed successfully"
    existing = res.json()
    assert_default_embed_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/header/", json=EMBED_HEADER_PATCHABLE_FIELDS)
    assert res.status_code == 200, "Should update the embed header successfully"
    updated = res.json()
    for key in EMBED_HEADER_PATCHABLE_FIELDS.keys():
        assert updated[key] == EMBED_HEADER_PATCHABLE_FIELDS[key], f"Embed header {key} should be updated correctly"
        assert existing["header"][key] != updated[key], f"Embed header {key} should be changed from {existing['header'][key]} to {updated[key]}"

################################################################################
@pytest.mark.parametrize("field", EMBED_HEADER_PATCHABLE_FIELDS.keys())
def test_patch_embed_header_partial(client, new_embed_id, field):
    """Test updating a single field of embed header."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/")
    assert res.status_code == 200, "Should retrieve the existing embed successfully"
    existing = res.json()
    assert_default_embed_data(existing)

    payload = {field: EMBED_HEADER_PATCHABLE_FIELDS[field]}
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/header/", json=payload)
    assert res.status_code == 200, "Should update the embed header successfully"
    updated = res.json()
    assert updated[field] == EMBED_HEADER_PATCHABLE_FIELDS[field], f"Embed header {field} should be updated correctly"
    assert existing["header"][field] != updated[field], f"Embed header {field} should be changed from {existing['header'][field]} to {updated[field]}"

################################################################################
def test_patch_embed_header_invalid_guild(client, new_embed_id):
    """Test updating embed header with an invalid guild ID."""

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/embeds/{new_embed_id}/header/", json=EMBED_HEADER_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Should return 404 for invalid guild ID"

################################################################################
def test_patch_embed_header_invalid_embed(client, new_embed_id):
    """Test updating embed header with an invalid embed ID."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{INVALID_ID}/header/", json=EMBED_HEADER_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Should return 404 for invalid embed ID"

################################################################################
def test_patch_embed_header_invalid_payload(client, new_embed_id):
    """Test updating embed header with an invalid payload."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/header/", json=INVALID_PAYLOAD)
    assert res.status_code == 422, "Should return 422 for invalid payload"

################################################################################

EMBED_FOOTER_PATCHABLE_FIELDS = {
    "text": TEST_DESCRIPTION,
    "icon_url": TEST_IMAGE_URL_DISCORD,
}

################################################################################
def test_patch_embed_footer_full(client, new_embed_id):
    """Test updating embed footer."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/")
    assert res.status_code == 200, "Should retrieve the existing embed successfully"
    existing = res.json()
    assert_default_embed_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/footer/", json=EMBED_FOOTER_PATCHABLE_FIELDS)
    assert res.status_code == 200, "Should update the embed footer successfully"
    updated = res.json()
    for key in EMBED_FOOTER_PATCHABLE_FIELDS.keys():
        assert updated[key] == EMBED_FOOTER_PATCHABLE_FIELDS[key], f"Embed footer {key} should be updated correctly"
        assert existing["footer"][key] != updated[key], f"Embed footer {key} should be changed from {existing['footer'][key]} to {updated[key]}"

################################################################################
@pytest.mark.parametrize("field", EMBED_FOOTER_PATCHABLE_FIELDS.keys())
def test_patch_embed_footer_partial(client, new_embed_id, field):
    """Test updating a single field of embed footer."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/")
    assert res.status_code == 200, "Should retrieve the existing embed successfully"
    existing = res.json()
    assert_default_embed_data(existing)

    payload = {field: EMBED_FOOTER_PATCHABLE_FIELDS[field]}
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/footer/", json=payload)
    assert res.status_code == 200, "Should update the embed footer successfully"
    updated = res.json()
    assert updated[field] == EMBED_FOOTER_PATCHABLE_FIELDS[field], f"Embed footer {field} should be updated correctly"
    assert existing["footer"][field] != updated[field], f"Embed footer {field} should be changed from {existing['footer'][field]} to {updated[field]}"

################################################################################
def test_patch_embed_footer_invalid_guild(client, new_embed_id):
    """Test updating embed footer with an invalid guild ID."""

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/embeds/{new_embed_id}/footer/", json=EMBED_FOOTER_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Should return 404 for invalid guild ID"

################################################################################
def test_patch_embed_footer_invalid_embed(client, new_embed_id):
    """Test updating embed footer with an invalid embed ID."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{INVALID_ID}/footer/", json=EMBED_FOOTER_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Should return 404 for invalid embed ID"

################################################################################
def test_patch_embed_footer_invalid_payload(client, new_embed_id):
    """Test updating embed footer with an invalid payload."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/footer/", json=INVALID_PAYLOAD)
    assert res.status_code == 422, "Should return 422 for invalid payload"

################################################################################

EMBED_FIELD_PATCHABLE_FIELDS = {
    "name": TEST_TITLE,
    "value": TEST_DESCRIPTION,
    "inline": True,
    "sort_order": 1,
}

################################################################################
def test_patch_embed_field_full(client, new_embed_id, new_embed_field_id):
    """Test updating an embed field by ID."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/fields/{new_embed_field_id}/")
    assert res.status_code == 200, "Should retrieve the existing embed field successfully"
    existing = res.json()
    assert_default_embed_field_data(existing)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/fields/{new_embed_field_id}/", json=EMBED_FIELD_PATCHABLE_FIELDS)
    assert res.status_code == 200, "Should update the embed field successfully"
    updated = res.json()
    for key in EMBED_FIELD_PATCHABLE_FIELDS.keys():
        assert updated[key] == EMBED_FIELD_PATCHABLE_FIELDS[key], f"Embed field {key} should be updated correctly"
        assert existing[key] != updated[key], f"Embed field {key} should be changed from {existing[key]} to {updated[key]}"

################################################################################
@pytest.mark.parametrize("field", EMBED_FIELD_PATCHABLE_FIELDS.keys())
def test_patch_embed_field_partial(client, new_embed_id, new_embed_field_id, field):
    """Test updating a single field of an embed field by ID."""

    res = client.get(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/fields/{new_embed_field_id}/")
    assert res.status_code == 200, "Should retrieve the existing embed field successfully"
    existing = res.json()
    assert_default_embed_field_data(existing)

    payload = {field: EMBED_FIELD_PATCHABLE_FIELDS[field]}
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/fields/{new_embed_field_id}/", json=payload)
    assert res.status_code == 200, "Should update the embed field successfully"
    updated = res.json()
    assert updated[field] == EMBED_FIELD_PATCHABLE_FIELDS[field], f"Embed field {field} should be updated correctly"
    assert existing[field] != updated[field], f"Embed field {field} should be changed from {existing[field]} to {updated[field]}"

################################################################################
def test_patch_embed_field_invalid_guild(client, new_embed_id, new_embed_field_id):
    """Test updating an embed field by ID with an invalid guild ID."""

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/embeds/{new_embed_id}/fields/{new_embed_field_id}/", json=EMBED_FIELD_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Should return 404 for invalid guild ID"

################################################################################
def test_patch_embed_field_invalid_embed(client, new_embed_id, new_embed_field_id):
    """Test updating an embed field by ID with an invalid embed ID."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{INVALID_ID}/fields/{new_embed_field_id}/", json=EMBED_FIELD_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Should return 404 for invalid embed ID"

################################################################################
def test_patch_embed_field_invalid_field(client, new_embed_id, new_embed_field_id):
    """Test updating an embed field by ID with an invalid field ID."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/fields/{INVALID_ID}/", json=EMBED_FIELD_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Should return 404 for invalid field ID"

################################################################################
def test_patch_embed_field_invalid_payload(client, new_embed_id, new_embed_field_id):
    """Test updating an embed field by ID with an invalid payload."""

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/fields/{new_embed_field_id}/", json=INVALID_PAYLOAD)
    assert res.status_code == 422, "Should return 422 for invalid payload"

################################################################################
def test_patch_embed_exceeding_limits(client, new_embed_id, new_embed_field_id):
    """Test updating an embed with fields exceeding limits."""

    long_title = "A" * (limits.EMBED_TITLE_MAX + 1)
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}", json={"title": long_title})
    assert res.status_code == 422, "Should return 422 for title exceeding length limit"

    long_description = "B" * (limits.EMBED_BODY_MAX + 1)
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}", json={"description": long_description})
    assert res.status_code == 422, "Should return 422 for description exceeding length limit"

    long_field_name = "C" * (limits.EMBED_FIELD_NAME_MAX + 1)
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/fields/{new_embed_field_id}", json={"name": long_field_name})
    assert res.status_code == 422, "Should return 413 for field name exceeding length limit"

    long_field_value = "D" * (limits.EMBED_FIELD_VALUE_MAX + 1)
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/embeds/{new_embed_id}/fields/{new_embed_field_id}", json={"value": long_field_value})
    assert res.status_code == 422, "Should return 422 for field value exceeding length limit"

################################################################################
