FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip3 install flask

EXPOSE 1123

ENTRYPOINT ["flask", "--app", "flaskr:create_app", "run", "--host=0.0.0.0", "--port=1123"]