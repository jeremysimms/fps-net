FROM python:3.11
WORKDIR /app
COPY src/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY models/v2.pkl model.pkl
COPY ./src/app.py .
EXPOSE 8080
CMD [ "gunicorn", "-w", "4","--bind", "0.0.0.0:8080", "app:app"]