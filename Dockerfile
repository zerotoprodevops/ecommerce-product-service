FROM python:3.11-slim

RUN apt-get  update && \
    apt-get upgrade -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY .  .

RUN pip install --no-cache-dir -r requirements.txt 

EXPOSE 5000

ENTRYPOINT ["python3", "app.py"]