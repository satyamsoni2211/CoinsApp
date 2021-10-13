# Welcome to CoinsApp!

[![Django CI](https://github.com/satyamsoni2211/CoinsApp/actions/workflows/django.yml/badge.svg)](https://github.com/satyamsoni2211/CoinsApp/actions/workflows/django.yml) [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
[![Flake 8 linting](https://github.com/satyamsoni2211/CoinsApp/actions/workflows/python-app.yml/badge.svg)](https://github.com/satyamsoni2211/CoinsApp/actions/workflows/python-app.yml)

This is Django Based Application simulating actual payment transfers amongst different accounts. Application makes
extensive use of [django rest framework](https://www.django-rest-framework.org/) for its rest API. It uses PostgreSQL as
database and is capable of handling atomic transactions without failure. You can find running instance of the
application at [CoinApp](https://coins-app-demo.herokuapp.com/swagger/).

# Environment Setup

Please follow below steps to setup your enviornment and bootstrap application

## Create Virtual Environment

It is recommended to prefer virtual environment for your applications so that you can isolate your dependencies and
manage them in a better way for individual projects.

```shell
python3 -m pip install virtualenv
python3 -m virtualenv venv
```

After creation we need to active it, so that we point to the correct interpreter and environment.

```shell
source venv/bin/active # linux and MAC
.\venv\Scripts\activate # windows
```

## Installing Dependencies

We will need to install all the dependencies in order to run the project.

```shell
python3 -m pip install -r requirements.txt
```

# Setting up database

We are using docker to set up Postgres rather than installing it locally. To quickly spin up instance of **Postgres**,
run the below command.

```shell
make pg
```

If you are running this command for the first time, it will pull the image for you and set up everything locally. I have
mapped a directory for persisting file so that the data is not lost once the container is stopped. You can also run and
customize below command, for custom inputs to the **DB**.

```shell 
docker run -e POSTGRES_USER=postgres \  
-e POSTGRES_DB=postgres \  
-e POSTGRES_PASSWORD=postgres \  
-e PGDATA=/var/lib/postgresql/data/pgdata \  
-p 5432:5432 \  
-v ${PWD}/data:/var/lib/postgresql/data/pgdata \  
postgres
```

# Running Project

Before running the project make sure you have applied all the migrations to your database. To apply migrations, run:

```shell
python manage.py makemigrations
python manage.py migrate
```

Above commands will create and apply all the migrations to the project.

To run project directly in development mode, set **Debug** to **True** and run:

```shell
python manage.py runserver
```

To run using **Gunicorn** webserver, run:

```shell
gunicorn -w 4 CoinsApp.wsgi:application
```

You can also quickly spin up your server and db instance using the below command:

```shell
docker-compose up --build
```

This will spin up docker instance of your PostGres and Server, and then you can
visit [document url](localhost:8000/swagger/) to check all the available API's in the project.

# Running Test

You can also test your project simply by running below command:

```shell
make test
```

There are automated tests already in place, which will get trigger for every push to master using github
actions. ![Django CI](https://github.com/satyamsoni2211/CoinsApp/actions/workflows/django.yml/badge.svg)

# Contributing

You can contribute to the project by forking and raising a pull request. Please do not forget to mention detail
description and justifications for the enhancement. Description should contain below:

- [ ] Feature
- [ ] zen behind the enahncement
- [ ] CI checks

You can follow
me [![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/satyamsoni2211/) [![Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Follow%20%40satyam_soni1306)](https://twitter.com/satyam_soni1306) [![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/satyam-soni-ba648192/)

 
