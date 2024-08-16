FROM python:3.10.12-slim

RUN apt-get update && \
    apt-get install -y git
    
ARG HUGGINGFACEHUB_API_TOKEN=$HUGGINGFACEHUB_API_TOKEN

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8000

COPY . /app

RUN ["pytest", "test.py"]

CMD ["python3", "app.py"]