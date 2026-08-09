FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    RIPPLECHECK_MODE=fixture

WORKDIR /app
COPY . /app

RUN addgroup -S ripplecheck && adduser -S ripplecheck -G ripplecheck \
    && chown -R ripplecheck:ripplecheck /app

USER ripplecheck
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)" || exit 1

CMD ["python", "main.py", "web"]

