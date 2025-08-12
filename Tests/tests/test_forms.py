import pytest

from ..payloads import *

from App import limits, Models
################################################################################
### Fixtures ###
################################################################################
@pytest.fixture(scope="function")
def new_form_id(client):

    res = client.post(f"/guilds/{TEST_GUILD_ID}/forms/")
    assert res.status_code == 201, "Should create a new form successfully"
    form = res.json()
    assert_form_default_data(form)
    yield form["id"]

################################################################################
@pytest.fixture(scope="function")
def new_form_question_id(client, new_form_id):

    res = client.post(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions")
    assert res.status_code == 201, "Should create a new form question successfully"
    question = res.json()
    assert_form_question_default_data(question)
    yield question["id"]

################################################################################
@pytest.fixture(scope="function")
def new_form_question_option_id(client, new_form_id, new_form_question_id):

    res = client.post(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/options/")
    assert res.status_code == 201, "Should create a new form question option successfully"
    option = res.json()
    assert_form_question_option_default_data(option)
    yield option["id"]

################################################################################
@pytest.fixture(scope="function")
def new_form_question_response_id(client, new_form_id, new_form_question_id):

    res = client.post(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/responses/",
        json=FORM_QUESTION_RESPONSE_CREATE_PAYLOAD
    )
    assert res.status_code == 201, "Should create a new form question response successfully"
    response = res.json()
    assert response is not None, "Response should not be None"
    assert "id" in response, "Response should have an ID"
    assert isinstance(response["id"], int), "Response ID should be an integer"
    yield response["id"]

################################################################################
### Default Data Assertions ###
################################################################################
def assert_form_default_data(f):

    assert f is not None, "Form should not be None"
    assert "id" in f, "Form should have an ID"
    assert isinstance(f["id"], int), "Form ID should be an integer"
    assert f["id"] >= 0, "Form ID should be >= 0"
    assert "name" in f, "Form should have a name"
    assert f["name"] is None, "Form name should be None by default"
    assert "create_channel" in f, "Form should have create_channel field"
    assert isinstance(f["create_channel"], bool), "Form create_channel should be an boolean"
    assert f["create_channel"] is False, "Form create_channel should be False by default"
    assert "channel_roles" in f, "Form should have channel_roles field"
    assert isinstance(f["channel_roles"], list), "Form channel_roles should be a list"
    assert f["channel_roles"] == [], "Form channel_roles should be an empty list by default"
    assert "creation_category" in f, "Form should have creation_category field"
    assert f["creation_category"] is None, "Form creation_category should be None by default"
    assert "post_url" in f, "Form should have post_url field"
    assert f["post_url"] is None, "Form post_url should be None by default"
    assert "notify_roles" in f, "Form should have notify_roles field"
    assert isinstance(f["notify_roles"], list), "Form notify_roles should be a list"
    assert f["notify_roles"] == [], "Form notify_roles should be an empty list by default"
    assert "notify_users" in f, "Form should have notify_users field"
    assert isinstance(f["notify_users"], list), "Form notify_users should be a list"
    assert f["notify_users"] == [], "Form notify_users should be an empty list by default"
    assert "response_collections" in f, "Form should have response_collections field"
    assert isinstance(f["response_collections"], list), "Form response_collections should be a list"
    assert f["response_collections"] == [], "Form response_collections should be an empty list by default"
    assert "questions" in f, "Form should have questions field"
    assert isinstance(f["questions"], list), "Form questions should be a list"
    for question in f["questions"]:
        assert_form_question_default_data(question)
    assert "post_options" in f, "Form should have post_options field"
    assert_form_post_options_default_data(f["post_options"])
    assert "pre_prompt" in f, "Form should have pre_prompt field"
    assert_form_prompt_default_data(f["pre_prompt"])
    assert "post_prompt" in f, "Form should have post_prompt field"
    assert_form_prompt_default_data(f["post_prompt"])

################################################################################
def assert_form_post_options_default_data(po):

    assert po is not None, "Post options should not be None"
    assert isinstance(po, dict), "Post options should be a dictionary"
    assert "description" in po, "Post options should have a description"
    assert po["description"] is None, "Post options description should be None by default"
    assert "thumbnail_url" in po, "Post options should have a thumbnail_url"
    assert po["thumbnail_url"] is None, "Post options thumbnail_url should be None by default"
    assert "color" in po, "Post options should have a color"
    assert po["color"] is None, "Post options color should be None by default"
    assert "button_label" in po, "Post options should have a button_label"
    assert po["button_label"] is None, "Post options button_label should be None by default"
    assert "button_emoji" in po, "Post options should have a button_emoji"
    assert po["button_emoji"] is None, "Post options button_emoji should be None by default"
    assert "channel_id" in po, "Post options should have a channel_id"
    assert po["channel_id"] is None, "Post options channel_id should be None by default"

################################################################################
def assert_form_prompt_default_data(p):

    assert p is not None, "Prompt should not be None"
    assert isinstance(p, dict), "Prompt should be a dictionary"
    assert "id" in p, "Prompt should have an ID"
    assert isinstance(p["id"], int), "Prompt ID should be an integer"
    assert p["id"] >= 0, "Prompt ID should be >= 0"
    assert "title" in p, "Prompt should have a title"
    assert p["title"] is None, "Prompt title should be None by default"
    assert "description" in p, "Prompt should have a description"
    assert p["description"] is None, "Prompt description should be None by default"
    assert "thumbnail_url" in p, "Prompt should have a thumbnail_url"
    assert p["thumbnail_url"] is None, "Prompt thumbnail_url should be None by default"
    assert "show_cancel" in p, "Prompt should have a show_cancel field"
    assert isinstance(p["show_cancel"], bool), "Prompt show_cancel should be a boolean"
    assert p["show_cancel"] is False, "Prompt show_cancel should be False by default"
    assert "is_active" in p, "Prompt should have an is_active field"
    assert isinstance(p["is_active"], bool), "Prompt is_active should be a boolean"
    assert p["is_active"] is False, "Prompt is_active should be True by default"

################################################################################
def assert_form_question_default_data(q):

    assert q is not None, "Question should not be None"
    assert "id" in q, "Question should have an ID"
    assert isinstance(q["id"], int), "Question ID should be an integer"
    assert q["id"] >= 0, "Question ID should be >= 0"
    assert "sort_order" in q, "Question should have a sort_order"
    assert isinstance(q["sort_order"], int), "Question sort_order should be an integer"
    assert q["sort_order"] >= 0, "Question sort_order should be >= 0"
    assert "primary_text" in q, "Question should have a primary_text"
    assert q["primary_text"] is None, "Question primary_text should be None by default"
    assert "secondary_text" in q, "Question should have a secondary_text"
    assert q["secondary_text"] is None, "Question secondary_text should be None by default"
    assert "ui_type" in q, "Question should have a ui_type"
    assert isinstance(q["ui_type"], int), "Question ui_type should be an integer"
    assert q["ui_type"] == 0, "Question ui_type should be 0 by default"
    assert "required" in q, "Question should have a required field"
    assert isinstance(q["required"], bool), "Question required should be a boolean"
    assert q["required"] is False, "Question required should be False by default"
    assert "options" in q, "Question should have options field"
    assert isinstance(q["options"], list), "Question options should be a list"
    for option in q["options"]:
        assert_form_question_option_default_data(option)
    assert "responses" in q, "Question should have responses field"
    assert isinstance(q["responses"], list), "Question responses should be a list"
    for response in q["responses"]:
        assert_form_question_response_default_data(response)
    assert "pre_prompt" in q, "Question should have a pre_prompt field"
    assert_form_prompt_default_data(q["pre_prompt"])
    assert "post_prompt" in q, "Question should have a post_prompt field"
    assert_form_prompt_default_data(q["post_prompt"])

################################################################################
def assert_form_question_option_default_data(o):

    assert o is not None, "Option should not be None"
    assert "id" in o, "Option should have an ID"
    assert isinstance(o["id"], int), "Option ID should be an integer"
    assert o["id"] >= 0, "Option ID should be >= 0"
    assert "label" in o, "Option should have a label"
    assert o["label"] is None, "Option label should be None by default"
    assert "sort_order" in o, "Option should have a sort_order"
    assert isinstance(o["sort_order"], int), "Option sort_order should be an integer"
    assert o["sort_order"] >= 0, "Option sort_order should be >= 0"
    assert "description" in o, "Option should have a description"
    assert o["description"] is None, "Option description should be None by default"
    assert "value" in o, "Option should have a value"
    assert o["value"] is None, "Option value should be None by default"
    assert "emoji" in o, "Option should have an emoji"
    assert o["emoji"] is None, "Option emoji should be None by default"

################################################################################
def assert_form_question_response_default_data(r):

    assert r is not None, "Response should not be None"
    assert "id" in r, "Response should have an ID"
    assert isinstance(r["id"], int), "Response ID should be an integer"
    assert r["id"] >= 0, "Response ID should be >= 0"
    assert "user_id" in r, "Response should have a user_id"
    assert isinstance(r["user_id"], int), "Response user_id should be an integer"
    assert r["user_id"] >= 0, "Response user_id should be >= 0"
    assert "values" in r, "Response should have values field"
    assert isinstance(r["values"], list), "Response values should be a list"
    assert r["values"] == TEST_STRING_LIST, "Response values should be an empty list by default"

################################################################################
### GET Tests ###
################################################################################
def test_get_all_forms(client, new_form_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/")
    assert res.status_code == 200, "Should return all forms successfully"
    forms = res.json()
    assert isinstance(forms, list), "Response should be a list of forms"
    assert len(forms) > 0, "Should return at least one form"
    assert any(form["id"] == new_form_id for form in forms), "Should include the newly created form in the list"
    for form in forms:
        assert_form_default_data(form)

################################################################################
def test_get_form_by_id(client, new_form_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 200, "Should return the form successfully"
    form = res.json()
    assert_form_default_data(form)
    assert form["id"] == new_form_id, "Returned form should match the requested form ID"

################################################################################
def test_get_form_invalid_guild(client, new_form_id):

    res = client.get(f"/guilds/{INVALID_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 404, "Should return 404 for form in a different guild"

################################################################################
def test_get_form_invalid_id(client, new_form_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/{INVALID_ID}")
    assert res.status_code == 404, "Should return 404 for non-existent form ID"

################################################################################
### POST Tests ###
################################################################################
def test_post_form_question_response(client, new_form_id, new_form_question_id):

    res = client.post(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/responses/",
        json=FORM_QUESTION_RESPONSE_CREATE_PAYLOAD
    )
    assert res.status_code == 201, "Should return the form question successfully"
    response = res.json()
    assert response is not None, "Response should not be None"
    assert "id" in response, "Response should have an ID"
    assert isinstance(response["id"], int), "Response ID should be an integer"
    assert response["id"] >= 0, "Response ID should be >= 0"
    assert "user_id" in response, "Response should have a user_id"
    assert isinstance(response["user_id"], int), "Response user_id should be an integer"
    assert response["user_id"] == FORM_QUESTION_RESPONSE_CREATE_PAYLOAD["user_id"], "Response user_id should be >= 0"
    assert "values" in response, "Response should have values field"
    assert isinstance(response["values"], list), "Response values should be a list"
    assert response["values"] == FORM_QUESTION_RESPONSE_CREATE_PAYLOAD["values"], "Response values should be an empty list by default"

################################################################################
def test_post_form_question_response_invalid_guild(client, new_form_id, new_form_question_id):

    res = client.post(
        f"/guilds/{INVALID_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/responses/",
        json=FORM_QUESTION_RESPONSE_CREATE_PAYLOAD
    )
    assert res.status_code == 404, "Should return 404 for form question response in a different guild"

################################################################################
def test_post_form_question_response_invalid_form(client, new_form_id, new_form_question_id):

    res = client.post(
        f"/guilds/{TEST_GUILD_ID}/forms/{INVALID_ID}/questions/{new_form_question_id}/responses/",
        json=FORM_QUESTION_RESPONSE_CREATE_PAYLOAD
    )
    assert res.status_code == 404, "Should return 404 for form question response in a non-existent form"

################################################################################
def test_post_form_question_response_invalid_question(client, new_form_id, new_form_question_id):

    res = client.post(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{INVALID_ID}/responses/",
        json=FORM_QUESTION_RESPONSE_CREATE_PAYLOAD
    )
    assert res.status_code == 404, "Should return 404 for form question response in a non-existent question"

################################################################################
def test_post_form_question_response_invalid_payload(client, new_form_id, new_form_question_id):

    res = client.post(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/responses/",
        json=INVALID_PAYLOAD
    )
    assert res.status_code == 422, "Should return 422 for invalid payload in form question response"

################################################################################
def test_post_form_response_collection(client, new_form_id):

    res = client.post(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/response-collections/",
        json=FORM_RESPONSE_COLLECTION_CREATE_PAYLOAD
    )
    assert res.status_code == 201, "Should create a new form response collection successfully"
    collection = res.json()
    assert collection is not None, "Response collection should not be None"
    assert "id" in collection, "Response collection should have an ID"
    assert isinstance(collection["id"], int), "Response collection ID should be an integer"
    assert collection["id"] >= 0, "Response collection ID should be >= 0"
    assert "user_id" in collection, "Response collection should have a user_id"
    assert collection["user_id"] == FORM_RESPONSE_COLLECTION_CREATE_PAYLOAD["user_id"], "Response collection user_id should match the payload user ID"

################################################################################
def test_post_form_response_collection_invalid_guild(client, new_form_id):

    res = client.post(
        f"/guilds/{INVALID_GUILD_ID}/forms/{new_form_id}/response-collections/",
        json=FORM_RESPONSE_COLLECTION_CREATE_PAYLOAD
    )
    assert res.status_code == 404, "Should return 404 for form response collection in a different guild"

################################################################################
def test_post_form_response_collection_invalid_form(client, new_form_id):

    res = client.post(
        f"/guilds/{TEST_GUILD_ID}/forms/{INVALID_ID}/response-collections/",
        json=FORM_RESPONSE_COLLECTION_CREATE_PAYLOAD
    )
    assert res.status_code == 404, "Should return 404 for form response collection in a non-existent form"

################################################################################
def test_post_form_response_collection_invalid_payload(client, new_form_id):

    res = client.post(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/response-collections/",
        json=INVALID_PAYLOAD
    )
    assert res.status_code == 422, "Should return 422 for invalid payload in form response collection"

################################################################################
def test_post_form_question_option_invalid_guild(client, new_form_id, new_form_question_id):

    res = client.post(f"/guilds/{INVALID_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/options/")
    assert res.status_code == 404, "Should return 404 for form question option in a different guild"

################################################################################
def test_post_form_question_option_invalid_form(client, new_form_id, new_form_question_id):

    res = client.post(f"/guilds/{TEST_GUILD_ID}/forms/{INVALID_ID}/questions/{new_form_question_id}/options/")
    assert res.status_code == 404, "Should return 404 for form question option in a non-existent form"

################################################################################
def test_post_form_question_option_invalid_question(client, new_form_id, new_form_question_id):

    res = client.post(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{INVALID_ID}/options/")
    assert res.status_code == 404, "Should return 404 for form question option in a non-existent question"

################################################################################
# DELETE Tests
################################################################################
def test_delete_form(client, db_session, new_form_id):

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 204, "Should delete the form successfully"

    # Verify deletion
    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 404, "Should return 404 for deleted form"

    # Verify that subtables are also deleted
    po = db_session.query(Models.FormPostOptionsModel).filter_by(form_id=new_form_id).first()
    assert po is None, "Post options should be deleted when the form is deleted"
    prompts = db_session.query(Models.FormPromptModel).filter_by(form_id=new_form_id).all()
    assert len(prompts) == 0, "Prompts should be deleted when the form is deleted"

################################################################################
def test_delete_form_invalid_guild(client, new_form_id):

    res = client.delete(f"/guilds/{INVALID_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 404, "Should return 404 for form deletion in a different guild"

################################################################################
def test_delete_form_invalid_id(client, new_form_id):

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/forms/{INVALID_ID}")
    assert res.status_code == 404, "Should return 404 for non-existent form deletion"

################################################################################
def test_delete_form_question(client, db_session, new_form_id, new_form_question_id):

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}")
    assert res.status_code == 204, "Should delete the form question successfully"

    # Verify deletion
    q = db_session.query(Models.FormQuestionModel).filter_by(form_id=new_form_id).first()
    assert q is None, "Question should be deleted"

    # Verify that subtables are also deleted
    prompts = db_session.query(Models.FormPromptModel).filter_by(question_id=new_form_question_id).all()
    assert len(prompts) == 0, "Prompts should be deleted when the question is deleted"

################################################################################
def test_delete_form_question_invalid_guild(client, new_form_id, new_form_question_id):

    res = client.delete(f"/guilds/{INVALID_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}")
    assert res.status_code == 404, "Should return 404 for form question deletion in a different guild"

################################################################################
def test_delete_form_question_invalid_form(client, new_form_id, new_form_question_id):

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/forms/{INVALID_ID}/questions/{new_form_question_id}")
    assert res.status_code == 404, "Should return 404 for form question deletion in a non-existent form"

################################################################################
def test_delete_form_question_invalid_question(client, new_form_id, new_form_question_id):

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{INVALID_ID}")
    assert res.status_code == 404, "Should return 404 for form question deletion in a non-existent question"

################################################################################
def test_delete_form_question_option(client, db_session, new_form_id, new_form_question_id, new_form_question_option_id):

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/options/{new_form_question_option_id}")
    assert res.status_code == 204, "Should delete the form question option successfully"

    # Verify deletion
    option = db_session.query(Models.FormQuestionOptionModel).filter_by(id=new_form_question_option_id).first()
    assert option is None, "Question option should be deleted"

################################################################################
def test_delete_form_question_option_invalid_guild(client, new_form_id, new_form_question_id, new_form_question_option_id):

    res = client.delete(f"/guilds/{INVALID_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/options/{new_form_question_option_id}")
    assert res.status_code == 404, "Should return 404 for form question option deletion in a different guild"

################################################################################
def test_delete_form_question_option_invalid_form(client, new_form_id, new_form_question_id, new_form_question_option_id):

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/forms/{INVALID_ID}/questions/{new_form_question_id}/options/{new_form_question_option_id}")
    assert res.status_code == 404, "Should return 404 for form question option deletion in a non-existent form"

################################################################################
def test_delete_form_question_option_invalid_question(client, new_form_id, new_form_question_id, new_form_question_option_id):

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{INVALID_ID}/options/{new_form_question_option_id}")
    assert res.status_code == 404, "Should return 404 for form question option deletion in a non-existent question"

################################################################################
def test_delete_form_question_option_invalid_option(client, new_form_id, new_form_question_id):

    res = client.delete(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/options/{INVALID_ID}")
    assert res.status_code == 404, "Should return 404 for form question option deletion in a non-existent option"

################################################################################

FORM_PATCHABLE_FIELDS = {
    "name": TEST_TITLE,
    "create_channel": True,
    "channel_roles": [TEST_ROLE_ID],
    "creation_category": TEST_CHANNEL_ID,
    "post_url": TEST_DISCORD_POST_URL,
    "notify_roles": [TEST_ROLE_ID],
    "notify_users": [TEST_USER_ID]
}

################################################################################
def test_patch_form_full(client, new_form_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 200, "Should retrieve the form successfully"
    current = res.json()
    assert_form_default_data(current)

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}", json=FORM_PATCHABLE_FIELDS)
    assert res.status_code == 200, "Should update the form successfully"
    updated = res.json()

    for key, value in FORM_PATCHABLE_FIELDS.items():
        assert key in updated, f"Updated form should have {key}"
        assert updated[key] == value, f"Updated form {key} should match the payload"

################################################################################
@pytest.mark.parametrize("field", FORM_PATCHABLE_FIELDS.keys())
def test_patch_form_partial(client, new_form_id, field):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 200, "Should retrieve the form successfully"
    current = res.json()
    assert_form_default_data(current)

    payload = {field: FORM_PATCHABLE_FIELDS[field]}
    res = client.patch(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}", json=payload)
    assert res.status_code == 200, "Should update the form successfully"
    updated = res.json()

    for key, value in FORM_PATCHABLE_FIELDS.items():
        if key == field:
            assert key in updated, f"Updated form should have {key}"
            assert updated[key] == value, f"Updated form {key} should match the payload"
        else:
            assert key in current, f"Current form should have {key}"
            assert current[key] == updated[key], f"Unchanged field {key} should remain the same"

################################################################################
def test_patch_form_invalid_guild(client, new_form_id):

    res = client.patch(f"/guilds/{INVALID_GUILD_ID}/forms/{new_form_id}", json=FORM_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Should return 404 for form patch in a different guild"

################################################################################
def test_patch_form_invalid_id(client, new_form_id):

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/forms/{INVALID_ID}", json=FORM_PATCHABLE_FIELDS)
    assert res.status_code == 404, "Should return 404 for non-existent form patch"

################################################################################
def test_patch_form_invalid_payload(client, new_form_id):

    res = client.patch(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}", json=INVALID_PAYLOAD)
    assert res.status_code == 422, "Should return 422 for invalid payload in form patch"

################################################################################

FORM_PROMPT_PATCHABLE_FIELDS = {
    "title": TEST_TITLE,
    "description": TEST_DESCRIPTION,
    "thumbnail_url": TEST_IMAGE_URL_DISCORD,
    "show_cancel": True,
    "is_active": True
}

################################################################################
def test_patch_form_pre_prompt_full(client, new_form_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 200, "Should retrieve the form successfully"
    current = res.json()
    assert_form_default_data(current)

    pre_prompt_id = current["pre_prompt"]["id"]
    assert pre_prompt_id >= 0, "Pre-prompt ID should be >= 0"

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/prompts/{pre_prompt_id}",
        json=FORM_PROMPT_PATCHABLE_FIELDS
    )
    assert res.status_code == 200, "Should update the form pre-prompt successfully"
    updated = res.json()

    for key, value in FORM_PROMPT_PATCHABLE_FIELDS.items():
        assert key in updated, f"Updated form pre-prompt should have {key}"
        assert updated[key] == value, f"Updated form pre-prompt {key} should match the payload"

################################################################################
@pytest.mark.parametrize("field", FORM_PROMPT_PATCHABLE_FIELDS.keys())
def test_patch_form_pre_prompt_partial(client, new_form_id, field):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 200, "Should retrieve the form successfully"
    current = res.json()
    assert_form_default_data(current)

    pre_prompt_id = current["pre_prompt"]["id"]
    assert pre_prompt_id >= 0, "Pre-prompt ID should be >= 0"

    payload = {field: FORM_PROMPT_PATCHABLE_FIELDS[field]}
    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/prompts/{pre_prompt_id}",
        json=payload
    )
    assert res.status_code == 200, "Should update the form pre-prompt successfully"
    updated = res.json()

    for key, value in FORM_PROMPT_PATCHABLE_FIELDS.items():
        if key == field:
            assert key in updated, f"Updated form pre-prompt should have {key}"
            assert updated[key] == value, f"Updated form pre-prompt {key} should match the payload"
        else:
            assert key in current["pre_prompt"], f"Current form pre-prompt should have {key}"
            assert current["pre_prompt"][key] == updated[key], f"Unchanged field {key} should remain the same"

################################################################################
def test_patch_form_prompt_invalid_guild(client, new_form_id):

    res = client.patch(
        f"/guilds/{INVALID_GUILD_ID}/forms/{new_form_id}/prompts/1",
        json=FORM_PROMPT_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, "Should return 404 for form prompt patch in a different guild"

################################################################################
def test_patch_form_prompt_invalid_form(client, new_form_id):

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{INVALID_ID}/prompts/1",
        json=FORM_PROMPT_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, "Should return 404 for form prompt patch in a non-existent form"

################################################################################
def test_patch_form_prompt_invalid_prompt(client, new_form_id):

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/prompts/{INVALID_ID}",
        json=FORM_PROMPT_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, "Should return 404 for form prompt patch in a non-existent prompt"

################################################################################
def test_patch_form_prompt_invalid_payload(client, new_form_id):

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/prompts/1",
        json=INVALID_PAYLOAD
    )
    assert res.status_code == 422, "Should return 422 for invalid payload in form prompt patch"

################################################################################

FORM_POST_OPTIONS_PATCHABLE_FIELDS = {
    "description": TEST_DESCRIPTION,
    "thumbnail_url": TEST_IMAGE_URL_DISCORD,
    "color": TEST_COLOR,
    "button_label": TEST_TITLE,
    "button_emoji": TEST_EMOJI,
    "channel_id": TEST_CHANNEL_ID
}

################################################################################
def test_patch_form_post_options_full(client, new_form_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 200, "Should retrieve the form successfully"
    current = res.json()
    assert_form_default_data(current)

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/post-options",
        json=FORM_POST_OPTIONS_PATCHABLE_FIELDS
    )
    assert res.status_code == 200, "Should update the form post options successfully"
    updated = res.json()

    for key, value in FORM_POST_OPTIONS_PATCHABLE_FIELDS.items():
        assert key in updated, f"Updated form post options should have {key}"
        assert updated[key] == value, f"Updated form post options {key} should match the payload"

################################################################################
@pytest.mark.parametrize("field", FORM_POST_OPTIONS_PATCHABLE_FIELDS.keys())
def test_patch_form_post_options_partial(client, new_form_id, field):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 200, "Should retrieve the form successfully"
    current = res.json()
    assert_form_default_data(current)

    payload = {field: FORM_POST_OPTIONS_PATCHABLE_FIELDS[field]}
    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/post-options",
        json=payload
    )
    assert res.status_code == 200, "Should update the form post options successfully"
    updated = res.json()

    for key, value in FORM_POST_OPTIONS_PATCHABLE_FIELDS.items():
        if key == field:
            assert key in updated, f"Updated form post options should have {key}"
            assert updated[key] == value, f"Updated form post options {key} should match the payload"
        else:
            assert key in current["post_options"], f"Current form post options should have {key}"
            assert current["post_options"][key] == updated[key], f"Unchanged field {key} should remain the same"

################################################################################
def test_patch_form_post_options_invalid_guild(client, new_form_id):

    res = client.patch(
        f"/guilds/{INVALID_GUILD_ID}/forms/{new_form_id}/post-options",
        json=FORM_POST_OPTIONS_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, "Should return 404 for form post options patch in a different guild"

################################################################################
def test_patch_form_post_options_invalid_form(client, new_form_id):

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{INVALID_ID}/post-options",
        json=FORM_POST_OPTIONS_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, "Should return 404 for form post options patch in a non-existent form"

################################################################################
def test_patch_form_post_options_invalid_payload(client, new_form_id):

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/post-options",
        json=INVALID_PAYLOAD
    )
    assert res.status_code == 422, "Should return 422 for invalid payload in form post options patch"

################################################################################

FORM_QUESTION_PATCHABLE_FIELDS = {
    "sort_order": 1,
    "primary_text": TEST_TITLE,
    "secondary_text": TEST_DESCRIPTION,
    "ui_type": 1,
    "required": True
}

################################################################################
def test_patch_form_question_full(client, new_form_id, new_form_question_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 200, "Should retrieve the form successfully"
    current = res.json()
    assert_form_default_data(current)

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}",
        json=FORM_QUESTION_PATCHABLE_FIELDS
    )
    assert res.status_code == 200, "Should update the form question successfully"
    updated = res.json()

    for key, value in FORM_QUESTION_PATCHABLE_FIELDS.items():
        assert key in updated, f"Updated form question should have {key}"
        assert updated[key] == value, f"Updated form question {key} should match the payload"

################################################################################
@pytest.mark.parametrize("field", FORM_QUESTION_PATCHABLE_FIELDS.keys())
def test_patch_form_question_partial(client, new_form_id, new_form_question_id, field):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 200, "Should retrieve the form successfully"
    current = res.json()
    assert_form_default_data(current)

    payload = {field: FORM_QUESTION_PATCHABLE_FIELDS[field]}
    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}",
        json=payload
    )
    assert res.status_code == 200, "Should update the form question successfully"
    updated = res.json()

    for key, value in FORM_QUESTION_PATCHABLE_FIELDS.items():
        if key == field:
            assert key in updated, f"Updated form question should have {key}"
            assert updated[key] == value, f"Updated form question {key} should match the payload"
        else:
            assert key in current["questions"][0], f"Current form question should have {key}"
            assert current["questions"][0][key] == updated[key], f"Unchanged field {key} should remain the same"

################################################################################
def test_patch_form_question_invalid_guild(client, new_form_id, new_form_question_id):

    res = client.patch(
        f"/guilds/{INVALID_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}",
        json=FORM_QUESTION_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, "Should return 404 for form question patch in a different guild"

################################################################################
def test_patch_form_question_invalid_form(client, new_form_id, new_form_question_id):

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{INVALID_ID}/questions/{new_form_question_id}",
        json=FORM_QUESTION_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, "Should return 404 for form question patch in a non-existent form"

################################################################################
def test_patch_form_question_invalid_question(client, new_form_id, new_form_question_id):

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{INVALID_ID}",
        json=FORM_QUESTION_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, "Should return 404 for form question patch in a non-existent question"

################################################################################
def test_patch_form_question_invalid_payload(client, new_form_id, new_form_question_id):

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}",
        json=INVALID_PAYLOAD
    )
    assert res.status_code == 422, "Should return 422 for invalid payload in form question patch"

################################################################################
def test_patch_form_question_prompt_full(client, new_form_id, new_form_question_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 200, "Should retrieve the form successfully"
    current = res.json()
    assert_form_default_data(current)

    pre_prompt_id = current["questions"][0]["pre_prompt"]["id"]
    assert pre_prompt_id >= 0, "Pre-prompt ID should be >= 0"

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/prompts/{pre_prompt_id}",
        json=FORM_PROMPT_PATCHABLE_FIELDS
    )
    assert res.status_code == 200, "Should update the form question pre-prompt successfully"
    updated = res.json()

    for key, value in FORM_PROMPT_PATCHABLE_FIELDS.items():
        assert key in updated, f"Updated form question pre-prompt should have {key}"
        assert updated[key] == value, f"Updated form question pre-prompt {key} should match the payload"

################################################################################
@pytest.mark.parametrize("field", FORM_PROMPT_PATCHABLE_FIELDS.keys())
def test_patch_form_question_prompt_partial(client, new_form_id, new_form_question_id, field):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 200, "Should retrieve the form successfully"
    current = res.json()
    assert_form_default_data(current)

    pre_prompt_id = current["questions"][0]["pre_prompt"]["id"]
    assert pre_prompt_id >= 0, "Pre-prompt ID should be >= 0"

    payload = {field: FORM_PROMPT_PATCHABLE_FIELDS[field]}
    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/prompts/{pre_prompt_id}",
        json=payload
    )
    assert res.status_code == 200, "Should update the form question pre-prompt successfully"
    updated = res.json()

    for key, value in FORM_PROMPT_PATCHABLE_FIELDS.items():
        if key == field:
            assert key in updated, f"Updated form question pre-prompt should have {key}"
            assert updated[key] == value, f"Updated form question pre-prompt {key} should match the payload"
        else:
            assert key in current["questions"][0]["pre_prompt"], f"Current form question pre-prompt should have {key}"
            assert current["questions"][0]["pre_prompt"][key] == updated[key], f"Unchanged field {key} should remain the same"

################################################################################

FORM_QUESTION_RESPONSE_PATCHABLE_FIELDS = {
    "values": ["Test Response", "Another Response", "Yet Another Response"]
}

################################################################################
def test_patch_form_question_response_full(client, new_form_id, new_form_question_id, new_form_question_response_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 200, "Should retrieve the form successfully"
    current = res.json()
    assert_form_default_data(current)

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/responses/{new_form_question_response_id}",
        json=FORM_QUESTION_RESPONSE_PATCHABLE_FIELDS
    )
    assert res.status_code == 200, "Should update the form question response successfully"
    updated = res.json()

    for key, value in FORM_QUESTION_RESPONSE_PATCHABLE_FIELDS.items():
        assert key in updated, f"Updated form question response should have {key}"
        assert updated[key] == value, f"Updated form question response {key} should match the payload"

################################################################################
@pytest.mark.parametrize("field", FORM_QUESTION_RESPONSE_PATCHABLE_FIELDS.keys())
def test_patch_form_question_response_partial(client, new_form_id, new_form_question_id, new_form_question_response_id, field):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 200, "Should retrieve the form successfully"
    current = res.json()
    assert_form_default_data(current)

    payload = {field: FORM_QUESTION_RESPONSE_PATCHABLE_FIELDS[field]}
    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/responses/{new_form_question_response_id}",
        json=payload
    )
    assert res.status_code == 200, "Should update the form question response successfully"
    updated = res.json()

    for key, value in FORM_QUESTION_RESPONSE_PATCHABLE_FIELDS.items():
        if key == field:
            assert key in updated, f"Updated form question response should have {key}"
            assert updated[key] == value, f"Updated form question response {key} should match the payload"
        else:
            assert key in current["questions"][0]["responses"][0], f"Current form question response should have {key}"
            assert current["questions"][0]["responses"][0][key] == updated[key], f"Unchanged field {key} should remain the same"

################################################################################
def test_patch_form_question_response_invalid_guild(client, new_form_id, new_form_question_id, new_form_question_response_id):

    res = client.patch(
        f"/guilds/{INVALID_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/responses/{new_form_question_response_id}",
        json=FORM_QUESTION_RESPONSE_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, "Should return 404 for form question response patch in a different guild"

################################################################################
def test_patch_form_question_response_invalid_form(client, new_form_id, new_form_question_id, new_form_question_response_id):

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{INVALID_ID}/questions/{new_form_question_id}/responses/{new_form_question_response_id}",
        json=FORM_QUESTION_RESPONSE_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, "Should return 404 for form question response patch in a non-existent form"

################################################################################
def test_patch_form_question_response_invalid_question(client, new_form_id, new_form_question_id, new_form_question_response_id):

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{INVALID_ID}/responses/{new_form_question_response_id}",
        json=FORM_QUESTION_RESPONSE_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, "Should return 404 for form question response patch in a non-existent question"

################################################################################
def test_patch_form_question_response_invalid_response(client, new_form_id, new_form_question_id):

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/responses/{INVALID_ID}",
        json=FORM_QUESTION_RESPONSE_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, "Should return 404 for form question response patch in a non-existent response"

################################################################################
def test_patch_form_question_response_invalid_payload(client, new_form_id, new_form_question_id, new_form_question_response_id):

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/responses/{new_form_question_response_id}",
        json=INVALID_PAYLOAD
    )
    assert res.status_code == 422, "Should return 422 for invalid payload in form question response patch"

################################################################################

FORM_QUESTION_OPTION_PATCHABLE_FIELDS = {
    "sort_order": 1,
    "label": TEST_TITLE,
    "description": TEST_DESCRIPTION,
    "value": TEST_TITLE,
    "emoji": TEST_EMOJI
}

################################################################################
def test_patch_form_question_option_full(client, new_form_id, new_form_question_id, new_form_question_option_id):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 200, "Should retrieve the form successfully"
    current = res.json()
    assert_form_default_data(current)

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/options/{new_form_question_option_id}",
        json=FORM_QUESTION_OPTION_PATCHABLE_FIELDS
    )
    assert res.status_code == 200, "Should update the form question option successfully"
    updated = res.json()

    for key, value in FORM_QUESTION_OPTION_PATCHABLE_FIELDS.items():
        assert key in updated, f"Updated form question option should have {key}"
        assert updated[key] == value, f"Updated form question option {key} should match the payload"

