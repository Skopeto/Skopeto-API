-- ============================================
-- SERVER MONITOR - MYSQL DATABASE SCHEMA
-- ============================================

-- ============================================
-- TABLES
-- ============================================

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    user_name VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    roles VARCHAR(500) NOT NULL,
    is_active TINYINT(1) DEFAULT 1 NOT NULL,
    is_superuser TINYINT(1) DEFAULT 0 NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    INDEX idx_users_email (email),
    INDEX idx_users_user_name (user_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Stores user authentication and authorization information';

-- Servers table
CREATE TABLE servers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    ssh_password_encrypted VARCHAR(500) NOT NULL,
    ip_address VARCHAR(50) NOT NULL,
    port INT NOT NULL,
    status VARCHAR(20) DEFAULT 'inactive' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_servers_status CHECK (status IN ('up', 'down', 'decommissioned', 'inactive')),
    CONSTRAINT chk_servers_port CHECK (port > 0 AND port <= 65535),
    INDEX idx_servers_status (status),
    INDEX idx_servers_ip_address (ip_address)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Stores SSH server connection details for monitoring';

-- Server Health table (current health status)
CREATE TABLE server_health (
    id INT AUTO_INCREMENT PRIMARY KEY,
    server_id INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    cpu_usage DECIMAL(5,2),
    memory_usage DECIMAL(5,2),
    disk_usage DECIMAL(5,2),
    uptime VARCHAR(100),
    checked_at TIMESTAMP NOT NULL,
    CONSTRAINT fk_server_health_server FOREIGN KEY (server_id)
        REFERENCES servers(id) ON DELETE CASCADE,
    CONSTRAINT chk_server_health_status CHECK (status IN ('healthy', 'unhealthy', 'offline', 'error')),
    CONSTRAINT chk_server_health_cpu CHECK (cpu_usage >= 0 AND cpu_usage <= 100),
    CONSTRAINT chk_server_health_memory CHECK (memory_usage >= 0 AND memory_usage <= 100),
    CONSTRAINT chk_server_health_disk CHECK (disk_usage >= 0 AND disk_usage <= 100),
    INDEX idx_server_health_server_id (server_id),
    INDEX idx_server_health_checked_at (checked_at),
    INDEX idx_server_health_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Stores current health metrics for monitored servers';

-- Server History table (historical health metrics)
CREATE TABLE server_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    server_id INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    cpu_usage DECIMAL(5,2),
    memory_usage DECIMAL(5,2),
    disk_usage DECIMAL(5,2),
    uptime VARCHAR(100),
    checked_at TIMESTAMP NOT NULL,
    CONSTRAINT fk_server_history_server FOREIGN KEY (server_id)
        REFERENCES servers(id) ON DELETE CASCADE,
    CONSTRAINT chk_server_history_status CHECK (status IN ('healthy', 'unhealthy', 'offline', 'error')),
    CONSTRAINT chk_server_history_cpu CHECK (cpu_usage >= 0 AND cpu_usage <= 100),
    CONSTRAINT chk_server_history_memory CHECK (memory_usage >= 0 AND memory_usage <= 100),
    CONSTRAINT chk_server_history_disk CHECK (disk_usage >= 0 AND disk_usage <= 100),
    INDEX idx_server_history_server_id (server_id),
    INDEX idx_server_history_checked_at (checked_at),
    INDEX idx_server_history_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Stores historical health metrics for trend analysis';

-- Docker Containers table
CREATE TABLE docker_containers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    server_id INT NOT NULL,
    container_id VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    image VARCHAR(500) NOT NULL,
    status VARCHAR(20) NOT NULL,
    ports VARCHAR(500),
    exit_code INT DEFAULT NULL,
    state_changed_at TIMESTAMP NULL DEFAULT NULL,
    is_healthy TINYINT(1) DEFAULT NULL,
    last_seen_at TIMESTAMP NULL DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_docker_containers_server FOREIGN KEY (server_id)
        REFERENCES servers(id) ON DELETE CASCADE,
    CONSTRAINT chk_docker_containers_status CHECK (status IN ('running', 'stopped', 'paused', 'restarting', 'exited', 'created', 'dead')),
    CONSTRAINT uq_docker_containers UNIQUE (server_id, name),
    INDEX idx_docker_containers_server_id (server_id),
    INDEX idx_docker_containers_status (status),
    INDEX idx_docker_containers_container_id (container_id),
    INDEX idx_docker_containers_last_seen (last_seen_at),
    INDEX idx_docker_containers_state_changed (state_changed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Stores Docker container information from monitored servers';

-- ============================================
-- COLUMN COMMENTS
-- ============================================

ALTER TABLE users MODIFY COLUMN roles VARCHAR(500) NOT NULL
    COMMENT 'JSON array of roles: superadmin, admin, or user';

ALTER TABLE servers MODIFY COLUMN ssh_password_encrypted VARCHAR(500) NOT NULL
    COMMENT 'Encrypted SSH password for server access';

ALTER TABLE server_health MODIFY COLUMN checked_at TIMESTAMP NOT NULL
    COMMENT 'Timestamp when health check was performed';

ALTER TABLE server_history MODIFY COLUMN checked_at TIMESTAMP NOT NULL
    COMMENT 'Timestamp when historical metric was recorded';

ALTER TABLE docker_containers MODIFY COLUMN container_id VARCHAR(100) NOT NULL
    COMMENT 'Docker container unique identifier';
