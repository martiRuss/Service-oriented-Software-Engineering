
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV POSTGRESQL_URL "postgres://faxtwhkp:pcfzlSgODUE7BqD7K7WUDNH8EefXBDkt@topsy.db.elephantsql.com/faxtwhkp"
CMD ["flask", "run"]
