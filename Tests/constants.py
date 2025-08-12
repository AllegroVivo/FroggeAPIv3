from datetime import datetime, timedelta
################################################################################
FROGGE_SECRET = "QljG4ZZXLVlJhuNfyqarQzar9W6jgyA4"
TEST_CLIENT_USER_ID = 334530475479531520
TEST_GUILD_ID = 1273061765831458866
TEST_GUILD_ID2 = 303742308874977280
INVALID_GUILD_ID = 999999999999999999
TEST_USER_ID = 265695573527625731
TEST_USER_ID2 = 334530475479531520
TEST_CHANNEL_ID = 1273061766448021580
TEST_CHANNEL_ID2 = 1286774185854636166
TEST_ROLE_ID = 1273061765919408250
TEST_ROLE_ID2 = 981565682502221885
INVALID_ID = 99999
SUFFIX = f"?editor_id={TEST_USER_ID}"
TEST_DISCORD_POST_URL = "https://canary.discord.com/channels/1273061765831458866/1273061766448021580/1403546786097922132"
TEST_URL = "https://toxiccasino.carrd.co/"
TEST_IMAGE_URL_DISCORD = "https://cdn.discordapp.com/attachments/991902526188302427/1400254221634371635/Ying_Tang_dragon.png?ex=6891e69d&is=6890951d&hm=df04e53d8215e68a44666d7cc0cda9c9b04f551cfc4b4e081a0d5cb76cc3b5fb&"
TEST_IMAGE_URL_CLOUDINARY = "https://res.cloudinary.com/dvv1ve9gj/image/upload/v1752889792/SPOILER_2025-01-08_00-17-26-073_Neneko_Wedding_Veil.png"
TEST_TITLE = "Test Title"
TEST_DESCRIPTION = (  # (250 characters)
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras pulvinar convallis risus, quis aliquam nisi finibus quis. Duis "
    "feugiat magna eget augue consequat tristique. Mauris eu felis ex. Aliquam aliquam nec orci sed porta. Aliquam efficitur eros."
)
TEST_COLOR = int("0x4ABC23", 16)
TEST_EMOJI = "<:Allegro_love:897615543459266590>"
TEST_DT1 = datetime.now()
TEST_DT2 = (datetime.now() + timedelta(minutes=90))
TEST_TIMESTAMP = TEST_DT1.isoformat()
TEST_TIMESTAMP2 = TEST_DT2.isoformat()
TEST_TIME = TEST_DT1.time().isoformat()
TEST_TIME2 = TEST_DT2.time().isoformat()
TEST_STRING_LIST = ["Test String 1", "Test String 2", "Test String 3", "Test String 4"]
TEST_STRING_WITH_UNICODE = " Staff Party Bus  A platform for venues to post their staff needs and for staff to pick up jobs!  https://discord.gg/spbxiv "
################################################################################
# Default Module Values
DEFAULT_TIMEZONE = 7
DEFAULT_VIP_WARNING_THRESHOLD = 3
DEFAULT_EVENT_ELEMENT_TYPE = 0
DEFAULT_FORM_PROMPT_TYPE = 0
################################################################################
