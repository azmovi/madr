# Madr
Projeto inspirado no curso de fastAPI do @dunossauro
[Link para acessar a ideia](https://fastapidozero.dunossauro.com/estavel/15/) 


- O objetivo do projeto é criarmos um gerenciador de livros e relacionar com seus autores.

### Sobre as partes do projeto

#### Backend
##### Tecnologia
- python
- fastapi
- sqlalchemy
- alembic

- Usando o uv
```bash
uv sync
```
```bash
source /venv/bin/activate
```

- Usando venv normal
```bash
python -m venv venv
```
```bash
pip install .
```
```bash
source /venv/bin/activate
```

- Rodando o backend
```bash
task run
```

#### Banco de dados
##### Tecnologia
- Postgres

> Muito trampo setar o postgres localmente sendo que eu não faço nenhuma mudança
nele porque eu uso o sistema de migrações usando o alembic


#### Frontend
##### Tecnologia
- vue


##### Rodando localmente
```bash
npm install
```
```bash
npm run dev
```

### Rodar o projeto via compose
```bash
docker compose up
```
