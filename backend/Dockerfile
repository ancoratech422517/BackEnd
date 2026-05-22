FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN ls -la

RUN pip install --no-cache-dir -r requirements.txt gunicorn gevent

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE ${PORT:-5000}

CMD ["sh", "-c", "
    echo '=== INICIANDO APLICAÇÃO ===' &&
    echo \"PORT = \${PORT}\" &&
    python -c '
from gevent import monkey
monkey.patch_all()
import os
print(\"=== MONKEY PATCH APLICADO ===\")
print(\"PORTA:\", os.getenv(\"PORT\"))
import app
print(\"=== APP IMPORTADO COM SUCESSO ===\")
print(\"App object:\", app.app)
    ' &&
    gunicorn --workers 2 --worker-class gevent --bind 0.0.0.0:\${PORT:-5000} --timeout 180 --log-level info app:app
"]
