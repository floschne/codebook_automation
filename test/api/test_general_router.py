from fastapi.testclient import TestClient

from main import app
from api.model import BooleanResponse

client = TestClient(app)


def test_heartbeat():
    response = client.get("/heartbeat")
    assert response.status_code == 200
    assert response.json() == BooleanResponse(value=True)
