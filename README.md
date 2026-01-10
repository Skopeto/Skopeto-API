# Skopeto

## Server Monitoring Tool

Open-source server and container monitoring with SSH health checks.

Built with FastAPI!

This project was born out of necessity having to monitor multiple containers in different servers  
and having to sometimes debug the server resources themselves  
its my plan to also add database health check analysis, container management  
and different methods of monitoring not just SSH

Front-End is Vue, however, with me not being a front end developer,  
it's there to just serve only one purpose and that is to provide an interface for our API  
you will find the UI in https://github.com/Skopeto/Skopeto-UI.git (dont judge me pls)

Other technologies that I make use of, some critical and some not so much are Docker, SSH, uv package manager,  
and of course the nice, lightweight image of Postgres.

![GitHub stars](https://img.shields.io/github/stars/Skopeto/Skopeto-API)
![License](https://img.shields.io/badge/license-AGPL--3.0-blue)

## Features

- 🖥️ SSH-based server monitoring (CPU, RAM, Disk)
- 🐳 Container health checks (ssh shell commands "docker ps -a")
- 📊 Real-time dashboards
- 🔔 Alert notifications - coming soon
- 🔐 Multi-user authentication (JWT)
- 🗄️ Supports PostgreSQL, MySQL, Oracle / i will provide schema dumps for them however repository implementations and dbConn are up to you.

## Quick Start (Self-Hosted)

### Prerequisites
- Docker and Docker Compose installed
- Git

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/Skopeto/Skopeto-API.git
cd Skopeto-API
```

2. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` and configure:
```
DB_USER=servermonitor
DB_PASSWORD=your-secure-password
DB_NAME=servermonitor
DB_HOST=postgres-db
DB_PORT=5432
SECRET_KEY=your-secret-key-here
```

3. **Start the application**
```bash
docker compose up -d
```

4. **Initialize database schema**
```bash
docker exec -i servermonitor_postgres psql -U servermonitor -d servermonitor < sql/schema.sql
```

5. **Verify installation**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Managing the Application

**View logs**
```bash
docker compose logs -f
```

**Stop the application**
```bash
docker compose down
```

**Reset database**
```bash
docker compose down -v
docker compose up -d
docker exec -i servermonitor_postgres psql -U servermonitor -d servermonitor < sql/schema.sql
```
## Tests
```bash
uv run python -m pytest tests/
```

## Documentation
- [API Documentation](docs/api.md)

## Managed Hosting ☁️

Don't want to manage infrastructure?
contact me

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

AGPL-3.0 - see [LICENSE](LICENSE)

**Commercial licensing available** - contact johnlesis91@gmail.com

## Author
Built by [Fatjon Lleshi] (https://www.linkedin.com/in/giannis-l-117b08196/)

⭐ Star us on GitHub if you find this useful!
