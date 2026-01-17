import pytest
from src.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


#T1 - unit test
def test_index_returns_project_name(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"ProjectDevOps" in response.data


#T2 - Logic
def test_health_logic_without_db(monkeypatch, client):

    class FakeCursor:
        def execute(self, query):
            pass

        def fetchone(self):
            return [5]

        def close(self):
            pass

    class FakeConnection:
        def cursor(self):
            return FakeCursor()

        def close(self):
            pass

    def fake_get_connection():
        return FakeConnection()

    monkeypatch.setattr("src.main.get_connection", fake_get_connection)

    response = client.get("/health")

    assert response.status_code == 200
    json_data = response.get_json()

    assert json_data["status"] == "ok"
    assert json_data["users"] == 5
    assert json_data["items"] == 5


#T3 HTTP endpoint
def test_health_endpoint_response_structure(monkeypatch, client):

    class FakeCursor:
        def execute(self, query):
            pass

        def fetchone(self):
            return [1]

        def close(self):
            pass

    class FakeConnection:
        def cursor(self):
            return FakeCursor()

        def close(self):
            pass

    monkeypatch.setattr("src.main.get_connection", lambda: FakeConnection())

    response = client.get("/health")

    assert response.status_code == 200
    assert "status" in response.json
    assert "users" in response.json
    assert "items" in response.json
