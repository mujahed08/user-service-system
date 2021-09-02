FROM python:3.9

RUN pip install -r requirements.txt

EXPOSE 80

COPY ../user-service-system /app

CMD ["uvicorn", "app.USER_SERVIE_SYSTEM.main:app", "--host", "0.0.0.0", "--port", "80"]