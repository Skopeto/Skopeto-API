# API Documentation

## Overview

The Skopeto Server Monitoring API provides endpoints for managing server monitoring, container tracking, and user authentication. All endpoints return JSON responses.

## Base URL

```
http://localhost:8000
```

## Authentication

Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

## Response Format

All successful responses follow this format:

```json
{
  "status": "success",
  "data": { ... }
}
```

Error responses include:

```json
{
  "error": "Error message description"
}
```

---

## Authentication Endpoints

### Register User

Register a new user account.

**Endpoint:** `POST /auth/register`

**Authentication:** Not required

**Request Body:**

```json
{
  "user_name": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "user_type": "admin"
}
```

**Field Validations:**
- `user_name`: 3-50 characters
- `first_name`: 1-50 characters
- `last_name`: 1-50 characters
- `email`: Valid email format
- `password`: Minimum 6 characters
- `user_type`: One of: `"superadmin"`, `"admin"`, `"user"`

**Response (201 Created):**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "user_name": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "roles": ["admin"],
    "is_active": true,
    "is_superuser": false
  }
}
```

**Note:** The response doesnt include the `hashed_password` field (Argon2 hash).

---

### Login

Authenticate and receive an access token.

**Endpoint:** `POST /auth/login`

**Authentication:** Not required

**Request Body:**

```json
{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**

```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_at": "2025-12-27T15:30:00",
    "user_id": 1
  }
}
```

**Error Response (401 Unauthorized):**

```json
{
  "error": "Invalid credentials"
}
```

---

## Server Endpoints

### Create Server

Register a new server for monitoring.

**Endpoint:** `POST /servers`

**Authentication:** Required

**Request Body:**

```json
{
  "registrator_id": 1,
  "name": "root",
  "password": "serverPassword123",
  "ip_address": "192.168.1.100",
  "port": 22,
  "status": "inactive"
}
```

**Field Details:**
- `registrator_id`: Must match the authenticated user's ID
- `name`: SSH username for the server
- `password`: SSH password (will be encrypted)
- `ip_address`: IPv4 or IPv6 address
- `port`: SSH port (typically 22)
- `status`: One of: `"up"`, `"down"`, `"decommissioned"`, `"inactive"`

**Response (201 Created):**

```json
{
  "status": "success",
  "data": {
    "id": 5,
    "user_name": "root",
    "ip_address": "192.168.1.100",
    "port": 22,
    "status": "inactive"
  }
}
```

**Note:** For security, the `ssh_password_encrypted` field is **not included** in API responses.

**Error Response (403 Forbidden):**

```json
{
  "error": "Cannot register server for another user"
}
```

---

### List Servers

Retrieve all registered servers.

**Endpoint:** `GET /servers`

**Authentication:** Required

**Response (200 OK):**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "user_name": "root",
      "ip_address": "192.168.1.100",
      "port": 22,
      "status": "up"
    },
    {
      "id": 2,
      "user_name": "admin",
      "ip_address": "192.168.1.101",
      "port": 22,
      "status": "down"
    }
  ]
}
```

**Note:** For security, the `ssh_password_encrypted` field is **not included** in API responses.

---

### Collect Container Metrics

Actively collect real-time health metrics and container data for a specific server.

**Endpoint:** `POST /containers/{server_id}/collect`

**Authentication:** Required

**Path Parameters:**
- `server_id`: Integer ID of the server

**Example:** `POST /containers/1/collect`

**Response (200 OK):**

```json
{
  "status": "success",
  "data": {
    "server": {
      "id": 1,
      "user_name": "root",
      "ip_address": "192.168.1.100",
      "port": 22,
      "status": "up"
    },
    "current_health": {
      "id": 42,
      "server_id": 1,
      "status": "healthy",
      "cpu_usage": 45.2,
      "memory_usage": 62.8,
      "disk_usage": 78.5,
      "uptime": "15 days, 3:24:10",
      "checked_at": "2025-12-26T15:30:00Z"
    },
    "containers": [
      {
        "id": 1,
        "server_id": 1,
        "container_id": "a1b2c3d4e5f6",
        "name": "servermonitor_api",
        "image": "python:3.12-slim",
        "status": "running",
        "ports": "0.0.0.0:8000->8000/tcp",
        "exit_code": null,
        "state_changed_at": "2025-12-26T10:00:00Z",
        "is_healthy": true,
        "last_seen_at": "2025-12-26T15:30:00Z",
        "created_at": "2025-12-25T08:00:00Z",
        "updated_at": "2025-12-26T15:30:00Z"
      }
    ]
  }
}
```

**Health Status Values:**
- `"healthy"`: Server is operational
- `"unhealthy"`: Server metrics exceed thresholds
- `"offline"`: Server is unreachable
- `"error"`: Error occurred during health check

**Notes:**
- This endpoint actively collects fresh metrics from the server via SSH
- Server health metrics are collected and persisted to the database
- Container metrics are only collected if the server is healthy
- Use `GET /containers` to retrieve stored data without triggering new collection

**Error Response (404 Not Found):**

```json
{
  "error": "Server not found"
}
```

---

### Collect All Monitoring Data

Trigger collection of complete monitoring data for all servers (health, containers, and databases).

**Endpoint:** `POST /monitoring/collect`

**Authentication:** Required

**Response (200 OK):**

```json
{
  "status": "success",
  "data": [
    {
      "server": {
        "id": 1,
        "user_name": "root",
        "ip_address": "192.168.1.100",
        "port": 22,
        "status": "up"
      },
      "current_health": {
        "id": 42,
        "server_id": 1,
        "status": "healthy",
        "cpu_usage": 45.2,
        "memory_usage": 62.8,
        "disk_usage": 78.5,
        "uptime": "15 days, 3:24:10",
        "checked_at": "2025-12-26T15:30:00Z"
      },
      "containers": [
        {
          "id": 1,
          "server_id": 1,
          "container_id": "a1b2c3d4e5f6",
          "name": "servermonitor_api",
          "image": "python:3.12-slim",
          "status": "running",
          "ports": "0.0.0.0:8000->8000/tcp",
          "exit_code": null,
          "state_changed_at": "2025-12-26T10:00:00Z",
          "is_healthy": true,
          "last_seen_at": "2025-12-26T15:30:00Z",
          "created_at": "2025-12-25T08:00:00Z",
          "updated_at": "2025-12-26T15:30:00Z"
        }
      ]
    }
  ]
}
```

**Notes:**
- This endpoint actively collects fresh metrics from all servers concurrently using asyncio.gather
- Returns an array of server monitoring results, each containing the full server object, current health metrics, and associated containers
- Failed servers are logged but excluded from results (only successful collections are returned)
- Use this endpoint to update the database with the latest metrics

---

### List All Containers

Retrieve all servers with their current health status and associated containers.

**Endpoint:** `GET /containers`

**Authentication:** Required

**Response (200 OK):**

```json
{
  "status": "success",
  "data": [
    {
      "server": {
        "id": 1,
        "user_name": "root",
        "ip_address": "192.168.1.100",
        "port": 22,
        "status": "up"
      },
      "server_health": {
        "id": 42,
        "server_id": 1,
        "status": "healthy",
        "cpu_usage": 45.2,
        "memory_usage": 62.8,
        "disk_usage": 78.5,
        "uptime": "15 days, 3:24:10",
        "checked_at": "2025-12-26T15:30:00Z"
      },
      "containers": [
        {
          "id": 1,
          "server_id": 1,
          "container_id": "a1b2c3d4e5f6",
          "name": "servermonitor_api",
          "image": "python:3.12-slim",
          "status": "running",
          "ports": "0.0.0.0:8000->8000/tcp",
          "exit_code": null,
          "state_changed_at": "2025-12-26T10:00:00Z",
          "is_healthy": true,
          "last_seen_at": "2025-12-26T15:30:00Z",
          "created_at": "2025-12-25T08:00:00Z",
          "updated_at": "2025-12-26T15:30:00Z"
        }
      ]
    },
    {
      "server": {
        "id": 2,
        "user_name": "admin",
        "ip_address": "192.168.1.101",
        "port": 22,
        "status": "down"
      },
      "current_health": null,
      "containers": []
    }
  ]
}
```

**Notes:**
- Returns all servers with their most recent health status from the database
- `server_health` can be `null` if no health check has been performed yet
- `containers` array will be empty if no containers exist on the server
- This endpoint does NOT trigger new health checks - it returns stored data from the database
- **Important:** May include containers that have been deleted but not yet removed from the database
- Containers are identified by `name` (not `container_id`) to handle container restarts correctly
- When a container is stopped and restarted, Docker assigns a new container_id but keeps the same name
- Use `POST /monitoring/collect` to trigger fresh metrics collection and update the database

---

### Update Server

Update server information with partial updates.

**Endpoint:** `PATCH /servers/{server_id}`

**Authentication:** Required

**Path Parameters:**
- `server_id`: Integer ID of the server to update

**Request Body:**

All fields are optional - only provide the fields you want to update:

```json
{
  "name": "root",
  "password": "newPassword123",
  "ip_address": "192.168.1.150",
  "port": 2222,
  "status": "up"
}
```

**Field Details:**
- `name`: SSH username for the server (optional)
- `password`: SSH password - will be encrypted (optional)
- `ip_address`: IPv4 or IPv6 address (optional)
- `port`: SSH port (optional)
- `status`: One of: `"up"`, `"down"`, `"decommissioned"`, `"inactive"` (optional)

**Response (200 OK):**

```json
{
  "status": "success",
  "data": {
    "id": 5,
    "user_name": "root",
    "ip_address": "192.168.1.150",
    "port": 2222,
    "status": "up"
  }
}
```

**Note:**
- For security, the `ssh_password_encrypted` field is **not included** in API responses.
- When providing a password, send the plaintext password - it will be encrypted before storage.

**Error Response (404 Not Found):**

```json
{
  "error": "Server 5 not found"
}
```

---

### Delete Server

Delete a registered server.

**Endpoint:** `DELETE /servers/{server_id}`

**Authentication:** Required

**Path Parameters:**
- `server_id`: Integer ID of the server to delete

**Example:** `DELETE /servers/5`

**Response (200 OK):**

```json
{
  "status": "success"
}
```

**Error Response (404 Not Found):**

```json
{
  "error": "Server not found"
}
```

---

## Database Endpoints

### Get Database Health

Retrieve all servers with their databases and current health metrics.

**Endpoint:** `GET /databases/health`

**Authentication:** Required

**Response (200 OK):**

```json
{
  "status": "success",
  "data": [
    {
      "server": {
        "id": 1,
        "user_name": "root",
        "ip_address": "192.168.1.100",
        "port": 22,
        "status": "up"
      },
      "current_health": {
        "id": 42,
        "server_id": 1,
        "status": "healthy",
        "cpu_usage": 45.2,
        "memory_usage": 62.8,
        "disk_usage": 78.5,
        "uptime": "15 days, 3:24:10",
        "checked_at": "2025-12-26T15:30:00Z"
      },
      "databases": [
        {
          "database": {
            "id": 1,
            "server_id": 1,
            "database_type": "postgresql",
            "name": "production_db",
            "host": "192.168.1.100",
            "port": 5432,
            "username": "dbuser"
          },
          "health": {
            "status": "healthy",
            "connection_count": 15,
            "response_time_ms": 12.5,
            "checked_at": "2025-12-26T15:30:00Z"
          }
        }
      ]
    }
  ]
}
```

**Notes:**
- This endpoint actively collects fresh database health metrics
- Includes server health information along with database-specific metrics
- Used for database monitoring dashboard refresh

---

### Create Database

Register a new database for monitoring.

**Endpoint:** `POST /databases`

**Authentication:** Required

**Request Body:**

```json
{
  "server_id": 1,
  "database_type": "postgresql",
  "name": "production_db",
  "host": "192.168.1.100",
  "port": 5432,
  "username": "dbuser",
  "password": "dbpassword"
}
```

**Field Details:**
- `server_id`: ID of the server where the database resides
- `database_type`: One of: `"postgresql"`, `"mysql"`, `"mongodb"`, etc.
- `name`: Database name
- `host`: Database host address
- `port`: Database port
- `username`: Database username
- `password`: Database password (will be encrypted)

**Response (200 OK):**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "server_id": 1,
    "database_type": "postgresql",
    "name": "production_db",
    "host": "192.168.1.100",
    "port": 5432,
    "username": "dbuser"
  }
}
```

