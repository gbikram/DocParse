FROM python:3

WORKDIR /backend

ADD . /backend

RUN python3 -m pip install --upgrade --force-reinstall -r requirements.txt
# RUN python3 -m pip install --no-cache-dir -r requirements.txt --upgrade

# CMD [ "python", "app.py" ]
CMD [ "uwsgi", "app.ini" ]
