# Task Manager

task-manager/
  database/  -> PostgreSQL (init.sql + docker-compose.yml)
  backend/   -> Flask REST API (app.py)
  frontend/  -> HTML / CSS / JS

## Run (3 terminals)

1) Database
   cd database && docker compose up -d

2) Backend
   cd backend
   python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   python app.py            # http://localhost:5000

3) Frontend
   cd frontend && python3 -m http.server 5500   # http://localhost:5500

## API
GET /api/tasks | POST /api/tasks | PUT /api/tasks/<id> | DELETE /api/tasks/<id>
