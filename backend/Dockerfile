FROM python:3.12-slim

WORKDIR /app

COPY . .

# Debug
RUN ls -la

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Usuário não-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE ${PORT:-5000}

# CMD mais explícito e seguro (sem gevent por agora)
CMD ["sh", "-c", "gunicorn --workers 1 --worker-class sync --bind 0.0.0.0:${PORT:-5000} --timeout 120 --log-level debug app:app"]
