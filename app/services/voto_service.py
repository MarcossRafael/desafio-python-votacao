from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models import Candidato, Voto
from app.schemas import VotoIn, ResultadoOut, ResultadoCandidato


async def registrar_voto(db: AsyncSession, dados: VotoIn) -> None:
    candidato = await db.get(Candidato, dados.candidato_id)
    if not candidato:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Candidato não encontrado")

    voto = Voto(cpf=dados.cpf, candidato_id=dados.candidato_id)
    db.add(voto)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CPF já votou")


async def obter_resultados(db: AsyncSession) -> ResultadoOut:
    candidatos_result = await db.execute(select(Candidato))
    candidatos = candidatos_result.scalars().all()

    total_result = await db.execute(select(func.count()).select_from(Voto))
    total_votos: int = total_result.scalar() or 0

    resultado_candidatos: list[ResultadoCandidato] = []
    for candidato in candidatos:
        votos_result = await db.execute(
            select(func.count()).select_from(Voto).where(Voto.candidato_id == candidato.id)
        )
        total_candidato: int = votos_result.scalar() or 0
        percentual = round((total_candidato / total_votos * 100), 2) if total_votos > 0 else 0.0

        resultado_candidatos.append(
            ResultadoCandidato(
                candidato_id=candidato.id,
                nome=candidato.nome,
                numero=candidato.numero,
                total_votos=total_candidato,
                percentual=percentual,
            )
        )

    return ResultadoOut(total_votos=total_votos, candidatos=resultado_candidatos)
