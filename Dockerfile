FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
  vim-tiny \
  binutils \
  tzdata \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
ENV PYTHONUNBUFFERED 1

CMD ["python", "/app/manage.py", "runserver"]
