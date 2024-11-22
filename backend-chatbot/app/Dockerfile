FROM python:3.10-slim

# RUN apt-get update && apt-get install -y curl && apt-get clean

# Install and add Poetry to PATH
# RUN curl -sSL https://install.python-poetry.org | python3 -
# ENV PATH="/root/.local/bin:$PATH"
RUN pip3 install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

CMD ["poetry", "run", "fastapi", "run", "main.py"]


