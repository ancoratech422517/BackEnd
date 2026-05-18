FROM python:3.10-slim

WORKDIR /app

# Copia o requirements garantindo que ele apanha o arquivo correto
COPY requirements*.txt ./

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto dos arquivos do backend
COPY . .

EXPOSE 5000

# Comando de inicialização usando a porta dinâmica da Railway
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
