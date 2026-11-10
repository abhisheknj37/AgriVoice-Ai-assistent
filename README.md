# AgriVoice — AI-Powered Farming Assistant

<escape>🚀 Live Backend API: https://agrivoice-api-5jh2.onrender.com</escape>  
> Django API deployed on Render. Configure a persistent database and required provider credentials before production use.


AgriVoice combines a Django REST Framework API with a React frontend to provide crop guidance, soil recommendations, weather information and an AI farming assistant.

## Repository layout

- `backend/` — Django API, authentication, ML model and deployment configuration
- `agrivoice-ui/` — React frontend (if present in your checkout)
- `DEPLOYMENT.md` and `FREE_DEPLOYMENT.md` — hosting notes

## Backend: local setup

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/`.

## Configuration

Copy `backend/.env.example` to `backend/.env` and provide values for the services you use. Never commit real API keys, database passwords, email passwords or production secret keys.

For production set at least:

- `DJANGO_SECRET_KEY` — a long, random secret
- `DJANGO_SETTINGS_MODULE=agrivoice.settings_prod`
- `DATABASE_URL` — a persistent PostgreSQL URL for production
- `OPENAI_API_KEY` and/or `SARVAM_API_KEY` when those integrations are enabled
- `FRONTEND_URL` — the deployed frontend origin

The production settings reject the placeholder secret key and use environment-based host and CORS configuration.

## Frontend

If the React frontend is included in your checkout, enter its directory, install dependencies and run its documented build command. Configure its API base URL to point to the deployed backend.

## API overview

- `/api/` — application API routes
- `/api/auth/` — authentication routes
- `/admin/` — Django administration

See `backend/api/urls.py` and `backend/users/urls.py` for the authoritative endpoint list.

## Deployment

Use the deployment guides in this repository as a starting point. Run Django with Gunicorn, apply migrations during release, and serve static assets using WhiteNoise or a reverse proxy. Use a persistent database for user data; ephemeral service storage is not suitable for production records.

## Security notes

- Do not use Django's development server in production.
- Do not use wildcard allowed hosts or hardcoded credentials.
- Keep secrets in the hosting provider's environment-variable settings.
- Configure the exact frontend origin in `FRONTEND_URL`.
