# Computer Science Daily Trivia API

A FastAPI-based REST API for serving computer science daily trivia questions with multiple choice answers. The API is secured with Auth0 and uses PostgreSQL for persistent storage.

## Overview

This API provides endpoints to fetch daily computer science trivia questions and their corresponding answers. Each question includes multiple choice options that are dynamically assigned letters (A, B, C, etc.) based on their position in the database.

### API Endpoints

#### Questions Domain (`/questions`)
- **`GET /questions/today`** - Retrieve today's trivia question
  - Returns: Question with all multiple choice options
  
- **`GET /questions/{id}`** - Retrieve a specific question by ID
  - Returns: Question with all multiple choice options

#### Answers Domain (`/answers`)
- **`GET /answers/{question_id}`** - Retrieve the answer for a specific question
  - Returns: Answer text and explanation

### Project Structure

This repository uses a **domain-driven** project structure where each functional area (domain) is self-contained:

```plaintext
src/
├── main.py                 # FastAPI application setup
├── config.py              # Application settings (Auth0)
├── database.py            # Database configuration (PostgreSQL)
├── auth/
│   ├── __init__.py
│   └── auth0.py          # Auth0 token verification
├── dependencies/
│   ├── get_db.py         # Database connection dependency
│   └── get_user.py       # Auth0 user extraction dependency
└── domains/
    ├── __init__.py
    ├── questions/        # Questions domain
    │   ├── __init__.py
    │   ├── choices_helper.py
    │   ├── get_today/
    │   │   ├── __init__.py
    │   │   └── test_get_today.py
    │   └── get_question_by_id/
    │       ├── __init__.py
    │       └── test_get_question_by_id.py
    └── answers/         # Answers domain
        ├── __init__.py
        └── get_answer_by_question_id/
            ├── __init__.py
            └── test_get_answer_by_question_id.py
```

## Setup & Configuration

### Prerequisites
- Python 3.14+
- PostgreSQL (for production)
- Auth0 account (for authentication)

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Auth0 Configuration
AUTH0_DOMAIN=your-auth0-domain.auth0.com
AUTH0_CLIENT_ID=your-auth0-client-id

# PostgreSQL Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=comp_sci_daily
```

See `.env.example` for a template.

### Installation

1. Install dependencies:
```bash
uv sync
```

2. Set up your PostgreSQL database:
```sql
CREATE TABLE questions (
    id UUID PRIMARY KEY,
    question TEXT NOT NULL,
    difficulty VARCHAR(50),
    date DATE NOT NULL
);

CREATE TABLE choices (
    id UUID PRIMARY KEY,
    question_id UUID NOT NULL REFERENCES questions(id),
    choice_text TEXT NOT NULL
);

CREATE TABLE answers (
    id UUID PRIMARY KEY,
    question_id UUID NOT NULL REFERENCES questions(id),
    answer TEXT NOT NULL,
    explanation TEXT
);
```

## Running the Application

### Development Server
Start the FastAPI development server:
```bash
uv run fastapi dev src/main.py
```

The API will be available at `http://localhost:8000`. Interactive API documentation (Swagger UI) is available at `http://localhost:8000/docs`.

### Running Tests

All tests are colocated with their respective domain endpoints. Run all tests with:

```bash
uv run pytest
```

Tests use an in-memory SQLite database and mock Auth0 authentication, so they run independently of external services.

## Authentication

All endpoints require a valid Auth0 Bearer token in the `Authorization` header:

```
Authorization: Bearer <your-auth0-token>
```

