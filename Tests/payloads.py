from .constants import *
################################################################################
REGISTER_CLIENT_PAYLOAD = {
    "user_id": TEST_CLIENT_USER_ID,
    "password": "password123",
    "frogge": FROGGE_SECRET,
}
LOGIN_FORM_DATA = {
    "username": str(TEST_CLIENT_USER_ID),
    "password": "password123",
}
INVALID_PAYLOAD = {
    "invalid_field": "This field should not be here"
}
BASE_CHANNEL_ID_PAYLOAD = {
    "channel_id": TEST_CHANNEL_ID,
}
BASE_USER_ID_PAYLOAD = {
    "user_id": TEST_USER_ID,
}
GUILD_ID_PAYLOAD = {
    "guild_id": TEST_GUILD_ID,
}
BASE_CREATE_ITEM_PAYLOAD = {
    "last_actor_id": TEST_USER_ID,
}
ALT_LAST_ACTOR_ID_PAYLOAD = {
    "last_actor_id": TEST_USER_ID2,
}
TEST_USER_CREATE_PAYLOAD = {
    "password": "password123",
    "frogge": FROGGE_SECRET,
    **BASE_USER_ID_PAYLOAD
}
FORM_QUESTION_RESPONSE_CREATE_PAYLOAD = {
    "values": TEST_STRING_LIST,
    **BASE_USER_ID_PAYLOAD
}
FORM_RESPONSE_COLLECTION_CREATE_PAYLOAD = {
    "data": {
        "questions": ["Test Question 1", "Test Question 2"],
        "responses": ["Test Response 1", "Test Response 2", "Test Response 3", "Test Response 4"]
    },
    **BASE_USER_ID_PAYLOAD
}
ADDITIONAL_IMAGE_CREATE_PAYLOAD = {
    "url": TEST_IMAGE_URL_CLOUDINARY,
}
CREATE_RAFFLE_ENTRY_PAYLOAD = {
    "quantity": 1,
    **BASE_USER_ID_PAYLOAD
}
################################################################################
