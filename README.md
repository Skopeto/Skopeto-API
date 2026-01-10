# Skopeto
## Server Monitoring Tool
🚀 **Open-Source Server & Container Monitoring (Built with FastAPI)**

Skopeto was built to answer a simple question:

**“What’s actually happening on my servers, containers, and databases — without me having to manually SSH into each server — and how do I know when something breaks?”**

It came from real-world pain.
Managing multiple servers, running containers across environments, and debugging resource issues often meant constantly logging into machines just to understand what was going on.

Skopeto aims to centralize that visibility into a single, **lightweight, self-hosted platform** — giving developers clear insights, automated health checks, and alerts **without agents, unnecessary complexity, or heavy overhead**.

---

### 🧭 How Skopeto Works (From a User’s Perspective)

### 1️⃣ Register a Server

Users add their server via SSH. Once registered, Skopeto collects key system metrics through a scheduler or manual refresh, including:

* 🧠 CPU usage
* 💾 Memory usage
* 🗄️ Disk usage
* ⏳ Server uptime
* ✅ Overall health status

---

### 2️⃣ Monitor Containers

For each server, Skopeto detects and tracks running Docker containers:

* Container status (running / stopped / exited)
* Health state
* Image & exposed ports
* Exit codes
* Last seen & state change timestamps

This makes it easy to spot unhealthy or repeatedly restarting containers before they become incidents.

---

### 3️⃣ Register Databases

Users can attach databases to a server using connection credentials and monitor:

* Connection health
* Active connection count
* Query / response time
* Overall database status

These are currently **basic checks**, with the goal of evolving this much further over time.

---

### 4️⃣ Subscribe to Notifications

Once resources are registered, users can add notification subscribers:

* 📬 Email
* 💬 Slack via webhooks (still being tested)
* 🔔 In-app notifications (per logged-in user)

When the scheduler runs and detects issues, alerts are sent automatically.
Slack and email alerts go to **all subscribers**, while in-app alerts are user-specific.

---

### 5️⃣ Automated Monitoring via Scheduler

Skopeto runs a scheduler every **30 minutes** to perform health checks across all registered resources.

This is intended as a **fire-and-forget** feature.
For real-time insights, users can manually refresh data in the app.

Skopeto is designed to be **lightweight and agentless** — no software is installed on the monitored servers. Whether this fits your needs depends on your specific use case.

---

### ➡️ What’s Next

* Configurable scheduler intervals
* More advanced database health checks
* Basic container management (restart / stop / start)
* Remote command execution per server

---

### ⚙️ Tech Stack

* **Backend:** FastAPI
* **Frontend:** Vue (API-first UI, purely to serve the API 😄)
* **Infrastructure:** Docker, SSH
* **Database:** PostgreSQL (lightweight image — more support planned)
* **Authentication:** JWT

---

Skopeto is still in its infancy and actively evolving, but the goal is clear:

**A simple, extensible, self-hosted monitoring platform — built by a developer, for developers.**

⭐ If this resonates, feel free to check it out, try it, or star the repo. Feedback is more than welcome.

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


