# Mock-WS

Real-time market-data pipeline built with Django, FastAPI, Redis, MySQL, WebSocket, and Docker.

## Stack

* Python **3.11.2**
* Django — web/admin application
* FastAPI — REST API
* WebSocket — real-time market-data ingestion
* Redis Pub/Sub — asynchronous message transport
* MySQL — persistent RTDS storage
* MinIO — profile-photo storage
* Nginx — `/app` and `/api` routing
* Docker Compose — local deployment

## Architecture

```text
Mock WebSocket
      ↓
   WorkerA
      ↓
 Redis Pub/Sub
      ↓
   WorkerB
      ↓
    MySQL
      ↑
 FastAPI / Django
```

WorkerA receives market updates and publishes structured JSON messages to Redis. WorkerB asynchronously consumes those messages and stores them transactionally in MySQL.

The real market data source was not used because the developer does not have a personal account on the broker's website. Therefore, a local WebSocket mock is used to provide realistic market-data events and keep the complete pipeline runnable and testable.

## Setup

Prerequisite: Docker Desktop.

```powershell
git clone https://github.com/qblob/Mock-WS.git
cd Mock-WS

copy .env.example .env
docker compose up -d --build
```

Initialize the databases:

```powershell
docker compose run --rm django python django_app/manage.py migrate
docker compose run --rm fastapi python -m core.create_tables
```

## Access

* Django: `http://localhost/app/`
* FastAPI Swagger: `http://localhost/api/docs`

Infrastructure ports:

* Redis: `6204`
* MySQL: `6206`
* Django: `6280`
* FastAPI: `6288`

## Configuration

Runtime secrets are stored in `.env` and excluded from Git.

FastAPI requires the API key from `.env` in the `X-API-Key` header.

## API

```text
GET /api/users/get/profile/{userid}
GET /api/users/get/photo/{userid}
GET /api/RTDS/get/current/{id}
GET /api/RTDS/get/historical/{id}
```

## Design

* **WebSocket:** event-driven real-time data ingestion without polling.
* **Redis Pub/Sub:** decouples data ingestion from persistence.
* **Async I/O:** used by WorkerA, WorkerB, Redis, and FastAPI.
* **Transactions:** WorkerB writes RTDS records transactionally.
* **Reconnects:** WorkerA reconnects after connection failures.
* **MinIO:** stores profile photos as objects instead of database blobs.
* **Nginx:** provides a single entry point for `/app` and `/api`.
* **Docker Compose:** provides reproducible local infrastructure.
* **Mock WebSocket:** used because the developer does not have a personal broker account.
