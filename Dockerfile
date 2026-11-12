FROM python:3.8-slim

LABEL maintainer="devops@citizen.tech"
ENV PORTA=8476 PYTHONDONTWRITEBYTECODE=1

RUN useradd -r -u 10001 -m app
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app . .

USER app
EXPOSE 8476
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request,os; urllib.request.urlopen('http://127.0.0.1:'+os.environ['PORTA'])"
CMD ["python", "app.py"]
