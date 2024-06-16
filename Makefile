.PHONY: setup
setup:
	cp .env.example .env
	docker-compose build
	docker-compose up -d db
	sleep 10 # Wait pg to init
	make upgrade-db

.PHONY: start
start:
	docker compose up -d

.PHONY: enqueue
enqueue:
	docker compose run --rm --no-deps enqueue $(ARGS)

.PHONY: generate-data
generate-data:
	docker compose run --rm --no-deps worker python ./scripts/generate_data.py $(ARGS)

.PHONY: create-migration
create-migration:
	docker-compose run --rm --no-deps worker alembic revision --autogenerate -m "$(NAME)"

.PHONY: upgrade-db
upgrade-db:
	docker-compose run --rm --no-deps worker alembic upgrade head

.PHONY: downgrade-db
downgrade-db:
	docker-compose run --rm --no-deps worker alembic downgrade -1
