# Desafio Python - Marcos Rafael do Nascimento Faria

Esse projeto é uma API de intenções de voto que desenvolvi como parte de um desafio técnico. A ideia é simular o backend de uma pesquisa eleitoral, onde pessoas podem registrar seu voto e consultar os resultados em tempo real.

A API foi construída com **FastAPI** e **SQLite**, usando operações assíncronas do início ao fim.

---

## O que você vai precisar

- Python 3.10 ou superior
- Poetry (gerenciador de dependências)

---

## Como rodar o projeto

**1. Clone o repositório**
```bash
git clone https://github.com/MarcossRafael/desafio-python-votacao.git
cd desafio-python-votacao
```

**2. Instale as dependências com Poetry**
```bash
poetry install
```

O Poetry já cria e gerencia o ambiente virtual automaticamente. Não precisa criar venv manualmente.

**3. Suba a API**
```bash
poetry run uvicorn app.main:app --reload
```

A API vai estar rodando em `http://localhost:8000`. Para testar de forma visual, acesse `http://localhost:8000/docs`, lá tem uma interface onde você consegue chamar cada endpoint direto pelo navegador.

---

## Endpoints

### `GET /candidatos`
Retorna a lista de candidatos disponíveis para votação.

```json
[
  { "id": 1, "nome": "Maria Silva", "numero": 13 },
  { "id": 2, "nome": "João Souza", "numero": 45 }
]
```

---

### `POST /votos`
Registra a intenção de voto de uma pessoa. Cada CPF só pode votar uma vez.

**O que enviar:**
```json
{
  "cpf": "12345678901",
  "candidato_id": 1
}
```

**Possíveis respostas:**
- `201` — Voto registrado com sucesso
- `400` — Candidato não encontrado
- `409` — Esse CPF já votou
- `422` — CPF inválido (precisa ter exatamente 11 dígitos numéricos)

---

### `GET /resultados`
Retorna o total de votos e o percentual de cada candidato.

```json
{
  "total_votos": 3,
  "candidatos": [
    { "candidato_id": 1, "nome": "Maria Silva", "numero": 13, "total_votos": 2, "percentual": 66.67 },
    { "candidato_id": 2, "nome": "João Souza", "numero": 45, "total_votos": 1, "percentual": 33.33 }
  ]
}
```

---

## Rodando os testes

```bash
poetry run pytest tests/ -v
```

São 7 testes que cobrem os principais cenários: voto com sucesso, CPF duplicado, CPF inválido, candidato inexistente e cálculo de percentuais.

---

## Rodando com Docker

Se preferir usar Docker em vez de configurar o ambiente local:

```bash
docker build -t votacao-api .
docker run -p 8000:8000 votacao-api
```

A API vai estar disponível no mesmo endereço: `http://localhost:8000`.
