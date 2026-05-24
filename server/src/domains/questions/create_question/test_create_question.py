from datetime import date, timedelta


def test_create_question_success(client):
    """Test creating a question with valid data."""
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    payload = {
        "question": "What is the time complexity of merge sort?",
        "difficulty": "medium",
        "choices": ["O(n)", "O(n log n)", "O(n^2)", "O(log n)", "O(1)"],
        "answer_letter": "B",
        "explanation": "Merge sort has a time complexity of O(n log n) in all cases.",
        "date": tomorrow,
    }

    response = client.post("/questions", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "What is the time complexity of merge sort?"
    assert data["difficulty"] == "medium"
    assert data["date"] == tomorrow
    assert len(data["choices"]) == 5
    assert data["id"] is not None


def test_create_question_with_valid_answer_letters(client):
    """Test creating questions with different valid answer letters."""
    for answer_letter in ["A", "B", "C", "D", "E", "F"]:
        tomorrow = (date.today() + timedelta(days=1)).isoformat()

        payload = {
            "question": f"Test question with answer {answer_letter}?",
            "difficulty": "easy",
            "choices": ["Option A", "Option B", "Option C", "Option D", "Option E", "Option F"],
            "answer_letter": answer_letter,
            "explanation": f"The correct answer is {answer_letter}.",
            "date": tomorrow,
        }

        response = client.post("/questions", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["question"] == f"Test question with answer {answer_letter}?"


def test_create_question_with_minimum_choices(client):
    """Test creating a question with minimum number of choices (2)."""
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    payload = {
        "question": "Is Python a programming language?",
        "difficulty": "easy",
        "choices": ["Yes", "No"],
        "answer_letter": "A",
        "explanation": "Python is indeed a programming language.",
        "date": tomorrow,
    }

    response = client.post("/questions", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert len(data["choices"]) == 2


def test_create_question_invalid_difficulty(client):
    """Test creating a question with invalid difficulty."""
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    payload = {
        "question": "Test question?",
        "difficulty": "impossible",  # Invalid difficulty
        "choices": ["Yes", "No"],
        "answer_letter": "A",
        "explanation": "Explanation.",
        "date": tomorrow,
    }

    response = client.post("/questions", json=payload)

    assert response.status_code == 422  # Validation error


def test_create_question_invalid_answer_letter(client):
    """Test creating a question with invalid answer letter."""
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    payload = {
        "question": "Test question?",
        "difficulty": "easy",
        "choices": ["Yes", "No"],
        "answer_letter": "Z",  # Invalid answer letter
        "explanation": "Explanation.",
        "date": tomorrow,
    }

    response = client.post("/questions", json=payload)

    assert response.status_code == 422  # Validation error


def test_create_question_too_few_choices(client):
    """Test creating a question with fewer than 2 choices."""
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    payload = {
        "question": "Test question?",
        "difficulty": "easy",
        "choices": ["Only one choice"],  # Only 1 choice, needs at least 2
        "answer_letter": "A",
        "explanation": "Explanation.",
        "date": tomorrow,
    }

    response = client.post("/questions", json=payload)

    assert response.status_code == 422  # Validation error


def test_create_question_missing_question_text(client):
    """Test creating a question with missing question text."""
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    payload = {
        # Missing "question" field
        "difficulty": "easy",
        "choices": ["Yes", "No"],
        "answer_letter": "A",
        "explanation": "Explanation.",
        "date": tomorrow,
    }

    response = client.post("/questions", json=payload)

    assert response.status_code == 422  # Validation error


def test_create_question_empty_question_text(client):
    """Test creating a question with empty question text."""
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    payload = {
        "question": "",  # Empty question
        "difficulty": "easy",
        "choices": ["Yes", "No"],
        "answer_letter": "A",
        "explanation": "Explanation.",
        "date": tomorrow,
    }

    response = client.post("/questions", json=payload)

    assert response.status_code == 422  # Validation error


def test_create_question_empty_explanation(client):
    """Test creating a question with empty explanation."""
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    payload = {
        "question": "Test question?",
        "difficulty": "easy",
        "choices": ["Yes", "No"],
        "answer_letter": "A",
        "explanation": "",  # Empty explanation
        "date": tomorrow,
    }

    response = client.post("/questions", json=payload)

    assert response.status_code == 422  # Validation error


def test_create_question_choices_returned_in_order(client):
    """Test that choices are returned in the order they were provided."""
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    choices = ["First", "Second", "Third", "Fourth"]
    payload = {
        "question": "Which is first?",
        "difficulty": "easy",
        "choices": choices,
        "answer_letter": "A",
        "explanation": "The first option is first.",
        "date": tomorrow,
    }

    response = client.post("/questions", json=payload)

    assert response.status_code == 200
    data = response.json()
    returned_choices = [choice["choice_text"] for choice in data["choices"]]
    assert returned_choices == choices
