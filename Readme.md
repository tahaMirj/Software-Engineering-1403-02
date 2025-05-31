
We used django as the backend for this service. The backend is a REST API that is used by the frontend to register ads and get the ads.

## Installation

First thing first, install the requirements:

```bash
pip install -r requirements.txt
```

## Usage

To run this project simply run the following command:

```bash
python manage.py runserver
```

Then open your browser and go to `http://localhost:8000/` to see the project.



Then add the following line:

```python

DB_NAME = ''
DB_USER = ''
DB_PASSWORD = ''
DB_HOST = ''
DB_PORT = ''
```

to run a redis instance:
```
docker run --rm -p 6379:6379 redis
```
