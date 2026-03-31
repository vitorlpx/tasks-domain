import pytest

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# --- testes ---

@pytest.fixture(autouse=True)
def token():
    # Cria um usuário e obtém um token de autenticação para os testes
    user_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "Test!@Password#123"
    }
    
    client.post("/auth/register", json=user_data)
    response = client.post("/auth/login", json={"email": user_data["email"], "password": user_data["password"]})
        
    return response.json().get("access_token")

def test_create_task(token):
    # Arrange & Act
    response = client.post("/tasks/", headers={"Authorization": f"Bearer {token}"}, json={"title": "Test Task", "description": "Descrição"})
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "pending"

def test_get_task(token):
    # Arrange & Act
    created = client.post("/tasks/", headers={"Authorization": f"Bearer {token}"}, json={"title": "Task Get"}).json()
    response = client.get(f"/tasks/{created['id']}", headers={"Authorization": f"Bearer {token}"})
    
    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]

def test_get_all_tasks(token):
    # Arrange
    client.post("/tasks/", headers={"Authorization": f"Bearer {token}"}, json={"title": "Task 1"})
    client.post("/tasks/", headers={"Authorization": f"Bearer {token}"}, json={"title": "Task 2"})
    
    # Act
    response = client.get("/tasks/", headers={"Authorization": f"Bearer {token}"})
    
    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_update_task_status(token):
    # Arrange & Act
    created = client.post("/tasks/", headers={"Authorization": f"Bearer {token}"}, json={"title": "Task Update"}).json()
    response = client.patch(f"/tasks/{created['id']}/status", headers={"Authorization": f"Bearer {token}"}, json={"status": "in_progress"})
    
    # Assert
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"

def test_get_task_not_found(token):
    # Act
    response = client.get("/tasks/9999", headers={"Authorization": f"Bearer {token}"})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Task with id 9999 not found."}
    
def test_delete_task(token):
    # Arrange 
    task_data = {
        "title": "Test Task for Delete",
        "description": "This is a test task for delete"
    }
    
    # Act
    create_response = client.post("/tasks/", headers={"Authorization": f"Bearer {token}"}, json=task_data)
    
    # Assert
    assert create_response.status_code == 201
    created_task = create_response.json()
    
    task_id = created_task["id"]
    
    #Act
    delete_response = client.delete(f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"}   )
    
    # Assert
    assert delete_response.status_code == 200
    
    data = delete_response.json()
    assert data["message"] == "Task deleted successfully"