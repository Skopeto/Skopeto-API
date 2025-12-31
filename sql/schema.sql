-- ============================================
-- SERVER MONITOR - POSTGRESQL DATABASE SCHEMA
-- ============================================

-- ============================================
-- TABLES
-- ============================================

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    user_name VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    roles VARCHAR(500) NOT NULL,  -- Store as JSON array or comma-separated values
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    is_superuser BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Servers table
CREATE TABLE servers (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    ssh_password_encrypted VARCHAR(500) NOT NULL,
    ip_address VARCHAR(50) NOT NULL,
    port INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'inactive' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_servers_status CHECK (status IN ('up', 'down', 'decommissioned', 'inactive')),
    CONSTRAINT chk_servers_port CHECK (port > 0 AND port <= 65535)
);

-- Server Health table (current health status)
CREATE TABLE server_health (
    id SERIAL PRIMARY KEY,
    server_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,
    cpu_usage NUMERIC(5,2),
    memory_usage NUMERIC(5,2),
    disk_usage NUMERIC(5,2),
    uptime VARCHAR(100),
    checked_at TIMESTAMP NOT NULL,
    CONSTRAINT fk_server_health_server FOREIGN KEY (server_id)
        REFERENCES servers(id) ON DELETE CASCADE,
    CONSTRAINT chk_server_health_status CHECK (status IN ('healthy', 'unhealthy', 'offline', 'error')),
    CONSTRAINT chk_server_health_cpu CHECK (cpu_usage >= 0 AND cpu_usage <= 100),
    CONSTRAINT chk_server_health_memory CHECK (memory_usage >= 0 AND memory_usage <= 100),
    CONSTRAINT chk_server_health_disk CHECK (disk_usage >= 0 AND disk_usage <= 100)
);

-- Server History table (historical health metrics)
CREATE TABLE server_history (
    id SERIAL PRIMARY KEY,
    server_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,
    cpu_usage NUMERIC(5,2),
    memory_usage NUMERIC(5,2),
    disk_usage NUMERIC(5,2),
    uptime VARCHAR(100),
    checked_at TIMESTAMP NOT NULL,
    CONSTRAINT fk_server_history_server FOREIGN KEY (server_id)
        REFERENCES servers(id) ON DELETE CASCADE,
    CONSTRAINT chk_server_history_status CHECK (status IN ('healthy', 'unhealthy', 'offline', 'error')),
    CONSTRAINT chk_server_history_cpu CHECK (cpu_usage >= 0 AND cpu_usage <= 100),
    CONSTRAINT chk_server_history_memory CHECK (memory_usage >= 0 AND memory_usage <= 100),
    CONSTRAINT chk_server_history_disk CHECK (disk_usage >= 0 AND disk_usage <= 100)
);

-- Docker Containers table
CREATE TABLE docker_containers (
    id SERIAL PRIMARY KEY,
    server_id INTEGER NOT NULL,
    container_id VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    image VARCHAR(500) NOT NULL,
    status VARCHAR(20) NOT NULL,
    ports VARCHAR(500),
    exit_code INTEGER DEFAULT NULL,
    state_changed_at TIMESTAMP DEFAULT NULL,
    is_healthy BOOLEAN DEFAULT NULL,
    last_seen_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_docker_containers_server FOREIGN KEY (server_id)
        REFERENCES servers(id) ON DELETE CASCADE,
    CONSTRAINT chk_docker_containers_status CHECK (status IN ('running', 'stopped', 'paused', 'restarting', 'exited', 'created', 'dead')),
    CONSTRAINT uq_docker_containers UNIQUE (server_id, name)
);

