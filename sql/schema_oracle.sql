-- ============================================
-- SERVER MONITOR - ORACLE DATABASE SCHEMA
-- ============================================

-- ============================================
-- SEQUENCES
-- ============================================

CREATE SEQUENCE users_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE servers_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE server_health_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE server_history_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE docker_containers_seq START WITH 1 INCREMENT BY 1;

-- ============================================
-- TABLES
-- ============================================

-- Users table
CREATE TABLE users (
    id NUMBER PRIMARY KEY,
    first_name VARCHAR2(100) NOT NULL,
    last_name VARCHAR2(100) NOT NULL,
    user_name VARCHAR2(100) NOT NULL UNIQUE,
    email VARCHAR2(255) NOT NULL UNIQUE,
    hashed_password VARCHAR2(255) NOT NULL,
    roles VARCHAR2(500) NOT NULL,
    is_active NUMBER(1) DEFAULT 1 NOT NULL,
    is_superuser NUMBER(1) DEFAULT 0 NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_users_is_active CHECK (is_active IN (0, 1)),
    CONSTRAINT chk_users_is_superuser CHECK (is_superuser IN (0, 1))
);

-- Servers table
CREATE TABLE servers (
    id NUMBER PRIMARY KEY,
    user_name VARCHAR2(100) NOT NULL,
    ssh_password_encrypted VARCHAR2(500) NOT NULL,
    ip_address VARCHAR2(50) NOT NULL,
    port NUMBER NOT NULL,
    status VARCHAR2(20) DEFAULT 'inactive' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_servers_status CHECK (status IN ('up', 'down', 'decommissioned', 'inactive')),
    CONSTRAINT chk_servers_port CHECK (port > 0 AND port <= 65535)
);

-- Server Health table (current health status)
CREATE TABLE server_health (
    id NUMBER PRIMARY KEY,
    server_id NUMBER NOT NULL,
    status VARCHAR2(20) NOT NULL,
    cpu_usage NUMBER(5,2),
    memory_usage NUMBER(5,2),
    disk_usage NUMBER(5,2),
    uptime VARCHAR2(100),
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
    id NUMBER PRIMARY KEY,
    server_id NUMBER NOT NULL,
    status VARCHAR2(20) NOT NULL,
    cpu_usage NUMBER(5,2),
    memory_usage NUMBER(5,2),
    disk_usage NUMBER(5,2),
    uptime VARCHAR2(100),
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
    id NUMBER PRIMARY KEY,
    server_id NUMBER NOT NULL,
    container_id VARCHAR2(100) NOT NULL,
    name VARCHAR2(255) NOT NULL,
    image VARCHAR2(500) NOT NULL,
    status VARCHAR2(20) NOT NULL,
    ports VARCHAR2(500),
    exit_code NUMBER DEFAULT NULL,
    state_changed_at TIMESTAMP DEFAULT NULL,
    is_healthy NUMBER(1) DEFAULT NULL,
    last_seen_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_docker_containers_server FOREIGN KEY (server_id)
        REFERENCES servers(id) ON DELETE CASCADE,
    CONSTRAINT chk_docker_containers_status CHECK (status IN ('running', 'stopped', 'paused', 'restarting', 'exited', 'created', 'dead')),
    CONSTRAINT chk_docker_is_healthy CHECK (is_healthy IS NULL OR is_healthy IN (0, 1)),
    CONSTRAINT uq_docker_containers UNIQUE (server_id, name)
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
-- TRIGGERS FOR AUTO-INCREMENT
-- ============================================

CREATE OR REPLACE TRIGGER users_before_insert
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        SELECT users_seq.NEXTVAL INTO :NEW.id FROM dual;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER servers_before_insert
BEFORE INSERT ON servers
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        SELECT servers_seq.NEXTVAL INTO :NEW.id FROM dual;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER server_health_before_insert
BEFORE INSERT ON server_health
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        SELECT server_health_seq.NEXTVAL INTO :NEW.id FROM dual;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER server_history_before_insert
BEFORE INSERT ON server_history
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        SELECT server_history_seq.NEXTVAL INTO :NEW.id FROM dual;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER docker_containers_before_insert
BEFORE INSERT ON docker_containers
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        SELECT docker_containers_seq.NEXTVAL INTO :NEW.id FROM dual;
    END IF;
END;
/

-- ============================================
-- TRIGGERS FOR UPDATED_AT
-- ============================================

CREATE OR REPLACE TRIGGER users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    :NEW.updated_at := CURRENT_TIMESTAMP;
END;
/

CREATE OR REPLACE TRIGGER servers_updated_at
BEFORE UPDATE ON servers
FOR EACH ROW
BEGIN
    :NEW.updated_at := CURRENT_TIMESTAMP;
END;
/

CREATE OR REPLACE TRIGGER docker_containers_updated_at
BEFORE UPDATE ON docker_containers
FOR EACH ROW
BEGIN
    :NEW.updated_at := CURRENT_TIMESTAMP;
END;
/

-- ============================================
-- COMMENTS
-- ============================================

COMMENT ON TABLE users IS 'Stores user authentication and authorization information';
COMMENT ON TABLE servers IS 'Stores SSH server connection details for monitoring';
COMMENT ON TABLE server_health IS 'Stores current health metrics for monitored servers';
COMMENT ON TABLE server_history IS 'Stores historical health metrics for trend analysis';
COMMENT ON TABLE docker_containers IS 'Stores Docker container information from monitored servers';

COMMENT ON COLUMN users.roles IS 'JSON array of roles: superadmin, admin, or user';
COMMENT ON COLUMN servers.ssh_password_encrypted IS 'Encrypted SSH password for server access';
COMMENT ON COLUMN server_health.checked_at IS 'Timestamp when health check was performed';
COMMENT ON COLUMN server_history.checked_at IS 'Timestamp when historical metric was recorded';
COMMENT ON COLUMN docker_containers.container_id IS 'Docker container unique identifier';
