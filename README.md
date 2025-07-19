# Madr
Projeto inspirado no curso de fastAPI do @dunossauro
[Link para acessar a ideia](https://fastapidozero.dunossauro.com/estavel/15/) 


- O objetivo do projeto é criarmos um gerenciador de livros e relacionar com seus autores.

### Rodando projeto com Minikube

sudo echo "$(minikube ip) madr.local" >> /etc/hosts

> Não consegui fazer funcionar o madr.local como url padrão no meu browser, entretanto passando com o hosts como visto na tela funciona corretamente
> No LE-6 fui capaz de rodar o minikube com a url mas aqui não sei o que rolou para não funcionar
<img width="957" height="742" alt="image" src="https://github.com/user-attachments/assets/fe1ea995-3f15-4e94-b555-dd81f8cca053" />


### Sobre as partes do projeto

#### Env de exemplo
```bash
# Database env
POSTGRES_USER=app_user
POSTGRES_DB=app_db
POSTGRES_PASSWORD=app_password
DATABASE_URL=postgresql+psycopg://app_user:app_password@mader_database:5432/app_db

# Security env
SECRET_KEY=supersegredosecreto123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
- sqlalchemy
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

