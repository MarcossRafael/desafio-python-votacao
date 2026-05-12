from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Candidato(Base):
    __tablename__ = "candidatos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    numero: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)

    votos: Mapped[list["Voto"]] = relationship("Voto", back_populates="candidato")


class Voto(Base):
    __tablename__ = "votos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True, index=True)
    candidato_id: Mapped[int] = mapped_column(ForeignKey("candidatos.id"), nullable=False)

    candidato: Mapped["Candidato"] = relationship("Candidato", back_populates="votos")
