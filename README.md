# Job Application Tracker API

A REST API built with Python, FastAPI, SQLAlchemy, and PostgreSQL for securely managing job applications. The API supports authentication, user-owned records, searching, filtering, sorting, and pagination.

## Features

- User registration and login
- Password hashing
- JWT-based authentication
- User-specific application access
- Create, retrieve, update, and delete job applications
- Search by company or position
- Filter by application status and company
- Sort application results by company
- Pagination
- Request validation with Pydantic
- PostgreSQL database integration
- SQLAlchemy ORM
- Database migration management with Alembic
- Automated tests with pytest
- Interactive API documentation with Swagger UI

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- PyJWT
- pwdlib
- pytest
- HTTPX
- python-dotenv
- Uvicorn

## Prerequisites

- Python 3.12 or compatible version
- PostgreSQL
- Git

## Local Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd job-tracker
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository's actual URL.

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root. Configure your PostgreSQL connection and JWT settings using the variable names expected by `database.py` and `auth/security.py`.

Do not commit `.env` or publish database passwords, signing secrets, or other credentials.

### 5. Prepare the database

Create the PostgreSQL database and ensure the connection details in `.env` point to it.

**Important:** The current Alembic history assumes that the original `users` and `applications` tables already exist. A complete, tested fresh-database migration path is still being finalized. Do not assume that `alembic upgrade head` alone initializes an empty database.

For an existing database, verify its schema and recorded Alembic revision before running migrations. Back up important data before any schema changes.

### 6. Run the API

```bash
uvicorn main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

## Running Tests

Configure a separate test database using `TEST_DATABASE_URL` in `.env`. Tests should run against the test database, not the main database.

Activate the virtual environment and run:

```bash
pytest -q
```

## Database Migrations

Check the current migration revision:

```bash
python -m alembic current
```

Review migration history:

```bash
python -m alembic history
```

Review every migration before applying it to a database containing important data.

## Security Notes

- Passwords are hashed rather than stored in plaintext.
- Protected endpoints require valid authentication.
- Users should only be able to access their own job applications.
- Secrets and database credentials belong in environment variables, not source control.

## Project Status

The project includes authentication, application ownership, database migration configuration, and automated tests. The test suite currently contains 31 passing tests. Fresh-database migration setup remains an improvement in progress.
