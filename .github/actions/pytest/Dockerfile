FROM python:3.7-alpine

RUN apk add --no-cache \
  bash \
  git
RUN pip install --upgrade pip pytest

RUN python --version
RUN pip --version
RUN pytest --version

COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
