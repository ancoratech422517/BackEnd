# Usa imagem oficial Python leve
FROM python:3.12-slim

# Define diretório de trabalho
WORKDIR /app

# Copia tudo de uma vez (mais confiável)
COPY . .

# Instala dependências + gunicorn
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Boa prática: rodar como usuário não-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Porta
EXPOSE ${PORT:-5000}

# Comando final
CMD gunicorn --workers 1 \
             --bind 0.0.0.0:${PORT:-5000} \
             --timeout 120 \
             app:app
