FROM python:3

WORKDIR /backend

ADD . /backend

RUN pip install --no-cache-dir -r requirements.txt

# CMD [ "python", "app.py" ]
CMD [ "uwsgi", "app.ini" ]