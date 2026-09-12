# FlexHEP

FlexHEP is a single-page launch-interest site for a collaborative home exercise plan platform built for physical therapists.

## Stack

- React and Vite frontend
- FastAPI backend
- Async SQLAlchemy with SQLite
- SQLite-only email waitlist

Run with Docker Compose:

```bash
cp .env.example .env
docker compose up --build
```

The frontend is available at `http://localhost:5173` and the API at `http://localhost:8000`.
