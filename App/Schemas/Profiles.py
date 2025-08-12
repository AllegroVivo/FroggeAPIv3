from __future__ import annotations

from typing import Optional, Any, Dict, List
from pydantic import Field

from .Common import *
################################################################################

__all__ = (
    "DeepProfileManagerSchema",
    "ShallowProfileSchema",
    "DeepProfileSchema",
    "ProfileDetailsSchema",
    "ProfileAtAGlanceSchema",
    "ProfilePersonalitySchema",
    "ProfileImagesSchema",
    "ProfileAdditionalImageSchema",
    "ProfileChannelGroupSchema",
    "ProfileRequirementsSchema",
    "ProfileCreateSchema",
    "ProfileAdditionalImageCreateSchema",
    "ProfileRequirementsUpdateSchema",
    "ProfileChannelGroupUpdateSchema",
    "ProfileUpdateSchema",
    "ProfileDetailsUpdateSchema",
    "ProfileAtAGlanceUpdateSchema",
    "ProfilePersonalityUpdateSchema",
    "ProfileImagesUpdateSchema",
    "ProfileAdditionalImageUpdateSchema",
)

################################################################################
class DeepProfileManagerSchema(BaseSchema):
    """
    Schema for a deep representation of a profile manager, including its fully hydrated profiles.
    """

    requirements: ProfileRequirementsSchema = Field(
        ...,
        description="The requirements for the profiles posted in the parent Guild."
    )
    profiles: List[DeepProfileSchema] = Field(
        ...,
        description="A list of profiles managed by this profile manager."
    )
    channel_groups: List[ProfileChannelGroupSchema] = Field(
        ...,
        description="A list of posting channel groups for this guild."
    )

################################################################################
class ProfileRequirementsSchema(BaseSchema):

    url: bool = Field(
        ...,
        description="Whether a URL is required to complete a profile."
    )
    color: bool = Field(
        ...,
        description="Whether an accent color is required to complete a profile."
    )
    jobs: bool = Field(
        ...,
        description="Whether RP jobs are required to complete a profile."
    )
    rates: bool = Field(
        ...,
        description="Whether the rates field is required to complete a profile."
    )
    gender: bool = Field(
        ...,
        description="Whether the gender field is required to complete a profile."
    )
    race: bool = Field(
        ...,
        description="Whether the race field is required to complete a profile."
    )
    orientation: bool = Field(
        ...,
        description="Whether the orientation field is required to complete a profile."
    )
    height: bool = Field(
        ...,
        description="Whether the height field is required to complete a profile."
    )
    age: bool = Field(
        ...,
        description="Whether the age field is required to complete a profile."
    )
    mare: bool = Field(
        ...,
        description="Whether the mare ID field is required to complete a profile."
    )
    world: bool = Field(
        ...,
        description="Whether setting the character's world field is required to complete a profile."
    )
    likes: bool = Field(
        ...,
        description="Whether the likes field is required to complete a profile."
    )
    dislikes: bool = Field(
        ...,
        description="Whether the dislikes field is required to complete a profile."
    )
    personality: bool = Field(
        ...,
        description="Whether the personality field is required to complete a profile."
    )
    aboutme: bool = Field(
        ...,
        description="Whether the about me section is required to complete a profile."
    )
    thumbnail: bool = Field(
        ...,
        description="Whether a thumbnail image is required to complete a profile."
    )
    main_image: bool = Field(
        ...,
        description="Whether a main image is required to complete a profile."
    )

################################################################################
class ShallowProfileSchema(IdentifiableSchema):
    """
    Schema for a shallow representation of a profile.
    """

    user_id: int = Field(
        ...,
        description="The user ID of the profile owner."
    )
    post_url: Optional[str] = Field(
        ...,
        description="The URL of the profile posting."
    )

################################################################################
class DeepProfileSchema(ShallowProfileSchema):
    """
    Schema for a deep representation of a profile, including its details.
    """

    details: ProfileDetailsSchema = Field(
        ...,
        description="The main details of the profile."
    )
    ataglance: ProfileAtAGlanceSchema = Field(
        ...,
        description="A quick overview of the parent character."
    )
    personality: ProfilePersonalitySchema = Field(
        ...,
        description="The personality traits of the character."
    )
    images: ProfileImagesSchema = Field(
        ...,
        description="The images associated with the profile."
    )

