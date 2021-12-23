# Проект Yamdb в Docker

![yamdb_workflow](https://github.com/mklstpn/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Описание приложения

#### Проект YaMDb собирает отзывы пользователей на произведения

#### Произведения делятся на категории(например, "Музыка", "Фильмы" и тд.)

#### Каждому произведению может быть присвоен жанр(например, "Роман", "Поп" и тд.)

#### Новые жанры может создавать только администратор

#### Project is available at http://51.250.1.69 or http://roomtake.store

## Пример заполнения .env файла
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<db name>
POSTGRES_USER=<db user>
POSTGRES_PASSWORD=<user password>
DB_HOST=<container name>
DB_PORT=<db port>
```

## Как запустить проект
- Перейти в директорию /infra
- Выполнить ```docker-compose up```
- После успешного поднятия контейнеров последовательно выполнить:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```

## Автор
#### Степанов Михаил
