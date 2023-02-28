FROM python:3.10-bullseye
ENV PYTHONUNBUFFERED 1
ENV TF_CPP_MIN_LOG_LEVEL 1


COPY . /app
WORKDIR /app

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        redis-server && \
    apt-get install -y --no-install-recommends \
        dialog \
        apt-utils \
        libnvinfer-dev \
        libnvinfer-plugin-dev \
        libnvparsers-dev \
        libnvonnxparsers-dev && \
    /opt/venv/bin/pip install --use-feature=2020-resolver --timeout 4000 -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    chmod +x entrypoint.sh 
    

CMD ["/app/entrypoint.sh"]