**Note:** For security, the password is **not included** in API responses.

---

### Update Database

Update database configuration with partial updates.

**Endpoint:** `PATCH /databases/{database_id}`

**Authentication:** Required

**Path Parameters:**
- `database_id`: Integer ID of the database to update

**Request Body:**

All fields are optional - only provide the fields you want to update:

```json
{
  "name": "production_db_v2",
  "port": 5433,
  "username": "new_dbuser",
  "password": "newpassword"
}
```

**Response (200 OK):**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "server_id": 1,
    "database_type": "postgresql",
    "name": "production_db_v2",
    "host": "192.168.1.100",
    "port": 5433,
    "username": "new_dbuser"
  }
}
```

---

### Delete Database

Delete a database from monitoring.

**Endpoint:** `DELETE /databases/{database_id}`

**Authentication:** Required

**Path Parameters:**
- `database_id`: Integer ID of the database to delete

**Example:** `DELETE /databases/1`

**Response (200 OK):**

```json
{
  "status": "success",
  "data": "Database 1 deleted successfully"
}
```

**Error Response (404 Not Found):**

```json
{
  "error": "Database not found"
}
```

---

## Error Handling

### Common HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: Authenticated but not authorized
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

### Validation Errors

Validation errors return details about which fields failed validation:

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## Rate Limiting

Currently, there are no rate limits enforced. This may change in future versions.

---

## Examples

### Complete Authentication Flow

**1. Register a new user:**

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "user_type": "admin"
  }'
```

