def test_get_today_question(client):
    response = client.get("/questions/today")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "11111111-1111-1111-1111-111111111111"
    assert data["question"] == "What does CPU stand for?"
    assert data["difficulty"] == "easy"
    assert len(data["choices"]) == 3
    assert data["choices"][0]["choice_letter"] == "A"
    assert data["choices"][1]["choice_letter"] == "B"
    assert data["choices"][2]["choice_letter"] == "C"


def test_get_today_question_has_correct_choices(client):
    response = client.get("/questions/today")

    assert response.status_code == 200
    data = response.json()
    choices = data["choices"]
    assert choices[0]["choice_text"] == "Central Processing Unit"
    assert choices[1]["choice_text"] == "Central Program Utility"
    assert choices[2]["choice_text"] == "Computer Personal Unit"
