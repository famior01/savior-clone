FROM python:3.10-bullseye


COPY . /app
WORKDIR /app

RUN python3 -m venv /opt/venv


RUN /opt/venv/bin/pip install --upgrade pip && \
    apt-get update && apt-get install libgl1 -y && \
    /opt/venv/bin/pip install -r requirements.txt --timeout 1000 && \
    chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]