################################################################################
class ProfileDetailsSchema(BaseSchema):
    """
    Schema for the main details of a profile.
    """

    name: Optional[str] = Field(
        ...,
        description="The name of the character."
    )
    custom_url: Optional[str] = Field(
        ...,
        description="The custom title URL of the character's profile."
    )
    color: Optional[int] = Field(
        ...,
        description="The desired accent color associated with the profile."
    )
    jobs: List[str] = Field(
        ...,
        description="A list of RP jobs associated with the character."
    )
    rates: Optional[str] = Field(
        ...,
        description="The rates field for the character."
    )

################################################################################
class ProfileAtAGlanceSchema(BaseSchema):
    """
    Schema for a quick overview of the parent character.
    """

    world: Optional[int] = Field(
        ...,
        description="The FFXIV world the character belongs to."
    )
    gender_enum: Optional[int] = Field(
        ...,
        description="The character's chosen gender."
    )
    pronouns: List[int] = Field(
        ...,
        description="A list of pronouns associated with the character."
    )
    race_enum: Optional[int] = Field(
        ...,
        description="The character's chosen FFXIV race."
    )
    clan_enum: Optional[int] = Field(
        ...,
        description="The character's chosen FFXIV clan."
    )
    orientation_enum: Optional[int] = Field(
        ...,
        description="The character's chosen orientation."
    )
    race_custom: Optional[str] = Field(
        ...,
        description="The character's custom race value, if applicable."
    )
    clan_custom: Optional[str] = Field(
        ...,
        description="The character's custom clan value, if applicable."
    )
    orientation_custom: Optional[str] = Field(
        ...,
        description="The character's custom orientation value, if applicable."
    )
    height: Optional[int] = Field(
        ...,
        description="The character's height - in centimeters."
    )
    age: Optional[str] = Field(
        ...,
        description="The character's age."
    )
    mare: Optional[str] = Field(
        ...,
        description="The character's mare ID, if applicable."
    )

################################################################################
class ProfilePersonalitySchema(BaseSchema):
    """
    Schema for the personality traits of the character.
    """

    likes: List[str] = Field(
        ...,
        description="The character's likes."
    )
    dislikes: List[str] = Field(
        ...,
        description="The character's dislikes."
    )
    personality: Optional[str] = Field(
        ...,
        description="The character's personality blurb."
    )
    aboutme: Optional[str] = Field(
        ...,
        description="The 'about me' section of the profile."
    )

################################################################################
class ProfileImagesSchema(BaseSchema):
    """
    Schema for the images associated with the profile.
    """

    thumbnail_url: Optional[str] = Field(
        ...,
        description="The URL of the profile's thumbnail image."
    )
    main_image_url: Optional[str] = Field(
        ...,
        description="The URL of the profile's main image."
    )
    addl_images: List[ProfileAdditionalImageSchema] = Field(
        ...,
        description="A list of additional images in the profile gallery."
    )

################################################################################
class ProfileAdditionalImageSchema(IdentifiableSchema):
    """
    Schema for an additional image in the profile gallery.
    """

    url: str = Field(
        ...,
        description="The URL of the additional image."
    )
    caption: Optional[str] = Field(
        ...,
        description="An optional caption for the additional image."
    )

################################################################################
class ProfileChannelGroupSchema(IdentifiableSchema):
    """
    Schema for a channel group used for posting profiles in a guild.
    """

    channel_ids: List[int] = Field(
        ...,
        description="A list of channel IDs where profiles can be posted."
    )
    role_ids: List[int] = Field(
        ...,
        description="A list of role IDs that can post profiles in the channels."
    )

################################################################################
class ProfileCreateSchema(BaseSchema):
    """
    Schema for creating a new profile.
    """

    user_id: int = Field(
        ...,
        description="The user ID of the profile owner."
    )

################################################################################
class ProfileAdditionalImageCreateSchema(BaseSchema):
    """
    Schema for creating an additional image in the profile gallery.
    """

    url: str = Field(
        ...,
        description="The URL of the additional image."
    )

