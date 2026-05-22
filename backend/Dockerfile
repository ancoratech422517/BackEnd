FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt gunicorn eventlet

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE ${PORT:-5000}

CMD ["sh", "-c", "
    echo '=== INICIANDO SERVIDOR ===' && 
    echo \"PORT recebido = ${PORT:-5000}\" && 
    exec gunicorn \
        --worker-class eventlet \
        --workers 1 \
        --bind 0.0.0.0:${PORT:-5000} \
        --timeout 180 \
        --keep-alive 60 \
        --log-level info \
        app:app
"]
