import string
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import Connection


class ChoiceResponse(BaseModel):
    """Response model for a choice."""

    id: UUID
    choice_text: str
    choice_letter: str


async def get_choices_for_question(question_id: UUID, db: Connection) -> list[ChoiceResponse]:
    """Fetch all choices for a given question."""

    query = text("SELECT id, choice_text FROM choices WHERE question_id = :question_id")

    params = {"question_id": str(question_id)}

    try:
        result = db.execute(query, params)
        rows = result.mappings().all()

        choices = []
        for index, row in enumerate(rows):
            choice_letter = string.ascii_uppercase[index]
            choices.append(
                ChoiceResponse(
                    id=row["id"],
                    choice_text=row["choice_text"],
                    choice_letter=choice_letter,
                )
            )
        return choices
    except Exception as e:
        print(e)
        return []
