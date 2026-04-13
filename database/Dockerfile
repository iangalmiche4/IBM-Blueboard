# PostgreSQL Database for IBM Blueboard
FROM postgres:18-alpine

# Copy initialization scripts
# These will be executed in alphabetical order on first container start
COPY init/*.sql /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432

# Note: Database credentials are provided by docker-compose.yml
# via environment variables from the .env file at project root