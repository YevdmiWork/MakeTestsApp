# MakeTestsApp

> Work in progress.

Application for creating and running tests.

## Tech Stack

* Python 3.11+
* Django 5.2
* PostgreSQL
* Selectel S3
* Redis
* Docker Compose

## Deployment

### 1. Clone the repository

```bash
git clone <repository-url>
cd maketestsapp
```

### 2. Configure environment

Create a `.env` file in the project root:

```env
DEBUG=on

SECRET_KEY=*

POSTGRES_NAME=*
POSTGRES_USER=*
POSTGRES_PASSWORD=*
POSTGRES_PORT=5432
POSTGRES_HOST=db

ADMIN_URL=admin/
DEBUG_TOOLBAR=True

LANGUAGE_CODE=ru
TIME_ZONE=Europe/Moscow

MEDIA_URL=/media/
STATIC_URL=/static/

ALLOWED_HOSTS=localhost,127.0.0.1
INTERNAL_IPS=127.0.0.1

AWS_ACCESS_KEY_ID=*
AWS_SECRET_ACCESS_KEY=*
AWS_STORAGE_BUCKET_NAME=*
AWS_S3_ENDPOINT_URL=https://s3.ru-1.storage.selcloud.ru
AWS_S3_REGION_NAME=ru-1
```

### 3. Build and start containers

```bash
docker compose up -d --build
```

### 4. Apply migrations

```bash
docker compose exec web python manage.py migrate
```

The application will be available at:

```text
http://127.0.0.1:8000/tests/
```
