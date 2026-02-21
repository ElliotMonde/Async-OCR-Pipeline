Author: Elliot Phua

Email: elliotphua@gmail.com

# OCR Service Application

This is a full-stack OCR (Optical Character Recognition) application that provides both synchronous and asynchronous image processing capabilities. It is built with a FastAPI backend, a React frontend, and uses Redis and PostgreSQL for task management and persistence. The project is structured as multi-container application using Docker Compose to ensure easy setup and deployment, and separate concerns between frontend, backend, and worker.

## Getting Started

The easiest way to run the application is using Docker Compose.

### Prerequisites
- Docker and Docker Compose installed on your machine.

### Untar project file
Firstly, "untar" the project tar file using the following command:

```bash
tar -xvzf mercari_assignment.tar.gz
```

Then `cd` into the project directory.

```bash
cd mercari_assignment
```

### Build and Run
To build and start all services (Frontend, Backend API, Worker, Database, Redis), run:

```bash
docker compose up --build
```

Once up and running, you can access the application at:
- **Frontend**: [http://localhost:5173](http://localhost:5173)
- **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

Recommended to use the interface at the Backend API Docs to test the API endpoints.

---

## Backend APIs

### 1. Synchronous OCR (`/image-sync`)
Upload image(s) and get the OCR results immediately in the response. The API takes `base64_encoded_string` or an `array of base64_encoded_string` (image batch) as input.

- **Endpoint**: `POST /image-sync`
- **Body**:
  ```json
  {
    "image_data": ["<base64_encoded_string>", ...]
  }
  ```
- **Response**:
  ```json
  {
    "text": ["Extracted text 1", ...]
  }
  ```

### 2. Asynchronous OCR (`/image`)
Offload heavy OCR tasks to a background worker. Returns a Task ID immediately. This API takes `base64_encoded_string` or an `array of base64_encoded_string` (image batch) as input.

- **Endpoint**: `POST /image`
- **Body**:
  ```json
  {
    "image_data": ["<base64_encoded_string>", ...]
  }
  ```
- **Response**:
  ```json
  {
    "task_id": "c56a4180-65aa-42ec-a945-5fd21dec0538"
  }
  ```

### 3. Get Async Task Result (`/image`)
Check the status or get the results of a submitted async task. The API takes `task_id` string as input. If the task is in progress, it will return an empty string for task with single image, or `[""]` for a batch task. If the task is completed, it will return the extracted text.

- **Endpoint**: `GET /image?task_id={task_id}`
- **Response**:
  ```json
  {
    "task_id": ["Extracted text 1", ...] 
  }
  ```

---

## Frontend Interface

The frontend is a modern React application built with Vite and Material UI for easier visualization and testing.

- **Sync OCR**: Upload an image to the left column. The UI waits for the server to process it and displays the text immediately.
- **Async OCR**: Upload an image to the right column. The UI receives a Task ID, polls the status, or allows you to manually check the result using the provided Task ID.

---

## Design Decisions

### Project Structure
The project is organized as a monorepo for simplicity:
- **`app/`**: Contains the FastAPI web server and API routers. This backend is structured using the router-service-repo (RSR) pattern. This pattern is used to separate concerns, allow for dependency injection, and make the code more modular and maintainable.
- **`ocr-frontend/`**: The React + Vite frontend application.
- **`shared/`**: Common logic shared between the API service and the background worker (DB models, Redis client, OCR logic).
- **`worker/`**: (In Docker) Runs the background processing script defined in `shared/worker/worker.py`.

### Asynchronous OCR Management
To handle potentially slow OCR operations without blocking the main API server, I used an event-driven architecture:
1.  **Submission**: When a user submits an async task, the API creates a record in PostgreSQL with status `PENDING` and pushes the `task_id` to Redis.
2.  **Processing**: A dedicated background worker (`ocr_worker`) constantly listens to the Redis queue. It picks up tasks, processes them using the OCR engine, and updates the database with the results (or failure status).
3.  **Result**: The user can query the API with the `task_id` to retrieve the final text once processing is complete.

### Queue System Design
I implemented a robust queueing system using Redis to ensure reliability:

1.  **Main Queue (`ocr:queue`)**:
    -   This is a standard List where new tasks are pushed.
    -   The worker blocks on this queue (`BRPOP`) waiting for new work, ensuring instant processing when tasks arrive.

2.  **Retry Queue (`ocr:retry`)**:
    -   If a task fails during processing, it is not immediately discarded.
    -   It is pushed to a Redis Sorted Set (`ZSET`) with a timestamp score calculated by an **Exponential Backoff** strategy (`min(2^attempt, 60s)`).
    -   The worker periodically checks this set (`promote_retries`) and moves ready items back to the Main Queue.

3.  **Dead Letter Queue (`ocr:dead`)**:
    -   If a task fails repeatedly and exceeds the maximum number of attempts (default: 3), it is moved to the Dead Letter Queue.
    -   This prevents "poison pill" tasks from looping infinitely and allows me to inspect failed payloads for debugging.


