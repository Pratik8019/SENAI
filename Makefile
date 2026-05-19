.PHONY: dev build up down logs seed index migrate test clean

# Development
dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# Production build
build:
	docker compose build --no-cache

# Start services
up:
	docker compose up -d

# Stop services
down:
	docker compose down

# View logs
logs:
	docker compose logs -f

# Database migrations
migrate:
	docker compose exec api alembic upgrade head

# Seed database with sample data
seed:
	docker compose exec api python -m scripts.seed_db

# Index knowledge base into ChromaDB
index:
	docker compose exec api python -m scripts.index_knowledge_base

# Run backend tests
test:
	docker compose exec api pytest tests/ -v

# Clean everything
clean:
	docker compose down -v --remove-orphans
	docker system prune -f
