import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_export(client):
    """Test the whole export pipeline."""
    # TODO remove the credentials
    response = client.get('/export/6422949', auth=('myUser123', 'secretSecret'))

    assert response.status_code == 200
    # check if we got success
    data = response.json
    assert data["success"] == True
