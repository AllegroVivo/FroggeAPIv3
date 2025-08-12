from __future__ import annotations

from typing import List, Union, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlalchemy.orm import selectinload

from .Common import *
from .. import Models, Schemas
from ..dependencies import get_dependencies, Dependencies
################################################################################

router = APIRouter(prefix="/forms", tags=["Fillable Forms"])

################################################################################
def full_form_select(
    deps: Dependencies,
    mode: Literal["All", "Single"] = "Single",
    form_id: Optional[int] = None
):

    query = deps.db.query(Models.FormModel).filter_by(guild_id=deps.guild_id).options(
        selectinload(Models.FormModel.post_options),
        selectinload(Models.FormModel.questions).selectinload(Models.FormQuestionModel.responses),
        selectinload(Models.FormModel.questions).selectinload(Models.FormQuestionModel.options),
        selectinload(Models.FormModel.questions).selectinload(Models.FormQuestionModel.prompts),
        selectinload(Models.FormModel.response_collections),
        selectinload(Models.FormModel.prompts)
    )

    if mode == "All":
        return query.all()
    elif mode == "Single":
        assert form_id is not None
        return query.filter_by(id=form_id).first()

################################################################################
def full_question_select(
    form_id: int,
    deps: Dependencies,
    mode: Literal["All", "Single"] = "Single",
    question_id: Optional[int] = None
):

    query = deps.db.query(Models.FormQuestionModel).filter_by(form_id=form_id).options(
        selectinload(Models.FormQuestionModel.responses),
        selectinload(Models.FormQuestionModel.options),
        selectinload(Models.FormQuestionModel.prompts)
    )

    if mode == "All":
        return query.all()
    elif mode == "Single":
        assert question_id is not None
        return query.filter_by(id=question_id).first()

################################################################################
# GET Requests
################################################################################
@router.get("/", response_model=List[Schemas.DeepFormSchema])
def get_forms(deps: Dependencies = Depends(get_dependencies)) -> List[Schemas.DeepFormSchema]:

    forms = full_form_select(deps, "All")
    return [map_form(form) for form in forms]

