FROM python:3.12.8

RUN apt-get update && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/*RUN  pip install pandas sqlalchemy psycopg2 requests  

RUN pip install --no-cache-dir --default-timeout=100 pandas sqlalchemy psycopg2 requests

WORKDIR /app

COPY ingest_data.py ingest_data.py

ENTRYPOINT ["bash"]