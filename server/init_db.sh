#!/bin/bash
# PostgreSQL Database Initialization Script
# Initializes the Computer Science Daily Trivia database

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Load environment variables from .env if it exists
if [ -f ./../.env ]; then
    set -a
    source ./../.env
    set +a
fi

# Use environment variables or defaults
DB_HOST=localhost # ${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-}
DB_NAME=${DB_NAME:-comp_sci_daily}

echo -e "${YELLOW}PostgreSQL Database Initialization${NC}"
echo "Database: $DB_NAME"
echo "Host: $DB_HOST"
echo "Port: $DB_PORT"
echo "User: $DB_USER"
echo ""

# Check if psql is available
if ! command -v psql &> /dev/null; then
    echo -e "${RED}Error: psql is not installed. Please install PostgreSQL client tools.${NC}"
    exit 1
fi

# Export the password for psql
export PGPASSWORD=$DB_PASSWORD

# Check if database exists
if psql -h "$DB_HOST" -U "$DB_USER" -d postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1; then
    echo -e "${YELLOW}Database '$DB_NAME' already exists.${NC}"
    read -p "Do you want to drop and recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Dropping database...${NC}"
        psql -h "$DB_HOST" -U "$DB_USER" -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"
    else
        echo -e "${YELLOW}Keeping existing database. Applying schema...${NC}"
        psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -f init_db.sql
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Schema applied successfully!${NC}"
        else
            echo -e "${RED}Failed to apply schema.${NC}"
            exit 1
        fi
        exit 0
    fi
fi

# Create database
echo -e "${YELLOW}Creating database '$DB_NAME'...${NC}"
psql -h "$DB_HOST" -U "$DB_USER" -d postgres -c "CREATE DATABASE $DB_NAME;"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Database created successfully.${NC}"
else
    echo -e "${RED}Failed to create database.${NC}"
    exit 1
fi

# Run initialization script
echo -e "${YELLOW}Initializing database schema...${NC}"
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -f init_db.sql

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Database initialized successfully!${NC}"
    echo ""
    echo -e "${GREEN}Summary:${NC}"
    echo "  ✓ Database created: $DB_NAME"
    echo "  ✓ Tables created: questions, choices, answers, users, user_answers"
    echo "  ✓ Indexes created for optimized queries"
    echo "  ✓ View created: user_stats"
else
    echo -e "${RED}Failed to initialize database.${NC}"
    exit 1
fi

# Unset password variable
unset PGPASSWORD
