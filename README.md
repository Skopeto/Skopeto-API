# Skopeto

## Server Monitoring Tool

Open-source server and container monitoring with SSH health checks.

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
```bash
git clone https://github.com/Skopeto/Skopeto-API.git
cd Skopeto-API
cp .env.example .env
docker compose up -d
```
Dont forget to assign vlaues to .env
Visit `http://localhost:8000`

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