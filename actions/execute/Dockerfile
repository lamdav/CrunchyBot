FROM python:3.7-alpine

LABEL "com.github.actions.name"="execute"
LABEL "com.github.actions.description"="execute crunchy_bot"
LABEL "com.github.actions.icon"="play-circle"
LABEL "com.github.actions.color"="yellow"

RUN apk add --no-cache bash
RUN pip install --upgrade pip
RUN pip install crunchy_bot
RUN python --version
RUN pip --version
RUN crunchy version

COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
