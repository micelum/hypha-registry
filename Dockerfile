FROM python:3.7-alpine

COPY . .
RUN pip install -r requirements.txt
RUN alembic upgrade head

ENTRYPOINT ["nameko", "run", "app"]