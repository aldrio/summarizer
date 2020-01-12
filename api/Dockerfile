FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY build.py ./
RUN python build.py

COPY . .

EXPOSE 8000

CMD gunicorn --bind 0.0.0.0:8000 wsgi
