from src.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health_check():
    # Arrage & Act
    response = client.get("/health")
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}