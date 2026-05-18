FROM python:3.12-slim

WORKDIR /app

# 1. Copia o requirements especificando a pasta exata do teu projeto
COPY BackEnd/backend/requirements.txt ./

# 2. Instala as dependências encontradas no arquivo
RUN pip install --no-cache-dir -r requirements.txt

# 3. Garante a instalação correta do eventlet e gunicorn juntos
RUN pip install --no-cache-dir eventlet gunicorn

# 4. Copia todo o conteúdo da pasta backend para dentro do diretório de trabalho
COPY BackEnd/backend/ .

EXPOSE 5000

# 5. Comando de inicialização definitivo para WebSocket
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
