FROM python:3.12.2
ENV PYTHONUNBUFFERED = 1
WORKDIR /usr/src/app
COPY ../requirements ./
RUN pip install --no-cache-dir -r dev.requirements.txt
COPY .. .