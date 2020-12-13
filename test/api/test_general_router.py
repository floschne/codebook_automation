import os
import sys

from starlette import status

sys.path.append(str(os.getcwd()))
from fastapi.testclient import TestClient

from main import app
from api.model import BooleanResponse

client = TestClient(app)


def test_heartbeat():
    response = client.get("/heartbeat")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == BooleanResponse(value=True)
