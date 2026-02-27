FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY legacy ./legacy
COPY configs ./configs

ENV APP_HOST=0.0.0.0
ENV APP_PORT=8080
ENV APP_ENV=production
ENV LOG_LEVEL=INFO
ENV PYTHONPATH=/app/src
ENV PROLOG_DATA_FILE=/app/legacy/academic_project/store.pl

EXPOSE 8080

CMD ["uvicorn", "polyglot_commerce.api.app:app", "--host", "0.0.0.0", "--port", "8080"]
