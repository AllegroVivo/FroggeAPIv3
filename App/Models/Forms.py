from __future__ import annotations

from sqlalchemy import Column, Integer, BigInteger, ForeignKey, JSON, String, TIMESTAMP, func
from sqlalchemy.orm import relationship

from .Common import *
################################################################################

__all__ = (
    "FormModel",
    "FormPostOptionsModel",
    "FormQuestionModel",
    "FormQuestionResponseModel",
    "FormResponseCollectionModel",
    "FormPromptModel",
    "FormQuestionOptionModel",
)

################################################################################
class FormModel(BaseModel):

    __tablename__ = 'forms'

    id = Column(Integer, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey("guild_ids.guild_id", name="forms_guild_ids_fkey"), nullable=False)
    name = Column(String, nullable=True)
    create_channel = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    channel_roles = Column(ArrayOrJSON(BigInteger), nullable=False, default=[], server_default="[]")
    creation_category = Column(BigInteger, nullable=True)
    post_url = Column(String, nullable=True)
    notify_roles = Column(ArrayOrJSON(BigInteger), nullable=False, default=[], server_default="[]")
    notify_users = Column(ArrayOrJSON(BigInteger), nullable=False, default=[], server_default="[]")

    # Relationships
    guild = relationship("GuildIDModel", back_populates="forms")
    questions = relationship("FormQuestionModel", back_populates="form", cascade="all, delete-orphan")
    response_collections = relationship("FormResponseCollectionModel", back_populates="form", cascade="all, delete-orphan")
    prompts = relationship("FormPromptModel", back_populates="form", cascade="all, delete-orphan")
    post_options = relationship("FormPostOptionsModel", back_populates="form", uselist=False, cascade="all, delete-orphan")

################################################################################
class FormPostOptionsModel(BaseModel):

    __tablename__ = 'form_post_options'

    form_id = Column(Integer, ForeignKey("forms.id", name="form_post_options_forms_fkey", ondelete="CASCADE"), primary_key=True)
    description = Column(String, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    color = Column(Integer, nullable=True)
    button_label = Column(String, nullable=True)
    button_emoji = Column(String, nullable=True)
    channel_id = Column(BigInteger, nullable=True)

    # Relationships
    form = relationship("FormModel", back_populates="post_options")

################################################################################
class FormQuestionModel(BaseModel):

    __tablename__ = 'form_questions'

    id = Column(Integer, primary_key=True)
    form_id = Column(Integer, ForeignKey("forms.id", name="form_questions_forms_fkey", ondelete="CASCADE"), nullable=False)
    sort_order = Column(Integer, nullable=False)
    primary_text = Column(String, nullable=True)
    secondary_text = Column(String, nullable=True)
    ui_type = Column(Integer, nullable=False, default=0, server_default="0")
    required = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")

    # Relationships
    form = relationship("FormModel", back_populates="questions")
    responses = relationship("FormQuestionResponseModel", back_populates="question", cascade="all, delete-orphan")
    options = relationship("FormQuestionOptionModel", back_populates="question", cascade="all, delete-orphan")
    prompts = relationship("FormPromptModel", back_populates="question", cascade="all, delete-orphan")

################################################################################
class FormQuestionResponseModel(BaseModel):

    __tablename__ = 'form_question_responses'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("form_questions.id", name="form_question_responses_form_questions_fkey", ondelete="CASCADE"), nullable=False)
    user_id = Column(BigInteger, nullable=False)
    values = Column(ArrayOrJSON(String), nullable=False, default=[], server_default="[]")
    last_edited = Column(TIMESTAMP, nullable=False, server_default=func.now())

    # Relationships
    question = relationship("FormQuestionModel", back_populates="responses")

################################################################################
class FormResponseCollectionModel(BaseModel):

    __tablename__ = 'form_response_collections'

    id = Column(Integer, primary_key=True)
    form_id = Column(Integer, ForeignKey("forms.id", name="form_response_collections_forms_fkey", ondelete="CASCADE"), nullable=False)
    user_id = Column(BigInteger, nullable=False)
    data = Column(JSON, nullable=False)
    submitted_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    # Relationships
    form = relationship("FormModel", back_populates="response_collections")

################################################################################
class FormPromptModel(BaseModel):

    __tablename__ = 'form_prompts'

    id = Column(Integer, primary_key=True)
    form_id = Column(Integer, ForeignKey("forms.id", name="form_prompts_forms_fkey", ondelete="CASCADE"), nullable=True)
    question_id = Column(Integer, ForeignKey("form_questions.id", name="form_prompts_form_questions_fkey", ondelete="CASCADE"), nullable=True)
    prompt_type = Column(Integer, nullable=False)  # 0: form, 1: question
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    show_cancel = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    is_active = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")

    # Relationships
    form = relationship("FormModel", back_populates="prompts")
    question = relationship("FormQuestionModel", back_populates="prompts")

################################################################################
class FormQuestionOptionModel(BaseModel):

    __tablename__ = 'form_question_options'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("form_questions.id", name="form_options_form_questions_fkey", ondelete="CASCADE"), nullable=False)
    label = Column(String, nullable=True)
    description = Column(String, nullable=True)
    value = Column(String, nullable=True)
    emoji = Column(String, nullable=True)
    sort_order = Column(Integer, nullable=False)

    # Relationships
    question = relationship("FormQuestionModel", back_populates="options")

################################################################################
