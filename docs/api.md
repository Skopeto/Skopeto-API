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
    "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$...",
    "roles": ["admin"],
    "is_active": true,
    "is_superuser": false
  }
}
```

**Note:** The response includes the `hashed_password` field (Argon2 hash).

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

### Register Server

Register a new server for monitoring.

**Endpoint:** `POST /servers/register`

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

### Get All Servers

Retrieve all registered servers.

**Endpoint:** `GET /servers/all-servers`

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

### Get Server Health

Get real-time health metrics for a specific server.

**Endpoint:** `GET /servers/monitoring/{server_id}`

**Authentication:** Required

**Path Parameters:**
- `server_id`: Integer ID of the server

**Example:** `GET /servers/monitoring/1`

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

**Error Response (404 Not Found):**

```json
{
  "error": "Server not found"
}
```

---

### Collect All Monitoring Data

Trigger collection of metrics from all registered servers and their containers.

**Endpoint:** `GET /servers/monitoring/collect-all`

**Authentication:** Required (typically used by scheduled tasks)

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

**Note:** Returns an array of server monitoring results, each containing the full server object, current health metrics, and associated containers.

---

### Get All Servers with Containers

Retrieve all servers with their current health status and associated containers.

**Endpoint:** `GET /servers/containers/all`

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
- `current_health` can be `null` if no health check has been performed yet
- `containers` array will be empty if no containers exist on the server
- This endpoint does NOT trigger new health checks - it returns stored data
- **Important:** May include containers that have been deleted but not yet removed from the database
- Containers are identified by `name` (not `container_id`) to handle container restarts correctly
- When a container is stopped and restarted, Docker assigns a new container_id but keeps the same name
- Use `GET /servers/monitoring/collect-all` to trigger fresh metrics collection and update the database

---

### Edit Server

Update server information with partial updates.

**Endpoint:** `PATCH /servers/edit/{server_id}`

**Authentication:** Required

**Path Parameters:**
- `server_id`: Integer ID of the server to edit

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

**Endpoint:** `DELETE /servers/delete/{server_id}`

**Authentication:** Required

**Path Parameters:**
- `server_id`: Integer ID of the server to delete

**Example:** `DELETE /servers/delete/5`

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

## Container Endpoints

### Get Container Data

Retrieve Docker container information from a specific server.

**Endpoint:** `POST /containers/get-container-data`

**Authentication:** Required

**Request Body:**

```json
{
  "server_id": 1
}
```

**Response (200 OK):**

```json
{
  "status": "success",
  "data": [
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
    },
    {
      "id": 2,
      "server_id": 1,
      "container_id": "f6e5d4c3b2a1",
      "name": "servermonitor_postgres",
      "image": "postgres:16-alpine",
      "status": "running",
      "ports": "0.0.0.0:5432->5432/tcp",
      "exit_code": null,
      "state_changed_at": "2025-12-26T10:00:00Z",
      "is_healthy": true,
      "last_seen_at": "2025-12-26T15:30:00Z",
      "created_at": "2025-12-25T08:00:00Z",
      "updated_at": "2025-12-26T15:30:00Z"
    }
  ]
}
```

**Container Status Values:**
The `status` field can have various values based on Docker container states:
- `"running"`: Container is currently running
- `"exited"`: Container has stopped
- `"paused"`: Container is paused
- `"restarting"`: Container is restarting
- `"dead"`: Container is dead
- `"created"`: Container created but not started

**Error Response (404 Not Found):**

```json
{
  "error": "Server not found"
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

**3. Use token to register a server:**

```bash
curl -X POST http://localhost:8000/servers/register \
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

**4. Get server health:**

```bash
curl -X GET http://localhost:8000/servers/monitoring/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**5. Get container data:**

```bash
curl -X POST http://localhost:8000/containers/get-container-data \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "server_id": 1
  }'
```

**6. Edit server:**

```bash
curl -X PATCH http://localhost:8000/servers/edit/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "port": 2222,
    "status": "up"
  }'
```

**7. Delete server:**

```bash
curl -X DELETE http://localhost:8000/servers/delete/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**8. Collect all monitoring data:**

```bash
curl -X GET http://localhost:8000/servers/monitoring/collect-all \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**9. Get all servers with containers:**

```bash
curl -X GET http://localhost:8000/servers/containers/all \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Notes

- All timestamps are in ISO 8601 format
- SSH passwords are encrypted before storage
- Server metrics are collected via SSH commands
- Container data is retrieved using `docker ps -a` via SSH
- The scheduler automatically collects metrics at configured intervals
