FROM python:3.10-bullseye


COPY . /app
WORKDIR /app

RUN python -m venv /opt/venv

RUN /opt/venv/bin/pip install --upgrade pip && \
    apt-get update && apt-get install libgl1 -y --no-install-recommends apt-utils --fix-missing && \
    apt-get install redis-server -y && \
    /opt/venv/bin/pip install --use-pep517 -r requirements.txt  --timeout 4000 && \
    chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]
