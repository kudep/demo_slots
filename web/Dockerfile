FROM python:3.10.12-slim

WORKDIR /web

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8501

COPY . /web
ENTRYPOINT ["streamlit", "run", "ui.py", "--server.port=8501", "--server.address=0.0.0.0"]