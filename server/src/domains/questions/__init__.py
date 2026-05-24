from fastapi import APIRouter

from . import create_question, get_question_by_id, get_today

router = APIRouter()

router.include_router(get_today.router)
router.include_router(get_question_by_id.router)
router.include_router(create_question.router)
