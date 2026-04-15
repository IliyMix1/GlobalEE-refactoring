from fastapi.testclient import TestClient
from routes.legacy import app

client = TestClient(app)

def test_get_all_students():
    response = client.get('/students')
    assert response.status_code == 200