################################################################################
@router.get("/{form_id}", response_model=Schemas.DeepFormSchema)
def get_form(
    form_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepFormSchema:

    form = get_shallow_or_404(deps.db, Models.FormModel, id=form_id)
    match_or_403(deps.guild_id, form.guild_id)

    form = full_form_select(deps, "Single", form_id=form.id)
    return map_form(form)

################################################################################
# POST Requests
################################################################################
@router.post("/", status_code=201, response_model=Schemas.DeepFormSchema)
def create_form(deps: Dependencies = Depends(get_dependencies)) -> Schemas.DeepFormSchema:

    form = Models.FormModel(guild_id=deps.guild_id)
    deps.db.add(form)
    deps.db.flush()
    deps.db.refresh(form)

    # Also add the post options and prompt table records
    post_opts = Models.FormPostOptionsModel(form_id=form.id)
    pre_prompt = Models.FormPromptModel(form_id=form.id, prompt_type=0)
    post_prompt = Models.FormPromptModel(form_id=form.id, prompt_type=1)
    deps.db.add_all([post_opts, pre_prompt, post_prompt])
    deps.db.flush()

    form = full_form_select(deps, "Single", form_id=form.id)
    audit_log_create(deps, form, form.id)

    return map_form(form)

################################################################################
@router.post("/{form_id}/response-collections", status_code=201, response_model=Schemas.FormResponseCollectionSchema)
def create_form_response_collection(
    form_id: int,
    data: Schemas.FormResponseCollectionCreateSchema,
    deps: Dependencies = Depends(get_dependencies),
) -> Schemas.FormResponseCollectionSchema:

    form = get_shallow_or_404(deps.db, Models.FormModel, id=form_id)
    match_or_403(deps.guild_id, form.guild_id)

    response_collection = Models.FormResponseCollectionModel(form_id=form.id, **data.model_dump())
    deps.db.add(response_collection)
    deps.db.flush()
    deps.db.refresh(response_collection)

    audit_log_create(deps, response_collection, response_collection.id)

    return Schemas.FormResponseCollectionSchema.model_validate(response_collection)

################################################################################
@router.post("/{form_id}/questions", status_code=201, response_model=Schemas.DeepFormQuestionSchema)
def create_form_question(
    form_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepFormQuestionSchema:

    form = get_shallow_or_404(deps.db, Models.FormModel, id=form_id)
    match_or_403(deps.guild_id, form.guild_id)

    existing = deps.db.query(Models.FormQuestionModel).filter_by(form_id=form.id).all()
    existing.sort(key=lambda x: x.sort_order)

    new_question = Models.FormQuestionModel(form_id=form.id, sort_order=next_sort_order(existing))
    deps.db.add(new_question)
    deps.db.flush()
    deps.db.refresh(new_question)

    pre_prompt = Models.FormPromptModel(question_id=new_question.id, prompt_type=0)
    post_prompt = Models.FormPromptModel(question_id=new_question.id, prompt_type=1)

    deps.db.add_all([pre_prompt, post_prompt])
    deps.db.flush()

    new_question = full_question_select(form.id, deps, "Single", question_id=new_question.id)
    audit_log_create(deps, new_question, new_question.id)

    return map_form_question(new_question)

################################################################################
@router.post("/{form_id}/questions/{question_id}/options", status_code=201, response_model=Schemas.FormQuestionOptionSchema)
def create_form_question_option(
    form_id: int,
    question_id: int,
    deps: Dependencies = Depends(get_dependencies),
) -> Schemas.FormQuestionOptionSchema:

    form = get_shallow_or_404(deps.db, Models.FormModel, id=form_id)
    match_or_403(deps.guild_id, form.guild_id)

    question = get_shallow_or_404(deps.db, Models.FormQuestionModel, id=question_id)
    match_or_403(form.id, question.form_id)

    existing = deps.db.query(Models.FormQuestionOptionModel).filter_by(question_id=question.id).all()
    existing.sort(key=lambda x: x.sort_order)

    option = Models.FormQuestionOptionModel(question_id=question.id, sort_order=next_sort_order(existing))
    deps.db.add(option)
    deps.db.flush()
    deps.db.refresh(option)

    audit_log_create(deps, option, option.id)

    return Schemas.FormQuestionOptionSchema.model_validate(option)

################################################################################
@router.post("/{form_id}/questions/{question_id}/responses", status_code=201, response_model=Schemas.FormQuestionResponseSchema)
def create_form_question_response(
    form_id: int,
    question_id: int,
    data: Schemas.FormQuestionResponseCreateSchema,
    deps: Dependencies = Depends(get_dependencies),
) -> Schemas.FormQuestionResponseSchema:

    form = get_shallow_or_404(deps.db, Models.FormModel, id=form_id)
    match_or_403(deps.guild_id, form.guild_id)

    question = get_shallow_or_404(deps.db, Models.FormQuestionModel, id=question_id)
    match_or_403(form.id, question.form_id)

    response = Models.FormQuestionResponseModel(question_id=question.id, **data.model_dump())
    deps.db.add(response)
    deps.db.flush()
    deps.db.refresh(response)

    audit_log_create(deps, response, response.id)

    return Schemas.FormQuestionResponseSchema.model_validate(response)

################################################################################
# DELETE Requests
################################################################################
@router.delete("/{form_id}", status_code=204)
def delete_form(
    form_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Response:

    form = get_shallow_or_404(deps.db, Models.FormModel, id=form_id)
    match_or_403(deps.guild_id, form.guild_id)

    deps.db.delete(form)
    audit_log_delete(deps, form, form.id)
    deps.db.flush()

    return Response(status_code=204)

################################################################################
@router.delete("/{form_id}/questions/{question_id}", status_code=204)
def delete_form_question(
    form_id: int,
    question_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Response:

    form = get_shallow_or_404(deps.db, Models.FormModel, id=form_id)
    match_or_403(deps.guild_id, form.guild_id)

    question = get_shallow_or_404(deps.db, Models.FormQuestionModel, id=question_id)
    match_or_403(form.id, question.form_id)

    deps.db.delete(question)
    audit_log_delete(deps, question, question.id)
    deps.db.flush()

    return Response(status_code=204)

################################################################################
@router.delete("/{form_id}/questions/{question_id}/options/{option_id}", status_code=204)
def delete_form_question_option(
    form_id: int,
    question_id: int,
    option_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Response:

    form = get_shallow_or_404(deps.db, Models.FormModel, id=form_id)
    match_or_403(deps.guild_id, form.guild_id)

    question = get_shallow_or_404(deps.db, Models.FormQuestionModel, id=question_id)
    match_or_403(form.id, question.form_id)

    option = get_shallow_or_404(deps.db, Models.FormQuestionOptionModel, id=option_id)
    match_or_403(question.id, option.question_id)

    deps.db.delete(option)
    audit_log_delete(deps, option, option.id)
    deps.db.flush()

    return Response(status_code=204)

################################################################################
# PATCH Requests
################################################################################
@router.patch("/{form_id}", response_model=Schemas.DeepFormSchema)
def patch_form(
    form_id: int,
    data: Schemas.FormUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepFormSchema:

    form = get_shallow_or_404(deps.db, Models.FormModel, id=form_id)
    match_or_403(deps.guild_id, form.guild_id)

    apply_updates(form, data)
    audit_log_update(deps, form, form.id)

    deps.db.flush()
    deps.db.refresh(form)

    return map_form(form)

################################################################################
@router.patch("/{form_id}/prompts/{prompt_id}/", response_model=Schemas.FormPromptSchema)
def patch_form_prompt(
    form_id: int,
    prompt_id: int,
    data: Schemas.FormPromptUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.FormPromptSchema:

    form = get_shallow_or_404(deps.db, Models.FormModel, id=form_id)
    match_or_403(deps.guild_id, form.guild_id)

    prompt = get_shallow_or_404(deps.db, Models.FormPromptModel, id=prompt_id)
    match_or_403(form.id, prompt.form_id)

    apply_updates(prompt, data)
    audit_log_update(deps, prompt, prompt.id)

    deps.db.flush()
    deps.db.refresh(prompt)

    return Schemas.FormPromptSchema.model_validate(prompt)

################################################################################
@router.patch("/{form_id}/post-options", response_model=Schemas.FormPostOptionsSchema)
def patch_form_post_options(
    form_id: int,
    data: Schemas.FormPostOptionsUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.FormPostOptionsSchema:

    form = get_shallow_or_404(deps.db, Models.FormModel, id=form_id)
    match_or_403(deps.guild_id, form.guild_id)

    post_options = get_shallow_or_404(deps.db, Models.FormPostOptionsModel, form_id=form.id)

    apply_updates(post_options, data)
    audit_log_update(deps, post_options, form.id)

    deps.db.flush()
    deps.db.refresh(post_options)

    return Schemas.FormPostOptionsSchema.model_validate(post_options)

################################################################################
@router.patch("/{form_id}/questions/{question_id}", response_model=Schemas.DeepFormQuestionSchema)
def patch_form_question(
    form_id: int,
    question_id: int,
    data: Schemas.FormQuestionUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepFormQuestionSchema:

    form = get_shallow_or_404(deps.db, Models.FormModel, id=form_id)
    match_or_403(deps.guild_id, form.guild_id)

    question = get_shallow_or_404(deps.db, Models.FormQuestionModel, id=question_id)
    match_or_403(form.id, question.form_id)

    apply_updates(question, data)
    audit_log_update(deps, question, question.id)

    deps.db.flush()
    deps.db.refresh(question)

    return map_form_question(question)

################################################################################
@router.patch("/{form_id}/questions/{question_id}/prompts/{prompt_id}/", response_model=Schemas.FormPromptSchema)
def patch_form_question_prompt(
    form_id: int,
    question_id: int,
    prompt_id: int,
    data: Schemas.FormPromptUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.FormPromptSchema:

    form = get_shallow_or_404(deps.db, Models.FormModel, id=form_id)
    match_or_403(deps.guild_id, form.guild_id)

    question = get_shallow_or_404(deps.db, Models.FormQuestionModel, id=question_id)
    match_or_403(form.id, question.form_id)

    prompt = get_shallow_or_404(deps.db, Models.FormPromptModel, id=prompt_id)
    match_or_403(question.id, prompt.question_id)

    apply_updates(prompt, data)
    audit_log_update(deps, prompt, prompt.id)

    deps.db.flush()
    deps.db.refresh(prompt)

    return Schemas.FormPromptSchema.model_validate(prompt)

################################################################################
@router.patch("/{form_id}/questions/{question_id}/responses/{response_id}", response_model=Schemas.FormQuestionResponseSchema)
def patch_form_question_response(
    form_id: int,
    question_id: int,
    response_id: int,
    data: Schemas.FormQuestionResponseUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.FormQuestionResponseSchema:

    form = get_shallow_or_404(deps.db, Models.FormModel, id=form_id)
    match_or_403(deps.guild_id, form.guild_id)

    question = get_shallow_or_404(deps.db, Models.FormQuestionModel, id=question_id)
    match_or_403(form.id, question.form_id)

    response = get_shallow_or_404(deps.db, Models.FormQuestionResponseModel, id=response_id)
    match_or_403(question.id, response.question_id)

    apply_updates(response, data)
    audit_log_update(deps, response, response.id)

    deps.db.flush()
    deps.db.refresh(response)

    return Schemas.FormQuestionResponseSchema.model_validate(response)

################################################################################
@router.patch("/{form_id}/questions/{question_id}/options/{option_id}", response_model=Schemas.FormQuestionOptionSchema)
def patch_form_question_option(
    form_id: int,
    question_id: int,
    option_id: int,
    data: Schemas.FormQuestionOptionUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.FormQuestionOptionSchema:

    form = get_shallow_or_404(deps.db, Models.FormModel, id=form_id)
    match_or_403(deps.guild_id, form.guild_id)

    question = get_shallow_or_404(deps.db, Models.FormQuestionModel, id=question_id)
    match_or_403(form.id, question.form_id)

    option = get_shallow_or_404(deps.db, Models.FormQuestionOptionModel, id=option_id)
    match_or_403(question.id, option.question_id)

    apply_updates(option, data)
    audit_log_update(deps, option, option.id)

    deps.db.flush()
    deps.db.refresh(option)

    return Schemas.FormQuestionOptionSchema.model_validate(option)

################################################################################
