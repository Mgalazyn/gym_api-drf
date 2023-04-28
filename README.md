
# gym_api-drf

![tesx](https://user-images.githubusercontent.com/91530764/233931541-a75336bf-8865-4f1b-994a-c28c5c2d4b6e.png)


This project is a RESTful API built with Python, Django, and Django REST Framework to manage a gym's memberships and classes. It uses Docker for containerization and Postgresql for data storage. Developed in spirit in the of TDD. Test written mostly in unitest, django.tests and with rest_framework.test,


## Getting Started

To get started with this project, you'll need to have Docker and Docker Compose installed on your machine. You can download them here.

Once you have Docker and Docker Compose installed, clone the repository to your machine:

```bash
  git clone https://github.com/Mgalazyn/gym_api-drf.git
```

Change into the project directory:

```bash
  cd gym_api-drf
```
```bash
  pip install -r requirements.txt
```
Create a file called .env and add the following environment variables:

```bash
DEBUG = 1
DB_HOST= your_db_host
DB_NAME= your_db_name
DB_USER= your_db_user
DB_PASS= your_db_password
SECRET_KEY= your_secret_key

```

Build and run the Docker containers:
```bash
docker-compose up -d --build
```
## Running Tests

To run tests, run the following command

```bash
  docker-compose app --rm run sh -c 'python manage.py'
```


## License

[MIT](https://choosealicense.com/licenses/mit/)

