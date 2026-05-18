FROM python:3.12-slim

WORKDIR /app

# 1. Copia o arquivo da pasta atual configurada na Railway
COPY backend/requirements.txt ./

# 2. Instala as dependências de forma limpa
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gevent gevent-websocket gunicorn

# 3. Copia o resto dos arquivos
COPY backend

EXPOSE 5000

# 4. Comando de inicialização usando o worker do gevent correspondente ao Flask-SocketIO
CMD ["gunicorn", "--worker-class", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
