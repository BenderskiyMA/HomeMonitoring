FROM tiangolo/uwsgi-nginx-flask:python3.8-2020-05-09
ENV jwt_secret_key ""
ENV DATABASE_URL ""
COPY ./requirements.txt /app/requirements.txt
COPY . /app
RUN pip install -r /app/requirements.txt
