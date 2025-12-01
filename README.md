# techgear-e-commerce-platform-215921-215931

Backend (FastAPI) notes:
- Configure environment via ecommerce_backend/.env (see .env.example).
- Key vars:
  - DATABASE_URL: database connection string (defaults to SQLite file).
  - SECRET_KEY: required for JWT; set to a secure random value in production.
  - BACKEND_CORS_ORIGINS: comma-separated list of allowed origins (e.g., http://localhost:3000).
  - SEED_DATA_ON_STARTUP: set true to seed dev data; automatically applies for SQLite.
- On startup the backend runs create_all and optional seeding for dev.

Frontend (React) notes:
- Use .env.development to set REACT_APP_API_BASE_URL pointing to backend URL (e.g., http://localhost:8000).
- API client should read the base URL from process.env and attach Authorization: Bearer <token> from AuthContext or similar.