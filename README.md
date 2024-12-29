# Admin panel for managing billing team activities

## Overview

This is pet-project made for learning purposes. The main goal is to create a simple admin panel for managing billing
team activities.

### Functional requirements

- Managing list of clients
- Managing list of payers
- Managing list of matters
- Managing list of actors
- Managing list of billing guidelines and its rules
- Managing relations between clients/payers/matters/actors/billing guidelines
- Ability to delegate responsibilities from one actor to another

### Technologies I wanted to use in this project

- Django
- PostgresSQL
- Nginx
- Docker
- Poetry

## How to run
1. In case tou have make installed, to start application just run
```shell
make build-up
```
2. In case you have docker-compose installed, to start application just run
```shell
docker-compose up -d --build
```
Application is available on http://localhost:80

To stop application run
```shell
make stop
```
or
```shell
docker-compose down
```
