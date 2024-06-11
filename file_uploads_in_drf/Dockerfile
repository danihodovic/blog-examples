FROM python:3.11

WORKDIR /app/

EXPOSE 80

RUN pip install --upgrade pip poetry==1.8.1
COPY pyproject.toml poetry.lock /app/

RUN <<EOF
poetry config virtualenvs.create false && poetry install --no-interaction
EOF

COPY file_uploads_in_drf /app/

CMD ["gunicorn", "-b", "0.0.0.0:80", "file_uploads_in_drf.wsgi", "--timeout", "90", "--max-requests=10000", "--max-requests-jitter=100"]
