import string
from sqlalchemy import TextClause
from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import Connection

from src.dependencies.get_db import get_db
from src.dependencies.get_user import User, get_user

router = APIRouter()


class ChoiceResponse(BaseModel):
    """Response model for a choice."""

    id: UUID
    choice_text: str

class TodayQuestionResponse(BaseModel):
    """Response model for today's question."""

    id: UUID
    question: str
    date: date
    choices: list[ChoiceResponse]


@router.get("/today", response_model=TodayQuestionResponse)
async def get_today_question(
    db: Connection = Depends(get_db),
    user: User = Depends(get_user),
):
    """Retrieve the question for today with all choices."""

    # Step 1: Fetch question

    question_query: TextClause = text(
        "SELECT id, question, date FROM questions WHERE date = CURRENT_DATE"
    )

    try:
        question_result = db.execute(question_query)
        question_row = question_result.mappings().one_or_none()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

    if not question_row:
        raise HTTPException(status_code=404, detail="Question not found.")

    question_id: UUID = question_row["id"]

    # Step 2: Fetch choices for question

    choices_query: TextClause = text("SELECT id, choice_text FROM choices WHERE question_id = :question_id")

    choices_params: dict[str, str] = {"question_id": str(question_id)}

    try:
        choices_result = db.execute(choices_query, choices_params)
        choices_rows = choices_result.mappings().all()

        choices: list[ChoiceResponse] = []
        for row in choices_rows:
            choices.append(
                ChoiceResponse(
                    id=row["id"],
                    choice_text=row["choice_text"],
                )
            )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

    return {**question_row, "choices": choices}