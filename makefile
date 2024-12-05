build:
	docker compose -f local.yml up --build -d --remove-orphans

logs:
	docker compose -f local.yml logs

logs_api:
	docker compose -f local.yml logs api

logs_nginx:
	docker compose -f local.yml logs nginx

logs_postgres:
	docker compose -f local.yml logs postgres

inspect_volume:
	docker volume inspect azubisc_local_postgres_data

makemigrations:
	docker compose -f local.yml run --rm api python manage.py makemigrations

migrate:
	docker compose -f local.yml run --rm api python manage.py migrate

remove_containers_volumes:
	docker compose -f local.yml down -v

down:
	docker compose -f local.yml down

rs:
	docker compose -f local.yml run --rm api python manage.py runserver

su:
	docker compose -f local.yml run --rm api python manage.py createsuperuser

prune_images:
	docker image prune

prune_volumes:
	docker volume prune

pytest:
	docker compose -f local.yml run --rm api pytest -v