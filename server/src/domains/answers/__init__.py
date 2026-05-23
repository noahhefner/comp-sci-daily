from fastapi import APIRouter

from . import get_answer_by_question_id

router = APIRouter()

router.include_router(get_answer_by_question_id.router)
