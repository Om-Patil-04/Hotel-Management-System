FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY setup.py requirements.txt ./

RUN pip install --no-cache-dir --no-build-isolation --progress-bar off -e .

COPY . .

EXPOSE 5000

CMD ["python", "application.py"]
