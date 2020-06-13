FROM python:3

# We copy just the requirements.txt first to leverage Docker cache
COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5555

CMD [ "python", "app.py" ]