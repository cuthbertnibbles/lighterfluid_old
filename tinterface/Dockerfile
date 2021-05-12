FROM python
WORKDIR /usr/ripper

RUN pip3 install gunicorn

RUN pip3 install flask mysql-connector-python requests

COPY ./src ./

CMD [ "python", "./main.py" ]