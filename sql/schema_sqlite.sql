-- ============================================
-- SERVER MONITOR - SQLITE DATABASE SCHEMA
-- ============================================

-- Enable foreign key support (required for SQLite)
PRAGMA foreign_keys = ON;

-- ============================================
-- TABLES
-- ============================================

-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    user_name TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    roles TEXT NOT NULL,
    is_active INTEGER DEFAULT 1 NOT NULL CHECK (is_active IN (0, 1)),
    is_superuser INTEGER DEFAULT 0 NOT NULL CHECK (is_superuser IN (0, 1)),
    created_at TEXT DEFAULT (datetime('now')) NOT NULL,
    updated_at TEXT DEFAULT (datetime('now')) NOT NULL
);

-- Servers table
CREATE TABLE servers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    ssh_password_encrypted TEXT NOT NULL,
    ip_address TEXT NOT NULL,
    port INTEGER NOT NULL CHECK (port > 0 AND port <= 65535),
    status TEXT DEFAULT 'inactive' NOT NULL CHECK (status IN ('up', 'down', 'decommissioned', 'inactive')),
    created_at TEXT DEFAULT (datetime('now')) NOT NULL,
    updated_at TEXT DEFAULT (datetime('now')) NOT NULL
);

-- Server Health table (current health status)
CREATE TABLE server_health (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('healthy', 'unhealthy', 'offline', 'error')),
    cpu_usage REAL CHECK (cpu_usage IS NULL OR (cpu_usage >= 0 AND cpu_usage <= 100)),
    memory_usage REAL CHECK (memory_usage IS NULL OR (memory_usage >= 0 AND memory_usage <= 100)),
    disk_usage REAL CHECK (disk_usage IS NULL OR (disk_usage >= 0 AND disk_usage <= 100)),
    uptime TEXT,
    checked_at TEXT NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);

-- Server History table (historical health metrics)
CREATE TABLE server_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('healthy', 'unhealthy', 'offline', 'error')),
    cpu_usage REAL CHECK (cpu_usage IS NULL OR (cpu_usage >= 0 AND cpu_usage <= 100)),
    memory_usage REAL CHECK (memory_usage IS NULL OR (memory_usage >= 0 AND memory_usage <= 100)),
    disk_usage REAL CHECK (disk_usage IS NULL OR (disk_usage >= 0 AND disk_usage <= 100)),
    uptime TEXT,
    checked_at TEXT NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);

-- Docker Containers table
CREATE TABLE docker_containers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id INTEGER NOT NULL,
    container_id TEXT NOT NULL,
    name TEXT NOT NULL,
    image TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('running', 'stopped', 'paused', 'restarting', 'exited', 'created', 'dead')),
    ports TEXT,
    exit_code INTEGER DEFAULT NULL,
    state_changed_at TEXT DEFAULT NULL,
    is_healthy INTEGER DEFAULT NULL CHECK (is_healthy IS NULL OR is_healthy IN (0, 1)),
    last_seen_at TEXT,
    created_at TEXT DEFAULT (datetime('now')) NOT NULL,
    updated_at TEXT DEFAULT (datetime('now')) NOT NULL,
    UNIQUE (server_id, name),
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);

-- ============================================
-- INDEXES
-- ============================================

-- Users indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_user_name ON users(user_name);

-- Servers indexes
CREATE INDEX idx_servers_status ON servers(status);
CREATE INDEX idx_servers_ip_address ON servers(ip_address);

-- Server Health indexes
CREATE INDEX idx_server_health_server_id ON server_health(server_id);
CREATE INDEX idx_server_health_checked_at ON server_health(checked_at);
CREATE INDEX idx_server_health_status ON server_health(status);

-- Server History indexes
CREATE INDEX idx_server_history_server_id ON server_history(server_id);
CREATE INDEX idx_server_history_checked_at ON server_history(checked_at);
CREATE INDEX idx_server_history_status ON server_history(status);

-- Docker Containers indexes
CREATE INDEX idx_docker_containers_server_id ON docker_containers(server_id);
CREATE INDEX idx_docker_containers_status ON docker_containers(status);
CREATE INDEX idx_docker_containers_container_id ON docker_containers(container_id);
CREATE INDEX idx_docker_containers_last_seen ON docker_containers(last_seen_at);
CREATE INDEX idx_docker_containers_state_changed ON docker_containers(state_changed_at);

-- ============================================
-- TRIGGERS FOR UPDATED_AT
-- ============================================

CREATE TRIGGER users_updated_at
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = datetime('now')
    WHERE id = NEW.id;
END;

CREATE TRIGGER servers_updated_at
AFTER UPDATE ON servers
FOR EACH ROW
BEGIN
    UPDATE servers SET updated_at = datetime('now')
    WHERE id = NEW.id;
END;

CREATE TRIGGER docker_containers_updated_at
AFTER UPDATE ON docker_containers
FOR EACH ROW
BEGIN
    UPDATE docker_containers SET updated_at = datetime('now')
    WHERE id = NEW.id;
END;
