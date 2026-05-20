FROM python:3.12-slim

WORKDIR /app

# Instala dependências do sistema necessárias para compilar pacotes (como psycopg2 se precisar)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 1. Como o Root Directory no Render já é 'backend', copiamos direto da raiz atual
COPY requirements.txt /app/

# 2. Instala as dependências do projeto e os workers do Gevent para o SocketIO
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gevent gevent-websocket gunicorn

# 3. Copia todos os arquivos da pasta atual do projeto para dentro do container
COPY . /app/

EXPOSE 5000

# 4. Comando de inicialização oficial para Flask + SocketIO no Render
CMD ["gunicorn", "--worker-class", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
