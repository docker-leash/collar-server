# vim:set ft=dockerfile ts=1 sw=1 ai et:
FROM python:2-slim

RUN pip install --no-cache-dir gunicorn

COPY . /srv/docker-collar
RUN pip install --no-cache-dir -e /srv/docker-collar/

CMD ["gunicorn", "--workers=5", "--bind=unix:/run/docker/plugins/collar.sock", "docker_collar.collar_client:app"]
