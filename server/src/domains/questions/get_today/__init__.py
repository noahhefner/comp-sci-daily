from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import Connection

from src.dependencies.get_db import get_db
from src.dependencies.get_user import User, get_user
from src.domains.questions.choices_helper import ChoiceResponse, get_choices_for_question

router = APIRouter()


class TodayQuestionResponse(BaseModel):
    """Response model for today's question."""

    id: UUID
    question: str
    difficulty: str
    date: date
    choices: list[ChoiceResponse]


@router.get("/today", response_model=TodayQuestionResponse)
async def get_today_question(
    db: Connection = Depends(get_db),
    user: User = Depends(get_user),
):
    """Retrieve the question for today with all choices."""

    query = text(
        "SELECT id, question, difficulty, date FROM questions WHERE date = CURRENT_DATE LIMIT 1"
    )

    try:
        result = db.execute(query)
        row = result.mappings().one_or_none()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

    if not row:
        raise HTTPException(status_code=404, detail="No question available for today")

    question_id = row["id"]
    choices = await get_choices_for_question(question_id, db)

    return {**row, "choices": choices}
