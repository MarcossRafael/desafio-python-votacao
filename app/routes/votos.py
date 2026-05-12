from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import VotoIn, VotoOut
from app.services.voto_service import registrar_voto

router = APIRouter(prefix="/votos", tags=["Votos"])


@router.post("", response_model=VotoOut, status_code=status.HTTP_201_CREATED)
async def votar(dados: VotoIn, db: AsyncSession = Depends(get_db)) -> VotoOut:
    await registrar_voto(db, dados)
    return VotoOut(mensagem="Voto registrado com sucesso")
