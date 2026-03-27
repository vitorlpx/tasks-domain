import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.db.database import Base, get_db

# banco isolado para testes
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# --- testes ---

def test_health_check():
    # Arrage & Act
    response = client.get("/health")
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_task():
    # Arrange & Act
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Descrição"})
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "pending"

def test_get_task():
    # Arrange & Act
    created = client.post("/tasks/", json={"title": "Task Get"}).json()
    response = client.get(f"/tasks/{created['id']}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]

def test_get_all_tasks():
    # Arrange
    client.post("/tasks/", json={"title": "Task 1"})
    client.post("/tasks/", json={"title": "Task 2"})
    
    # Act
    response = client.get("/tasks/")
    
    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_update_task_status():
    # Arrange & Act
    created = client.post("/tasks/", json={"title": "Task Update"}).json()
    response = client.patch(f"/tasks/{created['id']}/status", json={"status": "in_progress"})
    
    # Assert
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"

def test_get_task_not_found():
    # Act
    response = client.get("/tasks/9999")
    
    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Tarefa não encontrada."}
    
def test_delete_task():
    # Arrange 
    task_data = {
        "title": "Test Task for Delete",
        "description": "This is a test task for delete"
    }
    
    # Act
    create_response = client.post("/tasks/", json=task_data)
    
    # Assert
    assert create_response.status_code == 201
    created_task = create_response.json()
    
    task_id = created_task["id"]
    
    #Act
    delete_response = client.delete(f"/tasks/{task_id}")
    
    # Assert
    assert delete_response.status_code == 200
    
    data = delete_response.json()
    assert data["message"] == "Task deleted successfully"