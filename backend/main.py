from fastapi import FastAPI, HTTPException, Depends, Security, Query
from pydantic import BaseModel, Field, EmailStr, constr
from typing import List, Optional
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Any
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_openapi_description
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_openapi_description
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi import Query

app = FastAPI()

# Database simulation
fake_db = {
    "responsaveis": [],
    "animais": [],
    "veterinarios": [],
    "consultas": [],
    "atendimentos": [],
    "medicacoes": []
}

# Models
class Responsavel(BaseModel):
    id: int
    nome: constr(min_length=3, max_length=50)
    cpf: constr(regex="^\d{11}$", description="CPF deve conter 11 dígitos.")
    telefone: constr(regex="^\(\d{2}\) \d{4,5}-\d{4}$", description="Formato esperado: (XX) XXXXX-XXXX")
    email: EmailStr
    endereco: constr(min_length=5, max_length=100)

class Animal(BaseModel):
    id: int
    nome: constr(min_length=2, max_length=30)
    especie: constr(min_length=3, max_length=20)
    raca: constr(min_length=3, max_length=30)
    sexo: constr(regex="^(Macho|Fêmea)$", description="Deve ser 'Macho' ou 'Fêmea'")
    data_nascimento: datetime
    responsavel_id: int

class Veterinario(BaseModel):
    id: int
    nome: constr(min_length=3, max_length=50)
    crmv: constr(min_length=5, max_length=10, description="CRMV deve ser único e válido.")
    especialidade: constr(min_length=3, max_length=50)
    contato: constr(regex="^\(\d{2}\) \d{4,5}-\d{4}$")

class Consulta(BaseModel):
    id: int
    animal_id: int
    veterinario_id: int
    data: datetime
    horario: str
    tipo_atendimento: str

class Atendimento(BaseModel):
    id: int
    consulta_id: int
    observacoes: Optional[str]
    diagnostico: Optional[str]

class Medicacao(BaseModel):
    id: int
    atendimento_id: int
    nome: str
    dosagem: str
    frequencia: str
    forma: str
    observacoes: Optional[str]

# Security settings
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Adding user roles and permissions
roles = {"admin": ["manage_users", "manage_vets"], "vet": ["view_schedule", "write_prescriptions"], "reception": ["schedule_appointments"]}

# Routes
@app.post("/responsaveis/")
def create_responsavel(responsavel: Responsavel):
    if any(r["cpf"] == responsavel.cpf for r in fake_db["responsaveis"]):
        raise HTTPException(status_code=400, detail="CPF já cadastrado.")
    fake_db["responsaveis"].append(responsavel.dict())
    return {"message": "Responsável cadastrado com sucesso!"}

@app.get("/responsaveis/", response_model=List[Responsavel])
def list_responsaveis(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)):
    return fake_db["responsaveis"][skip: skip + limit]

@app.post("/animais/")
def create_animal(animal: Animal):
    if not any(r["id"] == animal.responsavel_id for r in fake_db["responsaveis"]):
        raise HTTPException(status_code=404, detail="Responsável não encontrado.")
    fake_db["animais"].append(animal.dict())
    return {"message": "Animal cadastrado com sucesso!"}

@app.get("/animais/", response_model=List[Animal])
def list_animais(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), especie: Optional[str] = None):
    animais = fake_db["animais"]
    if especie:
        animais = [animal for animal in animais if animal["especie"] == especie]
    return animais[skip: skip + limit]

@app.post("/veterinarios/")
def create_veterinario(veterinario: Veterinario):
    if any(v["crmv"] == veterinario.crmv for v in fake_db["veterinarios"]):
        raise HTTPException(status_code=400, detail="CRMV já cadastrado.")
    fake_db["veterinarios"].append(veterinario.dict())
    return {"message": "Veterinário cadastrado com sucesso!"}

@app.get("/veterinarios/", response_model=List[Veterinario])
def list_veterinarios(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), especialidade: Optional[str] = None):
    veterinarios = fake_db["veterinarios"]
    if especialidade:
        veterinarios = [vet for vet in veterinarios if vet["especialidade"] == especialidade]
    return veterinarios[skip: skip + limit]

@app.post("/consultas/")
def create_consulta(consulta: Consulta):
    # Check for scheduling conflicts
    for existing_consulta in fake_db["consultas"]:
        if (existing_consulta["veterinario_id"] == consulta.veterinario_id and
            existing_consulta["data"] == consulta.data and
            existing_consulta["horario"] == consulta.horario):
            raise HTTPException(status_code=400, detail="Conflito de horário para o veterinário.")

    fake_db["consultas"].append(consulta.dict())
    return {"message": "Consulta agendada com sucesso!"}

@app.get("/consultas/", response_model=List[Consulta])
def list_consultas():
    return fake_db["consultas"]

