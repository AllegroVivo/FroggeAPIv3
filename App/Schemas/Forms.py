from __future__ import annotations
from typing import Optional, List, Any, Dict
from datetime import datetime
from pydantic import Field
from App import limits

from .Common import *
################################################################################

__all__ = (
    "BaseFormSchema",
    "DeepFormSchema",
    "FormPostOptionsSchema",
    "FormPromptSchema",
    "FormResponseCollectionSchema",
    "BaseFormQuestionSchema",
    "DeepFormQuestionSchema",
    "FormQuestionOptionSchema",
    "FormQuestionResponseSchema",
    "FormQuestionResponseCreateSchema",
    "FormResponseCollectionCreateSchema",
    "FormUpdateSchema",
    "FormPostOptionsUpdateSchema",
    "FormQuestionUpdateSchema",
    "FormQuestionOptionUpdateSchema",
    "FormPromptUpdateSchema",
    "FormQuestionResponseUpdateSchema",
)

################################################################################
class BaseFormSchema(IdentifiableSchema):

    name: Optional[str]
    create_channel: bool
    channel_roles: List[int]
    creation_category: Optional[int]
    post_url: Optional[str]
    notify_roles: List[int]
    notify_users: List[int]

################################################################################
class DeepFormSchema(BaseFormSchema):

    post_options: FormPostOptionsSchema
    response_collections: List[FormResponseCollectionSchema]
    questions: List[DeepFormQuestionSchema]
    pre_prompt: FormPromptSchema
    post_prompt: FormPromptSchema

################################################################################
class FormPostOptionsSchema(BaseSchema):

    description: Optional[str]
    thumbnail_url: Optional[str]
    color: Optional[int]
    button_label: Optional[str]
    button_emoji: Optional[str]
    channel_id: Optional[int]

################################################################################
class FormPromptSchema(IdentifiableSchema):

    title: Optional[str]
    description: Optional[str]
    thumbnail_url: Optional[str]
    show_cancel: bool
    is_active: bool

################################################################################
class FormResponseCollectionSchema(IdentifiableSchema):

    user_id: int
    data: Dict[str, Any]
    submitted_at: datetime

################################################################################
class BaseFormQuestionSchema(IdentifiableSchema):

    sort_order: int
    primary_text: Optional[str]
    secondary_text: Optional[str]
    ui_type: int
    required: bool

################################################################################
class DeepFormQuestionSchema(BaseFormQuestionSchema):

    options: List[FormQuestionOptionSchema]
    responses: List[FormQuestionResponseSchema]
    pre_prompt: FormPromptSchema
    post_prompt: FormPromptSchema

################################################################################
class FormQuestionOptionSchema(IdentifiableSchema):

    label: Optional[str]
    description: Optional[str]
    value: Optional[str]
    emoji: Optional[str]
    sort_order: int

################################################################################
class FormQuestionResponseSchema(IdentifiableSchema):

    user_id: int
    values: List[str]

################################################################################
class FormQuestionResponseCreateSchema(BaseSchema):

    user_id: int
    values: List[str]

################################################################################
class FormResponseCollectionCreateSchema(BaseSchema):

    user_id: int
    data: Dict[str, Any]

################################################################################
class FormUpdateSchema(BaseSchema):

    name: Optional[str] = None
    create_channel: Optional[bool] = None
    channel_roles: Optional[List[int]] = None
    creation_category: Optional[int] = None
    post_url: Optional[str] = None
    notify_roles: Optional[List[int]] = None
    notify_users: Optional[List[int]] = None

################################################################################
class FormPostOptionsUpdateSchema(BaseSchema):

    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    color: Optional[int] = None
    button_label: Optional[str] = None
    button_emoji: Optional[str] = None
    channel_id: Optional[int] = None

################################################################################
class FormQuestionUpdateSchema(BaseSchema):

    sort_order: Optional[int] = None
    primary_text: Optional[str] = None
    secondary_text: Optional[str] = None
    ui_type: Optional[int] = None
    required: Optional[bool] = None

################################################################################
class FormQuestionOptionUpdateSchema(BaseSchema):

    label: Optional[str] = None
    description: Optional[str] = None
    value: Optional[str] = None
    emoji: Optional[str] = None
    sort_order: Optional[int] = None

################################################################################
class FormPromptUpdateSchema(BaseSchema):

    title: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    show_cancel: Optional[bool] = None
    is_active: Optional[bool] = None

################################################################################
class FormQuestionResponseUpdateSchema(BaseSchema):

    values: List[str]

################################################################################
