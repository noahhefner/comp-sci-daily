from datetime import date
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import Connection

from src.dependencies.get_db import get_db
from src.dependencies.get_user import User, get_user
from src.domains.questions.choices_helper import ChoiceResponse, get_choices_for_question

router = APIRouter()


class CreateQuestionRequest(BaseModel):
    """Request model for creating a new question."""

    question: str
    difficulty: str
    choices: list[str]
    answer_letter: str
    explanation: str
    date: date


class CreateQuestionResponse(BaseModel):
    """Response model for created question."""

    id: UUID
    question: str
    difficulty: str
    date: date
    choices: list[ChoiceResponse]


@router.post("/", response_model=CreateQuestionResponse)
async def create_question(
    request: CreateQuestionRequest,
    db: Connection = Depends(get_db),
    user: User = Depends(get_user),
):
    """Create a new question with choices and answer."""

    # Validate difficulty
    if request.difficulty not in ("easy", "medium", "hard"):
        raise HTTPException(
            status_code=422, detail="difficulty must be 'easy', 'medium', or 'hard'"
        )

    # Validate answer letter
    if request.answer_letter not in ("A", "B", "C", "D", "E", "F"):
        raise HTTPException(status_code=422, detail="answer_letter must be A, B, C, D, E, or F")

    # Validate choices
    if len(request.choices) < 2:
        raise HTTPException(status_code=422, detail="choices must have at least 2 options")

    # Validate question text
    if not request.question or len(request.question.strip()) == 0:
        raise HTTPException(status_code=422, detail="question cannot be empty")

    # Validate explanation
    if not request.explanation or len(request.explanation.strip()) == 0:
        raise HTTPException(status_code=422, detail="explanation cannot be empty")

    try:
        # Generate question ID
        question_id = uuid4()

        # Insert the question
        insert_question_query = text(
            """
            INSERT INTO questions (id, question, difficulty, date)
            VALUES (:id, :question, :difficulty, :date)
            """
        )

        question_params = {
            "id": str(question_id),
            "question": request.question,
            "difficulty": request.difficulty,
            "date": request.date,
        }

        db.execute(insert_question_query, question_params)

        # Insert the choices
        for idx, choice_text in enumerate(request.choices):
            choice_id = uuid4()
            insert_choice_query = text(
                """
                INSERT INTO choices (id, question_id, choice_text)
                VALUES (:id, :question_id, :choice_text)
                """
            )
            choice_params = {
                "id": str(choice_id),
                "question_id": str(question_id),
                "choice_text": choice_text,
            }
            db.execute(insert_choice_query, choice_params)

        # Insert the answer
        answer_id = uuid4()
        insert_answer_query = text(
            """
            INSERT INTO answers (id, question_id, answer, explanation)
            VALUES (:id, :question_id, :answer, :explanation)
            """
        )
        answer_params = {
            "id": str(answer_id),
            "question_id": str(question_id),
            "answer": request.answer_letter,
            "explanation": request.explanation,
        }
        db.execute(insert_answer_query, answer_params)

        # Commit the transaction
        db.commit()

        # Fetch and return the created question with choices
        choices = await get_choices_for_question(question_id, db)

        return {
            "id": question_id,
            "question": request.question,
            "difficulty": request.difficulty,
            "date": request.date,
            "choices": choices,
        }

    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")
