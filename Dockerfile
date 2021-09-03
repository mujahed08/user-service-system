FROM python:3.9

COPY . /dist

WORKDIR /dist

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "USER_SERVIE_SYSTEM.main:app", "--host", "localhost", "--port", "8000"]