# Group 1 Local Development Setup

This directory contains a Docker Compose configuration for setting up a local MySQL database for development.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Starting the MySQL Database

1. Navigate to the group1 directory:
   ```bash
   cd group1
   ```

2. Start the MySQL service:
   ```bash
   docker-compose up -d
   ```

   This will start a MySQL 8.0 database container in the background.

3. To stop the service:
   ```bash
   docker-compose down
   ```

   To stop the service and remove the data volume:
   ```bash
   docker-compose down -v
   ```

## Connecting to the MySQL Database

The MySQL database is accessible at:
- Host: localhost
- Port: 3306
- Database: defaultdb (or the value of DB_NAME environment variable)
- User: user (or the value of DB_USER environment variable)
- Password: password (or the value of DB_PASSWORD environment variable)
- Root Password: rootpassword (or the value of MYSQL_ROOT_PASSWORD environment variable)

## Configuring the Django Project

To use this local MySQL database with the Django project, update the `english_website/secret.py` file with the following:

```python
DB_NAME = 'defaultdb'  # or your custom database name
DB_USER = 'user'       # or your custom username
DB_PASSWORD = 'password'  # or your custom password
DB_HOST = 'localhost'
DB_PORT = '3306'
```

## Environment Variables

You can customize the MySQL configuration by setting the following environment variables before running `docker-compose up`:

- `DB_NAME`: The name of the database to create
- `DB_USER`: The username for the database
- `DB_PASSWORD`: The password for the user
- `MYSQL_ROOT_PASSWORD`: The password for the MySQL root user

Example:
```bash
export DB_NAME=mydb
export DB_USER=myuser
export DB_PASSWORD=mypassword
export MYSQL_ROOT_PASSWORD=myrootpassword
docker-compose up -d
```

## Troubleshooting

- If you encounter port conflicts, you can change the port mapping in the `docker-compose.yml` file.
- If you need to access the MySQL command line:
  ```bash
  docker exec -it group1-mysql mysql -u root -p
  ```