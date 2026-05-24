# Computer Science Daily

A daily computer science trivia application that tests your knowledge with fresh questions every day. Built with FastAPI, React, PostgreSQL, and Auth0.

## Features

- **Daily Trivia Questions** - Get a new computer science question each day
- **Multiple Difficulty Levels** - Easy, Medium, and Hard questions
- **User Authentication** - Secure login via Auth0

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM for database operations
- **Auth0** - Authentication and authorization
- **Uvicorn** - ASGI server

### Frontend
- **Vue.js** - UI framework
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
   cp .env.docker .env
   ```
   
   Update `.env` with your Auth0 credentials:
   ```env
   AUTH0_DOMAIN=your-auth0-domain.auth0.com
   AUTH0_AUDIENCE=your-auth0-audience
   ```

3. **Start the development environment**
   ```bash
   docker-compose up -d
   ```

4. **Start the frontend**
   ```bash
   cd client
   pnpm i
   pnpm dev
   ```

The application will be available at:
- **API**: http://localhost:8000
- **Frontend**: http://localhost:5173

### Development

The Docker Compose setup includes:
- **PostgreSQL** - Database with automatic initialization
- **FastAPI** - API server with hot reload enabled
- **Caddy** - Reverse proxy on port 8000

Any changes to files in `server/src/` will automatically reload the FastAPI application.

## Database

The application uses PostgreSQL with the following main tables:
- **questions** - Trivia questions with difficulty levels
- **choices** - Multiple choice options for questions
- **answers** - Correct answers with explanations
