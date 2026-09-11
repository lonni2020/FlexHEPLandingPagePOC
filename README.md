# FlexHEP

FlexHEP is a single-page launch-interest site for a collaborative home exercise plan platform built for physical therapists.

## Stack

- React and Vite frontend
- FastAPI backend
- Async SQLAlchemy with SQLite
- SQLite-only email waitlist

## Local Development

Copy `.env.example` to `.env` if you want to override the defaults.

Run the backend from `backend/`:

```bash
uv sync
uv run uvicorn app.main:app --reload
```

Run the frontend from `frontend/` in a second terminal:

```bash
npm install
npm run dev
```

Open `http://localhost:5173`.

Alternatively, run both services with Docker Compose:

```bash
docker compose up --build
```

The frontend is available at `http://localhost:5173` and the API at `http://localhost:8000`.

## Production Build

Build the frontend with `npm run build`. FastAPI serves `frontend/dist` when the backend runs from the project root or in the provided Docker Compose setup.

The waitlist endpoint is `POST /api/v1/waitlist` and stores only the normalized email and signup timestamp in SQLite.
