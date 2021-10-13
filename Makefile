PWD=$(shell pwd)
pg:
	@docker run -e POSTGRES_USER=postgres \
      -e POSTGRES_DB=postgres \
      -e POSTGRES_PASSWORD=postgres \
      -e PGDATA=/var/lib/postgresql/data/pgdata \
      -p 5432:5432 \
      -v ${PWD}/data:/var/lib/postgresql/data/pgdata \
      postgres

test:
	@ENV=TEST python manage.py test

service:
	@docker-compose up --build