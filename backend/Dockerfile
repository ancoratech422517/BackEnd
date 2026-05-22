# Usa imagem oficial Python leve
FROM python:3.12-slim

WORKDIR /app

# Copia tudo
COPY . .

# === DIAGNÓSTICO: Mostra os ficheiros que foram copiados ===
RUN ls -la

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Boa prática: usuário não-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE ${PORT:-5000}

CMD gunicorn --workers 1 \
             --bind 0.0.0.0:${PORT:-5000} \
             --timeout 120 \
             app:app
