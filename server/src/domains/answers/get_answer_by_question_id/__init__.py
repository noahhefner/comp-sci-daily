from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import Connection

from src.dependencies.get_db import get_db
from src.dependencies.get_user import User, get_user

router = APIRouter()


class AnswerResponse(BaseModel):
    """Response model for an answer."""

    id: UUID
    question_id: UUID
    choice_id: UUID
    explanation: str


@router.get("/{question_id}", response_model=AnswerResponse)
async def get_answer_by_question_id(
    question_id: Annotated[UUID, Path(description="ID of the question")],
    db: Connection = Depends(get_db),
    user: User = Depends(get_user),
):
    """Retrieve an answer by question ID."""

    query = text(
        "SELECT id, question_id, choice_id, explanation FROM answers WHERE question_id = :question_id"
    )

    params = {"question_id": str(question_id)}

    try:
        result = db.execute(query, params)
        row = result.mappings().one_or_none()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

    if not row:
        raise HTTPException(status_code=404, detail="Answer not found for this question")

    return row
