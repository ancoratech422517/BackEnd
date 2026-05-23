FROM python:3.12-slim

WORKDIR /app

# Copia requirements primeiro para melhor cache
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt gunicorn eventlet

# Copia o resto do código
COPY . .

# Cria usuário não-root por segurança
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE ${PORT:-5000}

CMD ["sh", "-c", "
    echo '=== INICIANDO SERVIDOR ===' &&
    echo \"PORT = ${PORT:-5000}\" &&
    exec gunicorn \
        --worker-class eventlet \
        --workers 1 \
        --bind 0.0.0.0:${PORT:-5000} \
        --timeout 300 \
        --keep-alive 60 \
        --log-level info \
        --access-logfile - \
        --error-logfile - \
        app:app
"]
