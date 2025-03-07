# Blog


Blog created on Django + PostgreSQL and launched in conteiners using Docker, allowing users to create, edit and manage posts.

## Tech Stack

- Backend: Django
- Database: PostgreSQL
- Conteinerization: Docker, Docker-Compose
- Frontend: Django Templates & Bootstrap

## Features

- Create, edit, delete and publish blog posts
- User authentication and registration 
- Ability to change a password
- Logging

## Getting started

Follow these steps to set up and run project locally with Docker

## Prerequisites

Ensure that you have the following installed on your system

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Installation

1. Clone the repository:
```
git clone https://github.com/ArtemRuban18/rubanarse-blog
cd rubanarse-shop
```
Create a .env file and configure environment variables

2.Build and run the containers:
```
docker-compose up --build
```

3.Create new database migrations:
```
docker-compose run django python manage.py makemigrations
```

4.Run database migrations:
```
docker-compose run django python manage.py migrate
```

5.Now you can run the server:
```
docker-compose run django python manage.py runserver
```

Create superuser:
```
docker-compose run django python manage.py createsuperuser
```