################################################################################
class ProfileRequirementsUpdateSchema(BaseSchema):
    """
    Schema for updating the requirements for profiles in a guild.
    """

    url: bool = Field(
        None,
        description="Whether a URL is required to complete a profile."
    )
    color: bool = Field(
        None,
        description="Whether an accent color is required to complete a profile."
    )
    jobs: bool = Field(
        None,
        description="Whether RP jobs are required to complete a profile."
    )
    rates: bool = Field(
        None,
        description="Whether the rates field is required to complete a profile."
    )
    gender: bool = Field(
        None,
        description="Whether the gender field is required to complete a profile."
    )
    race: bool = Field(
        None,
        description="Whether the race field is required to complete a profile."
    )
    orientation: bool = Field(
        None,
        description="Whether the orientation field is required to complete a profile."
    )
    height: bool = Field(
        None,
        description="Whether the height field is required to complete a profile."
    )
    age: bool = Field(
        None,
        description="Whether the age field is required to complete a profile."
    )
    mare: bool = Field(
        None,
        description="Whether the mare ID field is required to complete a profile."
    )
    world: bool = Field(
        None,
        description="Whether setting the character's world field is required to complete a profile."
    )
    likes: bool = Field(
        None,
        description="Whether the likes field is required to complete a profile."
    )
    dislikes: bool = Field(
        None,
        description="Whether the dislikes field is required to complete a profile."
    )
    personality: bool = Field(
        None,
        description="Whether the personality field is required to complete a profile."
    )
    aboutme: bool = Field(
        None,
        description="Whether the about me section is required to complete a profile."
    )
    thumbnail: bool = Field(
        None,
        description="Whether a thumbnail image is required to complete a profile."
    )
    main_image: bool = Field(
        None,
        description="Whether a main image is required to complete a profile."
    )

################################################################################
class ProfileChannelGroupUpdateSchema(BaseSchema):
    """
    Schema for updating a channel group used for posting profiles in a guild.
    """

    channel_ids: Optional[List[int]] = Field(
        None,
        description="A list of channel IDs where profiles can be posted."
    )
    role_ids: Optional[List[int]] = Field(
        None,
        description="A list of role IDs that can post profiles in the channels."
    )

################################################################################
class ProfileUpdateSchema(BaseSchema):
    """
    Schema for updating a profile.
    """

    post_url: Optional[str] = Field(
        None,
        description="The URL of the profile posting."
    )

################################################################################
class ProfileDetailsUpdateSchema(BaseSchema):
    """
    Schema for updating the main details of a profile.
    """

    name: Optional[str] = Field(
        None,
        description="The name of the character."
    )
    custom_url: Optional[str] = Field(
        None,
        description="The custom title URL of the character's profile."
    )
    color: Optional[int] = Field(
        None,
        description="The desired accent color associated with the profile."
    )
    jobs: Optional[List[str]] = Field(
        None,
        description="A list of RP jobs associated with the character."
    )
    rates: Optional[str] = Field(
        None,
        description="The rates field for the character."
    )

################################################################################
class ProfileAtAGlanceUpdateSchema(BaseSchema):
    """
    Schema for updating a quick overview of the parent character.
    """

    world: Optional[int] = Field(
        None,
        description="The FFXIV world the character belongs to."
    )
    gender_enum: Optional[int] = Field(
        None,
        description="The character's chosen gender."
    )
    pronouns: List[int] = Field(
        None,
        description="A list of pronouns associated with the character."
    )
    race_enum: Optional[int] = Field(
        None,
        description="The character's chosen FFXIV race."
    )
    clan_enum: Optional[int] = Field(
        None,
        description="The character's chosen FFXIV clan."
    )
    orientation_enum: Optional[int] = Field(
        None,
        description="The character's chosen orientation."
    )
    race_custom: Optional[str] = Field(
        None,
        description="The character's custom race value, if applicable."
    )
    clan_custom: Optional[str] = Field(
        None,
        description="The character's custom clan value, if applicable."
    )
    orientation_custom: Optional[str] = Field(
        None,
        description="The character's custom orientation value, if applicable."
    )
    height: Optional[int] = Field(
        None,
        description="The character's height - in centimeters."
    )
    age: Optional[str] = Field(
        None,
        description="The character's age."
    )
    mare: Optional[str] = Field(
        None,
        description="The character's mare ID, if applicable."
    )

################################################################################
class ProfilePersonalityUpdateSchema(BaseSchema):
    """
    Schema for updating the personality traits of the character.
    """

    likes: Optional[List[str]] = Field(
        None,
        description="The character's likes."
    )
    dislikes: Optional[List[str]] = Field(
        None,
        description="The character's dislikes."
    )
    personality: Optional[str] = Field(
        None,
        description="The character's personality blurb."
    )
    aboutme: Optional[str] = Field(
        None,
        description="The 'about me' section of the profile."
    )

################################################################################
class ProfileImagesUpdateSchema(BaseSchema):
    """
    Schema for updating the images associated with the profile.
    """

    thumbnail_url: Optional[str] = Field(
        None,
        description="The URL of the profile's thumbnail image."
    )
    main_image_url: Optional[str] = Field(
        None,
        description="The URL of the profile's main image."
    )

################################################################################
class ProfileAdditionalImageUpdateSchema(BaseSchema):
    """
    Schema for updating an additional image in the profile gallery.
    """

    caption: Optional[str] = Field(
        None,
        description="An optional caption for the additional image."
    )

################################################################################