Example request:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/questions/today
```

Invalid or missing tokens will return a 401 Unauthorized response.

## Development Notes

### Architecture Decisions

1. **Domain-Driven Structure**: Each domain (questions, answers) is self-contained with its own endpoints, models, and tests. This makes it easy to locate and modify related code.

2. **Auth0 Integration**: Authentication is centralized in the `get_user` dependency, making it easy to apply to new endpoints without duplicating auth logic.

3. **Dynamic Choice Letters**: Choice letters (A, B, C, etc.) are generated dynamically based on database row order, eliminating the need to store them and ensuring consistency.

4. **PostgreSQL**: Uses PostgreSQL for reliable, scalable data storage with proper foreign key constraints.

5. **Async/Await**: All endpoints are async-first, allowing for non-blocking I/O operations with database and external services.

### Adding New Endpoints

To add a new endpoint:

1. Create a new directory under the appropriate domain: `src/domains/{domain}/{endpoint_name}/`
2. Create an `__init__.py` file with your FastAPI router and endpoint logic
3. Create a `test_{endpoint_name}.py` file with test cases
4. Import and register the router in the domain's `__init__.py`

### Database Queries

All database queries use SQLAlchemy's `text()` for raw SQL queries. To add a new query:

1. Define your SQL with named parameters (`:param_name`)
2. Pass a dictionary of parameters to `db.execute()`
3. Use `.mappings()` to convert results to dict-like objects

Example:
```python
query = text("SELECT id, question FROM questions WHERE difficulty = :difficulty")
result = db.execute(query, {"difficulty": "easy"})
rows = result.mappings().all()
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: Database ORM and query builder
- **psycopg**: PostgreSQL driver
- **pyjwt**: Additional JWT utilities
- **python-dotenv**: Environment variable loading
- **pytest**: Testing framework

my_fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── internal/
│   │   ├── __init__.py
│   │   └── admin.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   └── db/
│       ├── __init__.py
│       ├── database.py
│       └── migrations/
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_users.py
│   ├── test_items.py
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── run.sh
```

While this works for small projects, as the API grows, developers often have to keep track of multiple parallel directory structures to work on a single feature.

This repository argues for a different approach: **domains** serve as the primary organizational unit. All logic for a given domain is encapsulated within its own directory:

```plaintext
├── domains
│   ├── __init__.py
│   ├── items
│   │   ├── get_all_items
│   │   │   ├── __init__.py
│   │   │   └── test_get_all_items.py
│   │   ├── get_item_by_id
│   │   │   ├── __init__.py
│   │   │   └── test_get_item_by_id.py
│   │   └── __init__.py
│   └── orders
│       ├── get_all_orders
│       │   ├── __init__.py
│       │   └── test_get_all_orders.py
│       ├── get_order_by_id
│       │   ├── __init__.py
│       │   ├── errors.py
│       │   ├── get_order_by_id.py
│       │   ├── models.py
│       │   └── test_get_order_by_id.py
│       └── __init__.py
```

By encapsulating each endpoint in its own directory, you gain two primary benefits:

1. **Colocated Related Code**: By placing data models, business logic, unit tests, and HTTP handling in the same directory, developers no longer need to jump between distant folders to make a single functional change.
2. **Flexible Complexity**: Not every endpoint is complex. Some might simply execute a short SQL query and return a response (ex. `items` endpoints). Others might involve dynamic query building, third-party APIs, or complex authorization. This structure allows simple endpoints to exist in a single file, while complex ones can be broken down into separate files for models, business logic, and errors within the same directory (ex. `get_order_by_id`).

## When To Use This Structure (And When Not To)

I created this template repository because I was frustrated with the poor developer ergonomics of the FastAPI “best-practice” layouts found online, especially in larger codebases. This layout provides a practical balance between developer experience and organizational rigidity.

If you are building a quick proof-of-concept or a single-domain API, this structure may be overkill. However, if your API has many domains, is expected to scale, or you simply prefer that related code stay grouped together, this structure is an excellent choice.

## Testing

[Pytest](https://docs.pytest.org/en/stable/) is used for testing the API endpoints. Following the same philosophy as the rest of the repository, test case files are colocated with the code they cover.

A shared `conftest.py` overrides the `get_db` dependency, ensuring each test runs against a fresh database instance.

To run the tests:

```sh
uv run pytest
```

## Running the HTTP Server

Start the server using the following command:

```sh
uv run fastapi dev src/main.py
```
