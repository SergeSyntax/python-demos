
Alembic Operations:

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
## run tests
```bash
pytest
```