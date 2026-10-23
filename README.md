# Scholar Compass (full-stack)

- `backend/`  FastAPI service: scholarship data (`scholarships.json`) + scoring (`POST /api/match`)
- `frontend/` single static page that calls the API

## Run locally
```bash
cd backend && pip install -r requirements.txt && uvicorn main:app --reload   # http://localhost:8000/docs
# in another terminal
cd frontend && python -m http.server 5500                                    # http://localhost:5500
```

## Deploy
- Backend: Render web service, root dir `backend`, build `pip install -r requirements.txt`, start `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Frontend: Vercel, root dir `frontend`, framework "Other". Then set the Render URL in the `API` constant in `frontend/index.html`.

Scholarship entries intentionally omit amounts and deadlines; verify on the official page.
