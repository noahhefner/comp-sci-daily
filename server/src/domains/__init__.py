from fastapi import APIRouter

from . import questions, answers

router = APIRouter()

router.include_router(
    questions.router,
    prefix="/questions",
    tags=["questions"],
)

router.include_router(
    answers.router,
    prefix="/answers",
    tags=["answers"],
)
