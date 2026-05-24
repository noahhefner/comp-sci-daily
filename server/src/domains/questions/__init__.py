from fastapi import APIRouter

from . import get_today, get_question_by_id, create_question

router = APIRouter()

router.include_router(get_today.router)
router.include_router(get_question_by_id.router)
router.include_router(create_question.router)
