# Image Moderation API Project

## Overview

This project implements an Image Moderation API with a FastAPI backend connected to MongoDB, and a React frontend UI. It moderates images for harmful or explicit content and returns a safety report.

---

## Features

- Token-based authentication with bearer tokens (admin and user tokens).
- MongoDB database for storing tokens and API logs.
- Admin endpoints to create, list, and delete tokens.
- Image moderation endpoint (mock implementation).
- Dockerized backend, frontend, and MongoDB services.
- Minimal React UI for authentication and image upload.

---

## Prerequisites

- **Docker** and **Docker Compose** installed (for Docker deployment).
- **Python 3.12+**, **Node.js 18+**, and **npm/yarn** installed (for local development).
- Basic familiarity with REST APIs and React.

---

## Quick Start with Docker

### 1. Clone the repository

```bash
git clone <repository_url>
cd ImageModerationAPIProject
````

### 2. Create backend environment file

Copy the example env file and adjust if needed:

```bash
cd backend
cp .env.example .env
# Edit .env to set MONGODB_URI if you want custom MongoDB connection
```

### 3. Build and start all services

From the root project directory:

```bash
sudo docker-compose up --build
```

This will build and start:

* MongoDB database container
* FastAPI backend on `http://localhost:7000`
* React frontend on `http://localhost:3000`

### 4. Access the frontend

Open your browser at:

```
http://localhost:3000
```

---

## Running Locally (Without Docker)

### Backend

1. Navigate to backend directory:

   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Setup MongoDB

   * Ensure you have MongoDB installed and running locally or provide a MongoDB URI.
   * Update `.env` file with your MongoDB URI if not using default localhost.

5. Run the backend server:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 7000
   ```

### Frontend

1. Navigate to frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the React development server:

   ```bash
   npm start
   ```

4. Open your browser at:

   ```
   http://localhost:3000
   ```

---

## Usage

### Generating Admin Token

To generate an admin token, insert it manually into the MongoDB tokens collection or use backend admin APIs (requires existing admin token).

Example to insert token in MongoDB shell:

```js
use image_moderation
db.tokens.insertOne({
  token: "supersecureadmintoken123",
  isAdmin: true,
  createdAt: new Date()
})
```

Use this token in the `Authorization` header as:

```
Authorization: Bearer supersecureadmintoken123
```

to access protected admin endpoints or generate new user tokens.

---

### API Endpoints

* **POST** `/auth/tokens` - Generate a new token (admin only).
* **GET** `/auth/tokens` - List tokens (admin only).
* **DELETE** `/auth/tokens/{token}` - Delete a token (admin only).
* **POST** `/moderate` - Upload image for moderation (requires valid token).

---

## Troubleshooting

* **CORS errors or "Failed to fetch"**
  Ensure backend CORS middleware allows your frontend origin (localhost or Docker IP).

* **Backend connection issues**
  Verify MongoDB URI in `.env` is correct and MongoDB container or service is running.

* **Docker build caching issues**
  Use `docker-compose build --no-cache` to rebuild images cleanly.

---

## License

MIT License

```

---

If you want me to generate a `.env.example` or `docker-compose.yml` sample as well, just ask!
```
