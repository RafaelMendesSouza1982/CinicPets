import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test for Responsaveis
@pytest.fixture
def responsavel_data():
    return {
        "id": 1,
        "nome": "João Silva",
        "cpf": "12345678901",
        "telefone": "(11) 98765-4321",
        "email": "joao.silva@example.com",
        "endereco": "Rua das Flores, 123"
    }

def test_create_responsavel(responsavel_data):
    response = client.post("/responsaveis/", json=responsavel_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Responsável cadastrado com sucesso!"

def test_list_responsaveis():
    response = client.get("/responsaveis/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)