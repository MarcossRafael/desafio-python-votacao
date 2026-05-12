from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import ResultadoOut
from app.services.voto_service import obter_resultados

router = APIRouter(prefix="/resultados", tags=["Resultados"])


@router.get("", response_model=ResultadoOut)
async def resultados(db: AsyncSession = Depends(get_db)) -> ResultadoOut:
    return await obter_resultados(db)
