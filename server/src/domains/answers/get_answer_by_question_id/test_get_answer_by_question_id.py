def test_get_answer_by_question_id(client):
    response = client.get("/answers/11111111-1111-1111-1111-111111111111")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "aaaaaaaa-aaaa-aaaa-aaaa-000000000001"
    assert data["question_id"] == "11111111-1111-1111-1111-111111111111"
    assert data["answer"] == "Central Processing Unit"
    assert (
        data["explanation"]
        == "The CPU is the primary component of a computer that performs most of the processing inside the computer."
    )


def test_get_answer_by_question_id_different_question(client):
    response = client.get("/answers/22222222-2222-2222-2222-222222222222")

    assert response.status_code == 200
    data = response.json()
    assert data["question_id"] == "22222222-2222-2222-2222-222222222222"
    assert data["answer"] == "O(log n)"


def test_get_answer_by_question_id_not_found(client):
    response = client.get("/answers/ffffffff-ffff-ffff-ffff-ffffffffffff")

    assert response.status_code == 404
    assert response.json()["detail"] == "Answer not found for this question"
