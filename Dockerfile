# vim:set ft=dockerfile ts=1 sw=1 ai et:
FROM python:2

RUN pip install --no-cache-dir gunicorn

COPY . /srv/collar-client
RUN pip install --no-cache-dir -e /srv/docker-collar/

CMD ["gunicorn", "--workers=5", "--bind=127.0.0.1:80", "docker_collar.collar_client:app"]
