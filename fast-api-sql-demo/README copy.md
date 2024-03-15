# entry-service
Service for admin and inference uis

## requirements
- Python version <= 3.11.5
- virtual env setup
  ```bash
    python3 -m venv .venv
    source ./.venv/bin/activate
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
pytest --disable-warnings 
```