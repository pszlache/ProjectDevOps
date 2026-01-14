# ---------- STAGE 1: builder ----------
FROM python:3.12 AS builder

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/src ./src


# ---------- STAGE 2: final ----------
FROM python:3.12-slim AS final

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app/src ./src

EXPOSE 5000

CMD ["python", "src/main.py"]
