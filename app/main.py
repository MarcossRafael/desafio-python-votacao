from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy import select

from app.database import init_db, SessionLocal
from app.models import Candidato
from app.routes import candidatos, votos, resultados

CANDIDATOS_INICIAIS = [
    {"id": 1, "nome": "Maria Silva", "numero": 13},
    {"id": 2, "nome": "João Souza", "numero": 45},
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await init_db()
    async with SessionLocal() as db:
        for dados in CANDIDATOS_INICIAIS:
            existente = await db.get(Candidato, dados["id"])
            if not existente:
                db.add(Candidato(**dados))
        await db.commit()
    yield


app = FastAPI(
    title="API de Votação",
    description="API para coleta e consulta de intenções de voto",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(candidatos.router)
app.include_router(votos.router)
app.include_router(resultados.router)
