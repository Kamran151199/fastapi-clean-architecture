include ./src/.env

pg-makemigrations:
	@read -p "Enter migration message: " message && alembic -c ./src/infrastructure/db/postgres/alembic.ini revision --autogenerate -m "$$message"

pg-migrate:
	@alembic -c ./src/infrastructure/db/postgres/alembic.ini upgrade head