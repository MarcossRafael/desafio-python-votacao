import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.database import Base, get_db
from app.models import Candidato

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_votacao.db"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSession = async_sessionmaker(test_engine, expire_on_commit=False)


async def override_get_db() -> AsyncSession:
    async with TestSession() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestSession() as db:
        db.add(Candidato(id=1, nome="Maria Silva", numero=13))
        db.add(Candidato(id=2, nome="João Souza", numero=45))
        await db.commit()
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def client():
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.mark.asyncio
async def test_listar_candidatos(client):
    async with client as c:
        response = await c.get("/candidatos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["nome"] == "Maria Silva"
    assert data[1]["nome"] == "João Souza"


@pytest.mark.asyncio
async def test_registrar_voto_sucesso(client):
    async with client as c:
        response = await c.post("/votos", json={"cpf": "12345678901", "candidato_id": 1})
    assert response.status_code == 201
    assert response.json()["mensagem"] == "Voto registrado com sucesso"


@pytest.mark.asyncio
async def test_voto_cpf_duplicado(client):
    async with client as c:
        await c.post("/votos", json={"cpf": "12345678901", "candidato_id": 1})
        response = await c.post("/votos", json={"cpf": "12345678901", "candidato_id": 2})
    assert response.status_code == 409
    assert "já votou" in response.json()["detail"]


@pytest.mark.asyncio
async def test_voto_cpf_invalido(client):
    async with client as c:
        response = await c.post("/votos", json={"cpf": "123", "candidato_id": 1})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_voto_candidato_inexistente(client):
    async with client as c:
        response = await c.post("/votos", json={"cpf": "12345678901", "candidato_id": 99})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_resultados_sem_votos(client):
    async with client as c:
        response = await c.get("/resultados")
    assert response.status_code == 200
    data = response.json()
    assert data["total_votos"] == 0
    assert all(c["percentual"] == 0.0 for c in data["candidatos"])


@pytest.mark.asyncio
async def test_resultados_com_votos(client):
    async with client as c:
        await c.post("/votos", json={"cpf": "11111111111", "candidato_id": 1})
        await c.post("/votos", json={"cpf": "22222222222", "candidato_id": 1})
        await c.post("/votos", json={"cpf": "33333333333", "candidato_id": 2})
        response = await c.get("/resultados")
    assert response.status_code == 200
    data = response.json()
    assert data["total_votos"] == 3
    maria = next(c for c in data["candidatos"] if c["nome"] == "Maria Silva")
    assert maria["total_votos"] == 2
    assert maria["percentual"] == 66.67
