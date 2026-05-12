# Desafio Python - API de Votação

API REST assíncrona para coleta e consulta de intenções de voto, construída com FastAPI e SQLite.

## Tecnologias

- Python 3.10+
- FastAPI
- SQLAlchemy (async) + aiosqlite
- Pytest

## Instalação

```bash
# Clonar o repositório
git clone https://github.com/MarcossRafael/desafio-python-votacao.git
cd desafio-python-votacao

# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Rodar a API
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.  
Documentação interativa: `http://localhost:8000/docs`

## Endpoints

### `GET /candidatos`
Retorna a lista de candidatos disponíveis.

```json
[
  { "id": 1, "nome": "Maria Silva", "numero": 13 },
  { "id": 2, "nome": "João Souza", "numero": 45 }
]
```

### `POST /votos`
Registra uma intenção de voto.

**Body:**
```json
{
  "cpf": "12345678901",
  "candidato_id": 1
}
```

**Respostas:**
- `201` — Voto registrado com sucesso
- `400` — Candidato não encontrado
- `409` — CPF já votou
- `422` — CPF inválido (deve ter 11 dígitos numéricos)

### `GET /resultados`
Retorna a totalização dos votos com percentuais.

```json
{
  "total_votos": 3,
  "candidatos": [
    { "candidato_id": 1, "nome": "Maria Silva", "numero": 13, "total_votos": 2, "percentual": 66.67 },
    { "candidato_id": 2, "nome": "João Souza", "numero": 45, "total_votos": 1, "percentual": 33.33 }
  ]
}
```

## Testes

```bash
pytest tests/ -v
```

## Docker

```bash
docker build -t votacao-api .
docker run -p 8000:8000 votacao-api
```
