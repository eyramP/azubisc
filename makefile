build:
	docker compose -f local.yml up --build -d --remove-orphans
logs_api:
	docker compose -f local.yml logs api
logs_postgres:
	docker compose -f local.yml logs postgres
inspect_volume:
	docker volume inspect azubisc_local_postgres_data