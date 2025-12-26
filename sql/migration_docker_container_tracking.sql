-- Migration: Add container failure tracking fields
-- Description: Add exit_code, state_changed_at, and is_healthy fields to track container failures and state changes
-- Date: 2025-12-26

ALTER TABLE docker_containers
ADD COLUMN exit_code INTEGER DEFAULT NULL,
ADD COLUMN state_changed_at TIMESTAMP DEFAULT NULL,
ADD COLUMN is_healthy BOOLEAN DEFAULT NULL;

CREATE INDEX idx_docker_containers_last_seen ON docker_containers(last_seen_at);
CREATE INDEX idx_docker_containers_state_changed ON docker_containers(state_changed_at);

ALTER TABLE docker_containers
DROP CONSTRAINT IF EXISTS chk_docker_containers_status,
ADD CONSTRAINT chk_docker_containers_status CHECK (
    status IN ('running', 'stopped', 'paused', 'restarting', 'exited', 'created', 'dead')
);
