FROM python:3.7-alpine

LABEL "com.github.actions.name"="pytest"
LABEL "com.github.actions.description"="execute pytest"
LABEL "com.github.actions.icon"="upload-cloud"
LABEL "com.github.actions.color"="yellow"

RUN apk add --no-cache bash
RUN apk add git
RUN pip install --upgrade pip
RUN pip install pytest setuptools
RUN python --version
RUN pip --version
RUN pytest --version

COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
