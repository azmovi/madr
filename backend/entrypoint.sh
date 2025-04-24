#!/bin/sh

# Executa as migrações do banco de dados
alembic upgrade head

# Inicia a aplicação
fastapi dev --host 0.0.0.0 mader/app.py
