import pytest
from app import app  # assumes your Flask code is in app.py

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_chat_route(client):
    response = client.post('/chat', json={"message": "Hello"})
    assert response.status_code == 200
    assert "response" in response.get_json()

def test_summarize_route(client):
    response = client.post('/summarize', json={"text": "Python is a popular programming language."})
    assert response.status_code == 200
    assert "summary" in response.get_json()

def test_rephrase_route(client):
    response = client.post('/rephrase', json={"text": "This is a test."})
    assert response.status_code == 200
    assert "rephrased" in response.get_json()
