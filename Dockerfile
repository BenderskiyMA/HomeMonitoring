FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine-2021-10-2621-10-26-alpine3.7
RUN apk --update add bash nano
ENV jwt_secret_key ""
ENV DATABASE_URL ""
COPY ./requirements.txt /var/www/requirements.txt
COPY ./model /var/www/app
COPY ./resources /var/www/app
COPY ./static /var/www/app
COPY ./utils /var/www/app
COPY ./*.py /var/www/app
COPY ./uwsgi.ini /var/www/py
RUN pip install -r /var/www/requirements.txt

