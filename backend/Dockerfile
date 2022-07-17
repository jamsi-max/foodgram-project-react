FROM python:3.7-alpine3.7
LABEL maintainer="foodgram"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY backend/requirements.txt /requirements.txt
COPY ./backend  /backend
COPY backend//scripts /scripts
COPY backend/data_for_db/ingredients.csv /ingredients.csv

WORKDIR /backend
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install --upgrade setuptools && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    apk add zlib-dev jpeg-dev gcc libc-dev libffi-dev && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser -D -H backend && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R backend:backend /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER backend

CMD ["run.sh"]