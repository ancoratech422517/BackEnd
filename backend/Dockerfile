# 1. Usa uma imagem oficial do Python leve
FROM python:3.12-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Copia o arquivo de dependências primeiro (otimiza o cache do Docker)
COPY backend/requirements.txt .

# 4. Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia o restante do código do projeto para dentro do container
COPY . .

# 7. Comando para rodar a aplicação usando o motor padrão do Gunicorn.
# Removido o '--worker-class eventlet' para evitar o erro de falta de pacote.
CMD gunicorn -w 1 -b 0.0.0.0:${PORT:-5000} app:app
