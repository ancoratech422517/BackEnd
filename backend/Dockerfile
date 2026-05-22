FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt gunicorn gevent

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE ${PORT:-5000}

# CMD corrigido para respeitar o $PORT do Railway
CMD ["sh", "-c", "echo '=== INICIANDO GUNICORN NO PORT ${PORT} ===' && gunicorn --workers 2 --worker-class gevent --bind 0.0.0.0:${PORT:-5000} --timeout 180 --log-level info app:app"]
