# Usa imagem oficial Python leve
FROM python:3.12-slim

# Define diretório de trabalho
WORKDIR /app

# Copia requirements primeiro (melhor cache do Docker)
COPY backend/requirements.txt .

# Instala dependências + gunicorn explicitamente
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copia o resto do código
COPY . .

# Boa prática: rodar como usuário não-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Porta (Render, Railway, Fly.io, etc. usam variável $PORT)
EXPOSE ${PORT:-5000}

# Comando final - usando worker sync (mais estável para iniciantes)
CMD gunicorn --workers 1 \
             --bind 0.0.0.0:${PORT:-5000} \
             --timeout 120 \
             app:app
