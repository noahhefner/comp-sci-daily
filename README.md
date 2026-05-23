# Computer Science Daily

A daily computer science trivia application that tests your knowledge with fresh questions every day. Built with FastAPI, React, PostgreSQL, and Auth0.

## Features

- **Daily Trivia Questions** - Get a new computer science question each day
- **Multiple Difficulty Levels** - Easy, Medium, and Hard questions
- **User Authentication** - Secure login via Auth0
- **Progress Tracking** - Track your answers and accuracy over time
- **Analytics** - View your performance statistics and streaks

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM for database operations
- **Auth0** - Authentication and authorization
- **Uvicorn** - ASGI server

### Frontend
- **React** - UI framework
- **TypeScript** - Type-safe JavaScript

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Local development orchestration
- **Caddy** - Reverse proxy and web server

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Auth0 account and credentials

### Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd comp-sci-daily
   ```

2. **Configure environment variables**
   ```bash
   cp server/.env.example server/.env
   ```
   
   Update `server/.env` with your Auth0 credentials:
   ```env
   AUTH0_DOMAIN=your-auth0-domain.auth0.com
   AUTH0_CLIENT_ID=your-auth0-client-id
   AUTH0_CLIENT_SECRET=your-auth0-client-secret
   DB_USER=comp_sci_user
   DB_PASSWORD=comp_sci_password
   DB_NAME=comp_sci_daily
   ```

3. **Start the development environment**
   ```bash
   docker-compose up
   ```

   The application will be available at:
   - **API**: http://localhost:8000
   - **Frontend**: http://localhost:3000 (if running separately)

### Development

The Docker Compose setup includes:
- **PostgreSQL** - Database with automatic initialization
- **FastAPI** - API server with hot reload enabled
- **Caddy** - Reverse proxy on port 8000

Any changes to files in `server/src/` will automatically reload the FastAPI application.

## Project Structure

```
comp-sci-daily/
├── server/                 # FastAPI backend
│   ├── src/
│   │   ├── auth/          # Auth0 authentication
│   │   ├── domains/       # Domain models
│   │   ├── dependencies/  # FastAPI dependencies
│   │   ├── main.py        # Application entry point
│   │   ├── config.py      # Settings
│   │   └── database.py    # Database configuration
│   ├── init_db.sql        # Database initialization script
│   ├── Dockerfile         # Backend container image
│   └── pyproject.toml     # Python dependencies
├── client/                # React frontend
├── docker-compose.yml     # Development environment
├── Caddyfile             # Reverse proxy configuration
└── README.md             # This file
```

## API Endpoints

### Authentication
- `GET /auth/login` - Initiate Auth0 login
- `GET /auth/callback` - Auth0 callback endpoint

### Trivia
- `GET /questions/today` - Get today's question
- `POST /questions/answer` - Submit an answer
- `GET /questions/{id}` - Get a specific question

### User
- `GET /user/stats` - Get user statistics
- `GET /user/history` - Get answer history

## Database

The application uses PostgreSQL with the following main tables:
- **questions** - Trivia questions with difficulty levels
- **choices** - Multiple choice options for questions
- **answers** - Correct answers with explanations
- **users** - User accounts (Auth0 integration)
- **user_answers** - User responses and tracking

Initial sample data includes 3 questions across different difficulty levels.

## Environment Variables

### Required
- `AUTH0_DOMAIN` - Your Auth0 domain
- `AUTH0_CLIENT_ID` - Auth0 application client ID
- `AUTH0_CLIENT_SECRET` - Auth0 application client secret

### Database
- `DB_HOST` - Database host (default: postgres)
- `DB_PORT` - Database port (default: 5432)
- `DB_USER` - Database username
- `DB_PASSWORD` - Database password
- `DB_NAME` - Database name

## Development Commands

### Start the application
```bash
docker-compose up
```

### Stop the application
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f api
docker-compose logs -f postgres
```

### Rebuild containers
```bash
docker-compose up --build
```

## Testing

Run tests for the backend:
```bash
docker-compose exec api pytest
```

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