################################################################################
@pytest.mark.parametrize("field", FORM_QUESTION_OPTION_PATCHABLE_FIELDS.keys())
def test_patch_form_question_option_partial(client, new_form_id, new_form_question_id, new_form_question_option_id, field):

    res = client.get(f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}")
    assert res.status_code == 200, "Should retrieve the form successfully"
    current = res.json()
    assert_form_default_data(current)

    payload = {field: FORM_QUESTION_OPTION_PATCHABLE_FIELDS[field]}
    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/options/{new_form_question_option_id}",
        json=payload
    )
    assert res.status_code == 200, "Should update the form question option successfully"
    updated = res.json()

    for key, value in FORM_QUESTION_OPTION_PATCHABLE_FIELDS.items():
        if key == field:
            assert key in updated, f"Updated form question option should have {key}"
            assert updated[key] == value, f"Updated form question option {key} should match the payload"
        else:
            assert key in current["questions"][0]["options"][0], f"Current form question option should have {key}"
            assert current["questions"][0]["options"][0][key] == updated[key], f"Unchanged field {key} should remain the same"

################################################################################
def test_patch_form_question_option_invalid_guild(client, new_form_id, new_form_question_id, new_form_question_option_id):

    res = client.patch(
        f"/guilds/{INVALID_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/options/{new_form_question_option_id}",
        json=FORM_QUESTION_OPTION_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, "Should return 404 for form question option patch in a different guild"

################################################################################
def test_patch_form_question_option_invalid_form(client, new_form_id, new_form_question_id, new_form_question_option_id):

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{INVALID_ID}/questions/{new_form_question_id}/options/{new_form_question_option_id}",
        json=FORM_QUESTION_OPTION_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, "Should return 404 for form question option patch in a non-existent form"

################################################################################
def test_patch_form_question_option_invalid_question(client, new_form_id, new_form_question_id, new_form_question_option_id):

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{INVALID_ID}/options/{new_form_question_option_id}",
        json=FORM_QUESTION_OPTION_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, "Should return 404 for form question option patch in a non-existent question"

################################################################################
def test_patch_form_question_option_invalid_option(client, new_form_id, new_form_question_id):

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/options/{INVALID_ID}",
        json=FORM_QUESTION_OPTION_PATCHABLE_FIELDS
    )
    assert res.status_code == 404, "Should return 404 for form question option patch in a non-existent option"

################################################################################
def test_patch_form_question_option_invalid_payload(client, new_form_id, new_form_question_id, new_form_question_option_id):

    res = client.patch(
        f"/guilds/{TEST_GUILD_ID}/forms/{new_form_id}/questions/{new_form_question_id}/options/{new_form_question_option_id}",
        json=INVALID_PAYLOAD
    )
    assert res.status_code == 422, "Should return 422 for invalid payload in form question option patch"

################################################################################
