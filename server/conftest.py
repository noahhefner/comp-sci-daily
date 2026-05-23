import tempfile
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from src.dependencies.get_db import get_db
from src.dependencies.get_user import get_user, User
from src.main import app


@pytest.fixture
def client():
    with tempfile.NamedTemporaryFile() as tmp:
        DATABASE_URL = f"sqlite:///{tmp.name}"

        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
        )

        # ---- Create schema + seed data ----
        with engine.connect() as conn:
            # QUESTIONS TABLE
            conn.execute(
                text("""
                CREATE TABLE questions (
                    id TEXT PRIMARY KEY,
                    question TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    date TEXT NOT NULL
                )
            """)
            )

            conn.execute(
                text(
                    "INSERT INTO questions (id, question, difficulty, date) VALUES (:id, :question, :difficulty, :date)"
                ),
                [
                    {
                        "id": "11111111-1111-1111-1111-111111111111",
                        "question": "What does CPU stand for?",
                        "difficulty": "easy",
                        "date": str(date.today()),
                    },
                    {
                        "id": "22222222-2222-2222-2222-222222222222",
                        "question": "What is the time complexity of binary search?",
                        "difficulty": "medium",
                        "date": "2024-01-01",
                    },
                    {
                        "id": "33333333-3333-3333-3333-333333333333",
                        "question": "Explain the concept of polymorphism in OOP.",
                        "difficulty": "hard",
                        "date": "2024-01-02",
                    },
                ],
            )

            # CHOICES TABLE
            conn.execute(
                text("""
                CREATE TABLE choices (
                    id TEXT PRIMARY KEY,
                    question_id TEXT NOT NULL,
                    choice_text TEXT NOT NULL,
                    FOREIGN KEY (question_id) REFERENCES questions(id)
                )
            """)
            )

            conn.execute(
                text(
                    "INSERT INTO choices (id, question_id, choice_text) VALUES (:id, :question_id, :choice_text)"
                ),
                [
                    {
                        "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                        "question_id": "11111111-1111-1111-1111-111111111111",
                        "choice_text": "Central Processing Unit",
                    },
                    {
                        "id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
                        "question_id": "11111111-1111-1111-1111-111111111111",
                        "choice_text": "Central Program Utility",
                    },
                    {
                        "id": "cccccccc-cccc-cccc-cccc-cccccccccccc",
                        "question_id": "11111111-1111-1111-1111-111111111111",
                        "choice_text": "Computer Personal Unit",
                    },
                    {
                        "id": "dddddddd-dddd-dddd-dddd-dddddddddddd",
                        "question_id": "22222222-2222-2222-2222-222222222222",
                        "choice_text": "O(log n)",
                    },
                    {
                        "id": "eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee",
                        "question_id": "22222222-2222-2222-2222-222222222222",
                        "choice_text": "O(n)",
                    },
                    {
                        "id": "ffffffff-ffff-ffff-ffff-ffffffffffff",
                        "question_id": "22222222-2222-2222-2222-222222222222",
                        "choice_text": "O(n^2)",
                    },
                    {
                        "id": "12121212-1212-1212-1212-121212121212",
                        "question_id": "33333333-3333-3333-3333-333333333333",
                        "choice_text": "Same method, different forms",
                    },
                    {
                        "id": "34343434-3434-3434-3434-343434343434",
                        "question_id": "33333333-3333-3333-3333-333333333333",
                        "choice_text": "Multiple inheritance only",
                    },
                    {
                        "id": "56565656-5656-5656-5656-565656565656",
                        "question_id": "33333333-3333-3333-3333-333333333333",
                        "choice_text": "Static method usage",
                    },
                ],
            )

            # ANSWERS TABLE
            conn.execute(
                text("""
                CREATE TABLE answers (
                    id TEXT PRIMARY KEY,
                    question_id TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    explanation TEXT NOT NULL,
                    FOREIGN KEY (question_id) REFERENCES questions(id)
                )
            """)
            )

            conn.execute(
                text(
                    "INSERT INTO answers (id, question_id, answer, explanation) VALUES (:id, :question_id, :answer, :explanation)"
                ),
                [
                    {
                        "id": "aaaaaaaa-aaaa-aaaa-aaaa-000000000001",
                        "question_id": "11111111-1111-1111-1111-111111111111",
                        "answer": "Central Processing Unit",
                        "explanation": "The CPU is the primary component of a computer that performs most of the processing inside the computer.",
                    },
                    {
                        "id": "bbbbbbbb-bbbb-bbbb-bbbb-000000000002",
                        "question_id": "22222222-2222-2222-2222-222222222222",
                        "answer": "O(log n)",
                        "explanation": "Binary search has a time complexity of O(log n) because it divides the search space in half with each iteration.",
                    },
                    {
                        "id": "cccccccc-cccc-cccc-cccc-000000000003",
                        "question_id": "33333333-3333-3333-3333-333333333333",
                        "answer": "Same method, different forms",
                        "explanation": "Polymorphism allows objects of different types to be treated as objects of a common superclass, enabling the same method to behave differently based on the object type.",
                    },
                ],
            )

            conn.commit()

        # ---- Override dependency ----
        def override_get_db():
            with engine.connect() as connection:
                yield connection

        async def override_get_user() -> User:
            return User(
                id="test-user-id",
                email="test@example.com",
                sub="test-user-id",
            )

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_user] = override_get_user

        with TestClient(app) as client:
            yield client

        app.dependency_overrides.clear()