-- Databases table
CREATE TABLE databases (
    id SERIAL PRIMARY KEY,
    server_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    db_type VARCHAR(50) NOT NULL,
    host VARCHAR(255) NOT NULL,
    port INTEGER NOT NULL,
    database_name VARCHAR(255),
    service_name VARCHAR(255),
    username VARCHAR(255) NOT NULL,
    encrypted_password VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_databases_server FOREIGN KEY (server_id)
        REFERENCES servers(id) ON DELETE CASCADE,
    CONSTRAINT chk_databases_port CHECK (port > 0 AND port <= 65535),
    CONSTRAINT chk_databases_db_type CHECK (db_type IN ('postgresql', 'mysql', 'oracle', 'sqlite', 'mongodb', 'redis', 'mariadb', 'sqlserver'))
);

-- Database Health table (current health status)
CREATE TABLE database_health (
    id SERIAL PRIMARY KEY,
    database_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,
    connection_time_ms NUMERIC(10,2),
    is_connected BOOLEAN NOT NULL,
    query_time_ms NUMERIC(10,2),
    error_message TEXT,
    checked_at TIMESTAMP NOT NULL,
    CONSTRAINT fk_database_health_database FOREIGN KEY (database_id)
        REFERENCES databases(id) ON DELETE CASCADE,
    CONSTRAINT chk_database_health_status CHECK (status IN ('healthy', 'slow', 'warning', 'error', 'offline')),
    CONSTRAINT chk_database_health_connection_time CHECK (connection_time_ms >= 0),
    CONSTRAINT chk_database_health_query_time CHECK (query_time_ms >= 0)
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

-- Databases indexes
CREATE INDEX idx_databases_server_id ON databases(server_id);
CREATE INDEX idx_databases_db_type ON databases(db_type);
CREATE INDEX idx_databases_host ON databases(host);
CREATE INDEX idx_databases_name ON databases(name);

-- Database Health indexes
CREATE INDEX idx_database_health_database_id ON database_health(database_id);
CREATE INDEX idx_database_health_checked_at ON database_health(checked_at);
CREATE INDEX idx_database_health_status ON database_health(status);
CREATE INDEX idx_database_health_is_connected ON database_health(is_connected);

-- ============================================
-- FUNCTIONS FOR UPDATED_AT TRIGGER
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- TRIGGERS FOR UPDATED_AT
-- ============================================

CREATE TRIGGER users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER servers_updated_at
    BEFORE UPDATE ON servers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER docker_containers_updated_at
    BEFORE UPDATE ON docker_containers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- COMMENTS
-- ============================================

COMMENT ON TABLE users IS 'Stores user authentication and authorization information';
COMMENT ON TABLE servers IS 'Stores SSH server connection details for monitoring';
COMMENT ON TABLE server_health IS 'Stores current health metrics for monitored servers';
COMMENT ON TABLE server_history IS 'Stores historical health metrics for trend analysis';
COMMENT ON TABLE docker_containers IS 'Stores Docker container information from monitored servers';
COMMENT ON TABLE databases IS 'Stores database connection details for monitoring';
COMMENT ON TABLE database_health IS 'Stores current health metrics for monitored databases';

COMMENT ON COLUMN users.roles IS 'JSON array of roles: superadmin, admin, or user';
COMMENT ON COLUMN servers.ssh_password_encrypted IS 'Encrypted SSH password for server access';
COMMENT ON COLUMN server_health.checked_at IS 'Timestamp when health check was performed';
COMMENT ON COLUMN server_history.checked_at IS 'Timestamp when historical metric was recorded';
COMMENT ON COLUMN docker_containers.container_id IS 'Docker container unique identifier';
COMMENT ON COLUMN databases.db_type IS 'Type of database: postgresql, mysql, oracle, sqlite, mongodb, redis, mariadb, sqlserver';
COMMENT ON COLUMN databases.encrypted_password IS 'Encrypted database password for secure access';
COMMENT ON COLUMN databases.service_name IS 'Service name for Oracle databases (TNS)';
COMMENT ON COLUMN database_health.connection_time_ms IS 'Time taken to establish connection in milliseconds';
COMMENT ON COLUMN database_health.query_time_ms IS 'Time taken to execute test query in milliseconds';
COMMENT ON COLUMN database_health.checked_at IS 'Timestamp when health check was performed';
