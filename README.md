# Rick-Morty (API)

### Requirements

### Technologies to use

### How to run:

- Create venv: "python -m venv venv"
- Activate it: "source venv/bin/activate"
- Install requirements: "pip install -r requirements.txt"
- Create new Postgres DB and User
- Copy .env.example and add your data
- Run migrations: "python manage.py migrate"
- Run Redis server: "docker run -d -p 6379:6379 redis"
- Run celery worker for task handling: "celery -A simpsons_api worker -l INFO "
- Run celery beat for task scheduling: "celery -A simpsons_api beat -l INFO --scheduler django_celery_beat.schedulers:
  DatabaseScheduler"
- Create schedule for running sync in DB
- Run app: "python manage.py runserver"