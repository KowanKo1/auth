### Run FastAPI Project

Create and get inside your venv then:

```bash
pip install -r requirements.txt
fastapi dev main.py
```

### Migrations with Alembic

create new migration:

```bash
alembic revision --autogenerate -m "<MIGRATION_NAME>"
```

Run migrations:

```bash
alembic upgrade head
```

Go back to before version:

```bash
alembic downgrade -1
```

Go back multiple migrations:

```bash
alembic downgrade <MIGRATION_IDENTIFIER>
```

View list of all migrations:

```bash
alembic history
```
