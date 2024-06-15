.PHONY: create-migration
create-migration:
	alembic revision --autogenerate -m "$(NAME)"


.PHONY: upgrade-db
upgrade-db:
	alembic upgrade head

.PHONY: downgrade-db
downgrade-db:
	alembic downgrade -1