**2. Login to get access token:**

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

**3. Use token to create a server:**

```bash
curl -X POST http://localhost:8000/servers \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "registrator_id": 1,
    "name": "root",
    "password": "serverPassword123",
    "ip_address": "192.168.1.100",
    "port": 22,
    "status": "inactive"
  }'
```

**4. List all servers:**

```bash
curl -X GET http://localhost:8000/servers \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**5. Collect container metrics for a server:**

```bash
curl -X POST http://localhost:8000/containers/1/collect \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**6. List all containers:**

```bash
curl -X GET http://localhost:8000/containers \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**7. Update server:**

```bash
curl -X PATCH http://localhost:8000/servers/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "port": 2222,
    "status": "up"
  }'
```

**8. Delete server:**

```bash
curl -X DELETE http://localhost:8000/servers/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**9. Collect all monitoring data:**

```bash
curl -X POST http://localhost:8000/monitoring/collect \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**10. Get database health:**

```bash
curl -X GET http://localhost:8000/databases/health \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**11. Create database:**

```bash
curl -X POST http://localhost:8000/databases \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "server_id": 1,
    "database_type": "postgresql",
    "name": "production_db",
    "host": "192.168.1.100",
    "port": 5432,
    "username": "dbuser",
    "password": "dbpassword"
  }'
```

**12. Update database:**

```bash
curl -X PATCH http://localhost:8000/databases/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "port": 5433,
    "username": "new_dbuser"
  }'
```

**13. Delete database:**

```bash
curl -X DELETE http://localhost:8000/databases/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Notes

- All timestamps are in ISO 8601 format
- SSH passwords are encrypted before storage
- Server metrics are collected via SSH commands
- Container data is retrieved using `docker ps -a` via SSH
- The scheduler automatically collects metrics at configured intervals
