FROM python:3.10-bullseye
ENV PYTHONUNBUFFERED 1
ENV TF_CPP_MIN_LOG_LEVEL 3


COPY . /app
WORKDIR /app

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    apt-get update && apt-get install libgl1 -y --no-install-recommends --fix-missing && \
    apt-get install redis-server -y && \
    /opt/venv/bin/pip install --use-pep517 -r requirements.txt  --timeout 4000 && \
    chmod +x entrypoint.sh 

CMD ["/app/entrypoint.sh"]
