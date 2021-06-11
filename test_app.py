import pytest
from flask_app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_export(client):
    response = client.get('/export/6439416', auth=('myUser123', 'secretSecret'))

    assert response.status_code == 200
    data = response.json
    assert data["success"] == True