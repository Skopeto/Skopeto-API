# Server Monitoring Tool

Open-source server and container monitoring with SSH and HTTP health checks.

![GitHub stars](https://img.shields.io/github/stars/you/monitoring-tool)
![License](https://img.shields.io/badge/license-AGPL--3.0-blue)

## Features

- 🖥️ SSH-based server monitoring (CPU, RAM, Disk)
- 🐳 Container health checks (HTTP/HTTPS)
- 📊 Real-time dashboards
- 🔔 Alert notifications
- 🔐 Multi-user authentication (JWT)
- 🗄️ Supports PostgreSQL, MySQL, Oracle

## Quick Start (Self-Hosted)
```bash
git clone https://github.com/you/monitoring-tool
cd monitoring-tool
cp .env.example .env
docker compose up -d
```

Visit `http://localhost:8000`

## Documentation

- [Installation Guide](docs/installation.md)
- [Configuration](docs/configuration.md)
- [API Documentation](docs/api.md)

## Managed Hosting ☁️

Don't want to manage infrastructure?

**Try our managed cloud version:**
- ✅ Automatic updates
- ✅ Backups included
- ✅ Priority support

**Pricing:**
- $40/month
- Enterprise: Custom pricing

## Self-Hosting vs Managed

| Feature | Self-Hosted (Free) | Managed Cloud |
|---------|-------------------|---------------|
| Price   | Free              | $29-99/month  |
| Updates | Manual            | Automatic |
| Backups | You manage        | Included |
| Support | Community         | Priority |

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

AGPL-3.0 - see [LICENSE](LICENSE)

**Commercial licensing available** - contact sales@yourapp.com

## Author

Built by [Fatjon Lleshi] (https://www.linkedin.com/in/giannis-l-117b08196/)

⭐ Star us on GitHub if you find this useful!