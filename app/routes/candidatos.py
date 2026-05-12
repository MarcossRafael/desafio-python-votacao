from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Candidato
from app.schemas import CandidatoOut

router = APIRouter(prefix="/candidatos", tags=["Candidatos"])


@router.get("", response_model=list[CandidatoOut])
async def listar_candidatos(db: AsyncSession = Depends(get_db)) -> list[CandidatoOut]:
    result = await db.execute(select(Candidato))
    return result.scalars().all()
