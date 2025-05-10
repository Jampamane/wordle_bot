FROM python:3.12-slim

RUN apt update && apt install -y \
    wget \
    unzip \
    curl \
    chromium-driver \
    chromium \
    libnss3 \
    libgconf-2-4 \
    libxi6 \
    libgbm1 \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/bin:$PATH"

WORKDIR /app

COPY . .

RUN pip install uv
RUN uv sync

CMD ["uv", "run", "wordle-bot"]
