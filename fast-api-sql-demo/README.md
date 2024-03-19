# entry-service
Service for admin and inference uis

## requirements
- Python version <= 3.11.5
- virtual env setup
  ```bash
    python3 -m venv venv
    source ./venv/bin/activate
    pip install -r requirements.txt
  ```

## run the application

- run prod
  ```bash
    uvicorn app.main:app
  ```
## run in development
  ```bash
    uvicorn app.main:app --reload
  ```

  Open your browser at for th app: http://127.0.0.1:8000.
  for the Interactive API docs: http://127.0.0.1:8000/docs
  alternative api docs:  http://127.0.0.1:8000/redoc
  open api schema http://127.0.0.1:8000/openapi.json


## run tests
```bash
pytest --disable-warnings -vv
```


## Alembic Operations:

setup alembic folder and config files
```bash
alembic init <folder name>
```

create alembic revision (migration)
```bash
alembic revision -m "Add user and todo models"
```

run migrations/revisions with alembic
```bash
alembic upgrade <revision #>
```
undo migrations/revision with alembic
```bash
alembic downgrade -l
```


to run the app get postgres running
```bash
docker compose up
```

and then run the api in dev mode
```bash
uvicorn main:app --reload
```
