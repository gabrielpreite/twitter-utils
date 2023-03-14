FROM python:3.9
WORKDIR /usr/src/app
COPY . .
RUN apt update --allow-insecure-repositories && apt install tzdata -y
ENV TZ="Europe/Rome"
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python3", "./app.py"]