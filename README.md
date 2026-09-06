# Distributed Cache Service

Flask API demonstrating a Redis-backed distributed cache with TTL and cache invalidation.

## Features
- Redis distributed cache
- Cache-aside pattern
- TTL support
- Cache hit/miss tracking
- Cache invalidation
- Health endpoint
- Pytest tests

## Run

```bash
docker run --name day321-redis -p 6379:6379 -d redis:7-alpine
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

Endpoints:
- GET /api/products/<id>
- DELETE /api/cache/products/<id>
- GET /health
