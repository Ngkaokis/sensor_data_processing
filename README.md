## Sensor Reading Csv Data Processing

This repo implement Work Queue System to process multiple large csv files in a distributed way

To scale up the system, we can increase the worker replicas / concurrency.
But please be reminded that we need to increase the connection pool size of the database as well

### TL;DR

```
make setup
make start
make enqueue ARGS="data"
```

### Setup

```
./scripts/setup.sh

or

make setup
```

### Start the work queue

```
docker compose up -d

or

make start
```

### Enqueue the jobs

```
docker compose run --rm --no-deps enqueue [-h] [--dbhost DBHOST] [--dbname DBNAME] [--dbuser DBUSER] [--dbpass DBPASS] [--dbport DBPORT] directory

or

make enqueue ARGS="[-h] [--dbhost DBHOST] [--dbname DBNAME] [--dbuser DBUSER] [--dbpass DBPASS] [--dbport DBPORT] directory"
```

### Generate Data

```
docker compose run --rm --no-deps worker python ./scripts/generate_data.py [--size] [--output]

or

make generate-data ARGS="[--size] [--output]"
```

### Test

```
make test
```

### Monitor the job status

```
1. docker compose up monitor
2. Access the panel via http://localhost:5555/
```

### ER diagram

![alt er_diagram](./docs/er_diagram.png)

### Table Structure

![alt sensor_table_structure](./docs/sensor_table_structure.png)

![alt sensor_reading_table_structure](./docs/sensor_reading_table_structure.png)

### Tech Stack

- Celery
- Rabbitmq
- Postgres
- Docker
- SQLAlchemy
