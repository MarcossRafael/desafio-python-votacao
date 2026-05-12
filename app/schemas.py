from pydantic import BaseModel, field_validator


class CandidatoOut(BaseModel):
    id: int
    nome: str
    numero: int

    model_config = {"from_attributes": True}


class VotoIn(BaseModel):
    cpf: str
    candidato_id: int

    @field_validator("cpf")
    @classmethod
    def validar_cpf(cls, v: str) -> str:
        v = v.strip()
        if not v.isdigit() or len(v) != 11:
            raise ValueError("CPF deve conter exatamente 11 dígitos numéricos")
        return v


class VotoOut(BaseModel):
    mensagem: str


class ResultadoCandidato(BaseModel):
    candidato_id: int
    nome: str
    numero: int
    total_votos: int
    percentual: float


class ResultadoOut(BaseModel):
    total_votos: int
    candidatos: list[ResultadoCandidato]
