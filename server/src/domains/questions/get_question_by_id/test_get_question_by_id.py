def test_get_question_by_id(client):
    response = client.get("/questions/22222222-2222-2222-2222-222222222222")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "22222222-2222-2222-2222-222222222222"
    assert data["question"] == "What is the time complexity of binary search?"
    assert data["difficulty"] == "medium"


def test_get_question_by_id_includes_choices(client):
    response = client.get("/questions/22222222-2222-2222-2222-222222222222")

    assert response.status_code == 200
    data = response.json()
    assert len(data["choices"]) == 3
    assert data["choices"][0]["choice_letter"] == "A"
    assert data["choices"][0]["choice_text"] == "O(log n)"
    assert data["choices"][1]["choice_letter"] == "B"
    assert data["choices"][1]["choice_text"] == "O(n)"
    assert data["choices"][2]["choice_letter"] == "C"
    assert data["choices"][2]["choice_text"] == "O(n^2)"


def test_get_question_by_id_not_found(client):
    response = client.get("/questions/ffffffff-ffff-ffff-ffff-ffffffffffff")

    assert response.status_code == 404
    assert response.json()["detail"] == "Question not found"
