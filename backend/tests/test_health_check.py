from http import HTTPStatus

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_health_check():
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'status': 'ok'}
