# pharma-copilot

Minimal demo project: backend (FastAPI) + frontend (Vite + React + Tailwind) + docker-compose.

Features:
- Backend: CRUD endpoints for medicines and simple AI copilot chat.
- Predict endpoint: `GET /predict?sku=SKU&days=7` returns fake forecast data.
- Chat endpoint: `POST /chat` handles simple queries like "low stock" or "predict paracetamol".
- Database: SQLite database with `medicines` table (id, name, qty, min_stock, expiry_date).
- Frontend: Inventory page and Copilot chat UI.

Run locally (with Docker Compose):

1) Build & start:

```bash
docker-compose up --build
```

2) Backend API: http://localhost:8000
3) Frontend (Vite dev): http://localhost:5173

Project layout (important files):
- `backend/` - FastAPI app and Dockerfile
- `frontend/` - Vite + React + Tailwind app and Dockerfile
- `docker-compose.yml` - runs both services

API endpoints:
- `GET /medicines` - list medicines
- `POST /medicines` - create medicine
- `PUT /medicines/{id}` - update medicine
- `DELETE /medicines/{id}` - delete medicine
- `GET /predict?sku=SKU&days=7` - fake forecast
- `POST /chat` - basic copilot (accepts JSON `{ "message": "..." }`)

Notes:
- The backend stores data in `pharma.db` (SQLite) in the backend service working directory.
- The Copilot is a simple rule-based demo. Extend with real AI integrations as needed.

Inventory &amp; Procurement Management
