from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import Connection

from src.dependencies.get_db import get_db
from src.dependencies.get_user import User, get_user
from src.domains.questions.choices_helper import ChoiceResponse, get_choices_for_question

router = APIRouter()


class QuestionResponse(BaseModel):
    """Response model for a single question."""

    id: UUID
    question: str
    difficulty: str
    choices: list[ChoiceResponse]


@router.get("/{id}", response_model=QuestionResponse)
async def get_question_by_id(
    id: Annotated[UUID, Path(description="ID of the question")],
    db: Connection = Depends(get_db),
    user: User = Depends(get_user),
):
    """Retrieve a question by its ID with all choices."""

    query = text("SELECT id, question, difficulty FROM questions WHERE id = :id")

    params = {"id": str(id)}

    try:
        result = db.execute(query, params)
        row = result.mappings().one_or_none()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

    if not row:
        raise HTTPException(status_code=404, detail="Question not found")

    choices = await get_choices_for_question(id, db)

    return {**row, "choices": choices}
