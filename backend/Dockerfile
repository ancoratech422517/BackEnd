FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN ls -la

RUN pip install --no-cache-dir -r requirements.txt gunicorn gevent

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE ${PORT:-5000}

CMD ["sh", "-c", "echo '=== INICIANDO DEBUG ===' && echo \"PORT = ${PORT}\" && python -c 'from gevent import monkey; monkey.patch_all(); print(\"[OK] Monkey patch\"); import os; print(\"[OK] PORT:\", os.getenv(\"PORT\")); import app; print(\"[OK] app.py importado\"); print(\"[OK] App:\", getattr(app, \"app\", None))' && echo '=== INICIANDO GUNICORN ===' && gunicorn --workers 2 --worker-class gevent --bind 0.0.0.0:${PORT:-5000} --timeout 180 --log-level info app:app"]
