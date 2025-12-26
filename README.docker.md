# Docker Setup Guide

## Prerequisites

- Docker installed on your system
- Docker Compose installed

## Quick Start

1. **Copy the environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Update the `.env` file with your configuration:**
   - Set a strong `JWT_SECRET_KEY`
   - Adjust database credentials if needed

3. **Start the services:**
   ```bash
   docker-compose up -d
   ```

4. **Check service status:**
   ```bash
   docker-compose ps
   ```

5. **View logs:**
   ```bash
   # All services
   docker-compose logs -f

   # Specific service
   docker-compose logs -f api
   docker-compose logs -f oracle-db
   ```

6. **Initialize the database:**

   Wait for Oracle to be fully initialized (first startup takes 2-3 minutes), then run:
   ```bash
   docker exec -it servermonitor_oracle sqlplus system/OraclePassword123@XEPDB1 @/docker-entrypoint-initdb.d/startup/schema.sql
   ```

7. **Access the application:**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Oracle EM Express: https://localhost:5500/em

## Services

### API Service
- **Container:** servermonitor_api
- **Port:** 8000
- **Auto-reload:** Enabled in development

### Oracle Database Service
- **Container:** servermonitor_oracle
- **Ports:** 1521 (database), 5500 (EM Express)
- **Default Credentials:**
  - User: system
  - Password: OraclePassword123
  - Service: XEPDB1

## Common Commands

### Stop services
```bash
docker-compose down
```

### Stop and remove volumes (CAUTION: deletes database data)
```bash
docker-compose down -v
```

### Rebuild services
```bash
docker-compose up -d --build
```

### Access API container shell
```bash
docker exec -it servermonitor_api bash
```

### Access Oracle container shell
```bash
docker exec -it servermonitor_oracle bash
```

### Run SQL commands
```bash
docker exec -it servermonitor_oracle sqlplus system/OraclePassword123@XEPDB1
```

## Troubleshooting

### Oracle database not starting
- First startup takes 2-3 minutes to initialize
- Check logs: `docker-compose logs oracle-db`
- Ensure you have enough disk space (min 2GB)

### API cannot connect to database
- Wait for Oracle health check to pass: `docker-compose ps`
- Verify database is running: `docker-compose logs oracle-db`
- Check connection string in `.env` file

### Port conflicts
If ports 8000, 1521, or 5500 are already in use, modify the port mappings in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Change 8001 to any available port
```

## Production Deployment

For production:

1. **Update environment variables:**
   - Set a strong `JWT_SECRET_KEY`
   - Use a stronger `DB_PASSWORD`
   - Set `DB_THICK_MODE=true` if needed

2. **Remove development features:**
   - Remove `--reload` from the API command in docker-compose.yml
   - Remove volume mount for `./app` directory

3. **Use proper secrets management:**
   - Use Docker secrets or environment variable injection
   - Never commit `.env` files to version control

4. **Set up proper networking:**
   - Use reverse proxy (nginx/traefik)
   - Enable HTTPS
   - Configure firewall rules
