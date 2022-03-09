# Yamdb in Docker

![yamdb_workflow](https://github.com/mklstpn/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## App description:

#### Yamdb collect users reviews about films, songs, etc.

#### App have categories like 'Films', 'Music', 'Books', etc.

#### For each item can be added genre like 'Poem', 'Action', 'Pop' etc.

#### New genres can be created only by admin

## Example of .env file
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<db name>
POSTGRES_USER=<db user>
POSTGRES_PASSWORD=<user password>
DB_HOST=<container name>
DB_PORT=<db port>
```

## How to run project:
- Go into /infra dir
- Run ```docker-compose up```
- After containers start run these commands:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```