@app.post("/atendimentos/")
def create_atendimento(atendimento: Atendimento):
    # Ensure the consultation exists
    if not any(consulta["id"] == atendimento.consulta_id for consulta in fake_db["consultas"]):
        raise HTTPException(status_code=404, detail="Consulta não encontrada.")

    fake_db["atendimentos"].append(atendimento.dict())
    return {"message": "Atendimento registrado com sucesso!"}

@app.get("/atendimentos/", response_model=List[Atendimento])
def list_atendimentos():
    return fake_db["atendimentos"]

@app.post("/medicacoes/")
def create_medicacao(medicacao: Medicacao):
    # Ensure the attendance exists
    if not any(atendimento["id"] == medicacao.atendimento_id for atendimento in fake_db["atendimentos"]):
        raise HTTPException(status_code=404, detail="Atendimento não encontrado.")

    fake_db["medicacoes"].append(medicacao.dict())
    return {"message": "Medicação registrada com sucesso!"}

@app.get("/medicacoes/", response_model=List[Medicacao])
def list_medicacoes():
    return fake_db["medicacoes"]

# User authentication
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_db["users"], form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(users, username: str, password: str):
    user = next((u for u in users if u["username"] == username), None)
    if user and verify_password(password, user["hashed_password"]):
        return user
    return None

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "roles": roles.get(username, [])}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/roles/{role}")
def get_role_permissions(role: str):
    return {"role": role, "permissions": roles.get(role, [])}

# Adding client, animal, and veterinarian management modules

@app.put("/responsaveis/{responsavel_id}")
def update_responsavel(responsavel_id: int, updated_responsavel: Responsavel):
    for index, responsavel in enumerate(fake_db["responsaveis"]):
        if responsavel["id"] == responsavel_id:
            fake_db["responsaveis"][index] = updated_responsavel.dict()
            return {"message": "Responsável atualizado com sucesso!"}
    raise HTTPException(status_code=404, detail="Responsável não encontrado.")

@app.delete("/responsaveis/{responsavel_id}")
def delete_responsavel(responsavel_id: int):
    for responsavel in fake_db["responsaveis"]:
        if responsavel["id"] == responsavel_id:
            if any(animal["responsavel_id"] == responsavel_id for animal in fake_db["animais"]):
                raise HTTPException(status_code=400, detail="Não é possível remover um responsável com animais ativos.")
            fake_db["responsaveis"].remove(responsavel)
            return {"message": "Responsável removido com sucesso!"}
    raise HTTPException(status_code=404, detail="Responsável não encontrado.")

@app.put("/animais/{animal_id}")
def update_animal(animal_id: int, updated_animal: Animal):
    for index, animal in enumerate(fake_db["animais"]):
        if animal["id"] == animal_id:
            fake_db["animais"][index] = updated_animal.dict()
            return {"message": "Animal atualizado com sucesso!"}
    raise HTTPException(status_code=404, detail="Animal não encontrado.")

@app.delete("/animais/{animal_id}")
def delete_animal(animal_id: int):
    for animal in fake_db["animais"]:
        if animal["id"] == animal_id:
            fake_db["animais"].remove(animal)
            return {"message": "Animal removido com sucesso!"}
    raise HTTPException(status_code=404, detail="Animal não encontrado.")

@app.put("/veterinarios/{veterinario_id}")
def update_veterinario(veterinario_id: int, updated_veterinario: Veterinario):
    for index, veterinario in enumerate(fake_db["veterinarios"]):
        if veterinario["id"] == veterinario_id:
            fake_db["veterinarios"][index] = updated_veterinario.dict()
            return {"message": "Veterinário atualizado com sucesso!"}
    raise HTTPException(status_code=404, detail="Veterinário não encontrado.")

@app.delete("/veterinarios/{veterinario_id}")
def delete_veterinario(veterinario_id: int):
    for veterinario in fake_db["veterinarios"]:
        if veterinario["id"] == veterinario_id:
            fake_db["veterinarios"].remove(veterinario)
            return {"message": "Veterinário removido com sucesso!"}
    raise HTTPException(status_code=404, detail="Veterinário não encontrado.")

# Adding public agenda view
@app.get("/agenda/")
def public_agenda():
    agenda = []
    for consulta in fake_db["consultas"]:
        animal = next((a for a in fake_db["animais"] if a["id"] == consulta["animal_id"]), None)
        if animal:
            agenda.append({
                "horario": consulta["horario"],
                "nome_animal": animal["nome"],
                "tipo_atendimento": consulta["tipo_atendimento"]
            })
    return agenda

# Adding security measures
from fastapi.middleware.cors import CORSMiddleware

# Enable CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# SQL Injection protection is handled by using parameterized queries in the database layer (not implemented in this mock database).

# Adding logging and monitoring
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response