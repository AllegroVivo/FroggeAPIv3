from __future__ import annotations

from datetime import datetime
from typing import List, Type, TypeVar, Any, Dict, Union, Literal, Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from App.dependencies import Dependencies
from .. import Models, Schemas
################################################################################

__all__ = (
    "map_embed",
    "map_form",
    "map_form_question",
    "get_shallow_or_404",
    "apply_updates",
    "next_sort_order",
    "build_audit_log_changes",
    "audit_log_create",
    "audit_log_update",
    "audit_log_delete",
    "match_or_403",
)

T = TypeVar("T")

################################################################################
def map_embed(embed: Union[Models.EmbedModel, Type[Models.EmbedModel]]) -> Schemas.DeepEmbedSchema:

    return Schemas.DeepEmbedSchema.model_validate(embed)

################################################################################
def map_form(form: Union[Models.FormModel, Type[Models.FormModel]]) -> Schemas.DeepFormSchema:

    # Prompts: 0 -> Pre, 1 -> Post
    pre_prompt = form.prompts[0] if form.prompts[0].prompt_type == 0 else form.prompts[1]
    post_prompt = form.prompts[1] if form.prompts[0].prompt_type == 0 else form.prompts[0]

    return Schemas.DeepFormSchema.model_validate({
        "id": form.id,
        "name": form.name,
        "create_channel": form.create_channel,
        "channel_roles": form.channel_roles,
        "creation_category": form.creation_category,
        "post_url": form.post_url,
        "notify_roles": form.notify_roles,
        "notify_users": form.notify_users,
        "post_options": Schemas.FormPostOptionsSchema.model_validate(form.post_options),
        "questions": [map_form_question(question) for question in form.questions],
        "response_collections": [Schemas.FormResponseCollectionSchema.model_validate(rc) for rc in form.response_collections],
        "pre_prompt": Schemas.FormPromptSchema.model_validate(pre_prompt),
        "post_prompt": Schemas.FormPromptSchema.model_validate(post_prompt),
    })

################################################################################
def map_form_question(q: Union[Models.FormQuestionModel, Type[Models.FormQuestionModel]]) -> Schemas.DeepFormQuestionSchema:

    # Prompts: 0 -> Pre, 1 -> Post
    pre_prompt = q.prompts[0] if q.prompts[0].prompt_type == 0 else q.prompts[1]
    post_prompt = q.prompts[1] if q.prompts[0].prompt_type == 0 else q.prompts[0]

    return Schemas.DeepFormQuestionSchema.model_validate({
        "id": q.id,
        "sort_order": q.sort_order,
        "primary_text": q.primary_text,
        "secondary_text": q.secondary_text,
        "ui_type": q.ui_type,
        "required": q.required,
        "responses": [Schemas.FormQuestionResponseSchema.model_validate(r) for r in q.responses],
        "options": [Schemas.FormQuestionOptionSchema.model_validate(o) for o in q.options],
        "pre_prompt": Schemas.FormPromptSchema.model_validate(pre_prompt),
        "post_prompt": Schemas.FormPromptSchema.model_validate(post_prompt),
    })

################################################################################
def get_shallow_or_404(db: Session, model: Type[T], **filters) -> T:

    item = db.query(model).filter_by(**filters).first()
    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"{model.__name__.rstrip('Model')} with with identifiers '{filters}' not found"
        )
    return item

################################################################################
def match_or_403(parent_id: int, reference_id: int) -> bool:
    """Checks if two models match and raises 403 if they do not."""

    if parent_id != reference_id:
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource.")
    return True

################################################################################
def apply_updates(target: Union[Models.BaseModel, Type[Models.BaseModel]], schema: Schemas.BaseSchema) -> None:

    data = schema.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(target, key, value)

################################################################################
def next_sort_order(opts: List[Union[Models.BaseModel, Type[Models.BaseModel]]]) -> int:

    return next((i for i, order in enumerate(range(len(opts))) if i != order), len(opts))

################################################################################
def build_audit_log_changes(obj: Any) -> Dict[str, Any]:

    changes = {}
    state = inspect(obj)

    for attr in state.attrs:
        if not attr.history.has_changes():
            continue
        old, new = None, None
        # history.deleted/new hold previous/current values in lists
        if attr.history.deleted:
            old = attr.history.deleted[0]
        if attr.history.added:
            new = attr.history.added[0]
        if old != new:
            changes[attr.key] = {"old": old, "new": new}

    return changes

################################################################################
def _record_audit_log_item(
    guild_id: int,
    db: Session,
    obj: Any,
    target_id: int,
    op: Literal["Create", "Update", "Delete"],
    actor_id: int,
) -> None:

    action = Models.AuditLogModel(
        guild_id=guild_id,
        target=obj.__class__.__name__.removesuffix("Model"),
        target_id=target_id,
        action=op,
        user_id=actor_id,
        changes=jsonable_encoder(build_audit_log_changes(obj)),
        request_id=None
    )
    db.add(action)

################################################################################
def audit_log_create(deps: Dependencies, obj: Any, target_id: int) -> None:
    """Records a create operation in the audit log."""

    _record_audit_log_item(deps.guild_id, deps.db, obj, target_id, "Create", deps.actor_id)

################################################################################
def audit_log_update(deps: Dependencies, obj: Any, target_id: int) -> None:
    """Records an update operation in the audit log."""

    _record_audit_log_item(deps.guild_id, deps.db, obj, target_id, "Update", deps.actor_id)

################################################################################
def audit_log_delete(deps: Dependencies, obj: Any, target_id: int) -> None:
    """Records a delete operation in the audit log."""

    _record_audit_log_item(deps.guild_id, deps.db, obj, target_id, "Delete", deps.actor_id)

################################################################################
