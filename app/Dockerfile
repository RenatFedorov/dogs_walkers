FROM python:3.10-bullseye
LABEL authors="renat"

ENV APP_HOME=/home/app/web
WORKDIR $APP_HOME

COPY requirements.txt .
RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT [ "/bin/bash", "entripoint.sh" ]