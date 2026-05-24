import string
from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.sql.elements import TextClause

from src.dependencies.get_db import get_db
from src.dependencies.get_user import User, get_user

router = APIRouter()


class CreateQuestionRequest(BaseModel):
    question: str
    date: date
    choices: list[str]
    answer_index: int
    explanation: str


class CreateQuestionResponse(BaseModel):
    id: UUID


@router.post("/", response_model=CreateQuestionResponse)
async def create_question(
    request: CreateQuestionRequest,
    db: Connection = Depends(get_db),
    user: User = Depends(get_user),
):

    # Validation

    if len(request.question.strip()) == 0:
        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty.",
        )

    if len(request.explanation.strip()) == 0:
        raise HTTPException(
            status_code=422,
            detail="Explanation cannot be empty.",
        )

    if len(request.choices) < 2:
        raise HTTPException(
            status_code=422,
            detail="Must provide two or more choices.",
        )

    if (
        request.answer_index < 0
        or request.answer_index >= len(request.choices)
    ):
        raise HTTPException(
            status_code=422,
            detail="Invalid answer index.",
        )

    for choice in request.choices:
        if len(choice.strip()) == 0:
            raise HTTPException(
                status_code=422,
                detail="Choices cannot be empty.",
            )

    try:

        # Insert question

        question_query: TextClause = text("""
            INSERT INTO questions (question, date)
            VALUES (:question, :date)
            RETURNING id
        """)

        question_params = {
            "question": request.question.strip(),
            "date": request.date,
        }

        question_result = db.execute(
            question_query,
            question_params,
        )

        question_id: UUID = question_result.scalar_one()

        # Insert choices

        inserted_choice_ids: list[UUID] = []

        choice_query: TextClause = text("""
            INSERT INTO choices (question_id, choice_text)
            VALUES (:question_id, :choice_text)
            RETURNING id
        """)

        for choice in request.choices:

            choice_result = db.execute(
                choice_query,
                {
                    "question_id": question_id,
                    "choice_text": choice.strip(),
                },
            )

            inserted_choice_ids.append(
                choice_result.scalar_one()
            )

        # Insert answer

        answer_query: TextClause = text("""
            INSERT INTO answers (
                question_id,
                choice_id,
                explanation
            )
            VALUES (
                :question_id,
                :choice_id,
                :explanation
            )
        """)

        db.execute(
            answer_query,
            {
                "question_id": question_id,
                "choice_id": inserted_choice_ids[
                    request.answer_index
                ],
                "explanation": request.explanation.strip(),
            },
        )

        db.commit()

        return {"id": question_id}

    except Exception as e:

        db.rollback()

        print(e)

        # Unique date constraint
        if "questions_date_key" in str(e):
            raise HTTPException(
                status_code=409,
                detail="A question already exists for this date.",
            )

        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )