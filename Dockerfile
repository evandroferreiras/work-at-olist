FROM python:3.7.0-alpine3.8
ADD ./requirements/common.txt /etc
ADD ./requirements/prod.txt /etc
RUN apk update && \
    apk add postgresql-libs && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install -r /etc/prod.txt --no-cache-dir && \
    apk --purge del .build-deps
ADD . /
WORKDIR /
ENTRYPOINT [ "gunicorn", "-c", "../gunicorn.py", "app:app"]
EXPOSE 5000
