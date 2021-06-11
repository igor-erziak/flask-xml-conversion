import pytest
from flask_app import create_app

@pytest.fixture
def app():
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_export(client):
    response = client.get('/export/6439416')

    assert response.status_code == 401