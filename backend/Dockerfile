FROM python:3.10-slim

WORKDIR /app

# 1. Copia o requirements especificando a pasta exata do teu projeto
COPY backend/requirements.txt ./

# 2. Instala as dependências encontradas no arquivo
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copia todo o conteúdo da pasta backend para dentro do diretório de trabalho
COPY backend/ .

EXPOSE 5000

# 4. Comando de inicialização
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
