FROM python:3.13.2-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependencias Python primeiro para aproveitar cache de build
COPY app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt

# Copia somente os arquivos da aplicacao necessarios para execucao
COPY app/src ./src
COPY app/settings.py ./settings.py

# Etapa de runtime (seguindo o padrão multi-stage build)
FROM python:3.13.2-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

WORKDIR /app

# Copia os pacotes instalados no builder (inclui uvicorn e demais deps)
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app/src ./src
COPY --from=builder /app/settings.py ./settings.py

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]