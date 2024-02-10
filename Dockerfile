FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y make gcc

WORKDIR /app

COPY . /app
RUN make build

EXPOSE 8000
CMD ["poetry", "run", "python", "-m", "server"]
