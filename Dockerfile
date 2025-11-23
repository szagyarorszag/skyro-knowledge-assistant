FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src/ ./src/
COPY skyro_dataset/ ./skyro_dataset/
COPY skyro-logo.svg .
COPY docker-entrypoint.sh .

RUN chmod +x docker-entrypoint.sh
RUN mkdir -p chroma_db

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["./docker-entrypoint.sh"]

