FROM python:3.7-alpine

RUN apk add --no-cache \
  bash \
  chromium-chromedriver \
  chromium

RUN pip install --upgrade pip
RUN pip install --upgrade crunchy-bot

RUN python --version
RUN pip --version
RUN crunchy version

COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
