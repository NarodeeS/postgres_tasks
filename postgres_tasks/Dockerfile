FROM python:3.11-alpine

RUN apk --update --upgrade \
    add gcc musl-dev jpeg-dev zlib-dev \
    libffi-dev cairo-dev pango-dev \
    gdk-pixbuf-dev

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /server

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY supervisor/supervisord.conf /etc/supervisor/supervisord.conf

COPY . .

CMD [ "supervisord" ]
