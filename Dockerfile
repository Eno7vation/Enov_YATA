FROM python:3.8.16

ENV PYTHONUNBUFFERED 1

RUN mkdir /srv/docker-test_server
ADD . /srv/docker-test_server

WORKDIR /srv/docker-test_server

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
