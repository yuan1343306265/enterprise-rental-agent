from fastapi.testclient import TestClient

from app.main import app

async def fake_rental_agent(
        message:str,
        session_id:str,
) ->str:
    return"自动化测试回答"


def test_chat_with_agent(monkeypatch):
    monkeypatch.setattr(
        "app.main.ask_rental_agent",
        fake_rental_agent,
    )

    with TestClient(app) as client:
        response = client.post(
            "/api/chat",
            json={
                "message":"我想找一套房子",
                "session_id":"api-test-1",
            },
        )

    assert response.status_code ==200
    assert response.json()=={
        "success":True,
        "reply" : "自动化测试回答",
        "session_id": "api-test-1",
    }    

def test_chat_rejects_empty_message():
    with TestClient(app) as client:
        response = client.post(
            "/api/chat",
            json={
                "message":"",
                "session_id":"validation-test-1",
            },
        )

        assert response.status_code == 422