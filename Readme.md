
We used django as the backend for this service. The backend is a REST API that is used by the frontend to register ads and get the ads.

## ⚙️ Setup Guide

### 1. Clone the project

### 2. Create your `.env` file

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

If you're using a **cloud database**, update the values in `.env` with your own credentials.

---

### 3. (Optional) Start the MySQL database with Docker

Once Docker is installed, run:

```bash
docker-compose up -d
```

This will run a MySQL container using the settings from your `.env` file.

> Skip this step if you're connecting to a remote or cloud-hosted database.

---

### 4. Set up Django

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 5. Run migrations and start the server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Now visit: [http://localhost:8000](http://localhost:8000)

---

## 🧪 .env variables

These variables are used to configure the database:

```env
DATABASE_HOST=127.0.0.1
DATABASE_NAME=software-database
DATABASE_USER=user
DATABASE_PASSWORD=password
MYSQL_ROOT_PASSWORD=password
DATABASE_PORT=3306
```
