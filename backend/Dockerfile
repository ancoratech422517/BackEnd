FROM python:3.12-slim

WORKDIR /app

# 1. Copia o arquivo requirements usando aspas para evitar erros de sintaxe
COPY ["backend/requirements.txt", "/app/"]

# 2. Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gevent gevent-websocket gunicorn

# 3. Copia todo o resto do código para a pasta /app
COPY ["backend", "/app/"]

EXPOSE 5000

# 4. Comando de inicialização com o Gevent Worker
CMD ["gunicorn", "--worker-class", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
