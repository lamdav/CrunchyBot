FROM python:3.7-alpine

LABEL "com.github.actions.name"="black"
LABEL "com.github.actions.description"="black python formatting check"
LABEL "com.github.actions.icon"="file-text"
LABEL "com.github.actions.color"="black"

RUN apk add --no-cache \
  bash \
  git

RUN pip install --upgrade pip
RUN pip install --upgrade black==19.10b0

RUN python --version
RUN pip --version

COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
