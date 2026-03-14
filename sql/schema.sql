--
-- PostgreSQL database dump
--

\restrict goyVbMNb9NDuRWvqavsonqywmFH0a9tfUAJBBHfid80ecAdO441VOz2US9ZMuDO

-- Dumped from database version 16.11
-- Dumped by pg_dump version 16.11

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.server_history DROP CONSTRAINT IF EXISTS fk_server_history_server;
ALTER TABLE IF EXISTS ONLY public.server_health DROP CONSTRAINT IF EXISTS fk_server_health_server;
ALTER TABLE IF EXISTS ONLY public.notifications DROP CONSTRAINT IF EXISTS fk_notifications_user;
ALTER TABLE IF EXISTS ONLY public.notification_subscribers DROP CONSTRAINT IF EXISTS fk_notification_subscribers_user;
ALTER TABLE IF EXISTS ONLY public.docker_containers DROP CONSTRAINT IF EXISTS fk_docker_containers_server;
ALTER TABLE IF EXISTS ONLY public.databases DROP CONSTRAINT IF EXISTS fk_databases_server;
ALTER TABLE IF EXISTS ONLY public.database_health DROP CONSTRAINT IF EXISTS fk_database_health_database;
DROP TRIGGER IF EXISTS users_updated_at ON public.users;
DROP TRIGGER IF EXISTS servers_updated_at ON public.servers;
DROP TRIGGER IF EXISTS docker_containers_updated_at ON public.docker_containers;
DROP INDEX IF EXISTS public.idx_users_user_name;
DROP INDEX IF EXISTS public.idx_users_email;
DROP INDEX IF EXISTS public.idx_servers_status;
DROP INDEX IF EXISTS public.idx_servers_ip_address;
DROP INDEX IF EXISTS public.idx_server_history_status;
DROP INDEX IF EXISTS public.idx_server_history_server_id;
DROP INDEX IF EXISTS public.idx_server_history_checked_at;
DROP INDEX IF EXISTS public.idx_server_health_status;
DROP INDEX IF EXISTS public.idx_server_health_server_id;
DROP INDEX IF EXISTS public.idx_server_health_checked_at;
DROP INDEX IF EXISTS public.idx_notifications_user_unread;
DROP INDEX IF EXISTS public.idx_notifications_user_id;
DROP INDEX IF EXISTS public.idx_notifications_is_read;
DROP INDEX IF EXISTS public.idx_notifications_created_at;
DROP INDEX IF EXISTS public.idx_notification_subscribers_user_id;
DROP INDEX IF EXISTS public.idx_notification_subscribers_is_active;
DROP INDEX IF EXISTS public.idx_notification_subscribers_channel;
DROP INDEX IF EXISTS public.idx_notification_subscribers_active_channels;
DROP INDEX IF EXISTS public.idx_docker_containers_status;
DROP INDEX IF EXISTS public.idx_docker_containers_state_changed;
DROP INDEX IF EXISTS public.idx_docker_containers_server_id;
DROP INDEX IF EXISTS public.idx_docker_containers_last_seen;
DROP INDEX IF EXISTS public.idx_docker_containers_container_id;
DROP INDEX IF EXISTS public.idx_databases_server_id;
DROP INDEX IF EXISTS public.idx_databases_name;
DROP INDEX IF EXISTS public.idx_databases_host;
DROP INDEX IF EXISTS public.idx_databases_db_type;
DROP INDEX IF EXISTS public.idx_database_health_status;
DROP INDEX IF EXISTS public.idx_database_health_is_connected;
DROP INDEX IF EXISTS public.idx_database_health_database_id;
DROP INDEX IF EXISTS public.idx_database_health_checked_at;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_user_name_key;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_email_key;
ALTER TABLE IF EXISTS ONLY public.notification_subscribers DROP CONSTRAINT IF EXISTS uq_notification_subscribers;
ALTER TABLE IF EXISTS ONLY public.docker_containers DROP CONSTRAINT IF EXISTS uq_docker_containers;
ALTER TABLE IF EXISTS ONLY public.servers DROP CONSTRAINT IF EXISTS servers_pkey;
ALTER TABLE IF EXISTS ONLY public.server_checks DROP CONSTRAINT IF EXISTS server_checks_pkey;
ALTER TABLE IF EXISTS ONLY public.server_history DROP CONSTRAINT IF EXISTS server_history_pkey;
ALTER TABLE IF EXISTS ONLY public.server_health DROP CONSTRAINT IF EXISTS server_health_pkey;
ALTER TABLE IF EXISTS ONLY public.scheduler_timer DROP CONSTRAINT IF EXISTS scheduler_timer_pkey;
ALTER TABLE IF EXISTS ONLY public.notifications DROP CONSTRAINT IF EXISTS notifications_pkey;
ALTER TABLE IF EXISTS ONLY public.notification_subscribers DROP CONSTRAINT IF EXISTS notification_subscribers_pkey;
ALTER TABLE IF EXISTS ONLY public.docker_containers DROP CONSTRAINT IF EXISTS docker_containers_pkey;
ALTER TABLE IF EXISTS ONLY public.databases DROP CONSTRAINT IF EXISTS databases_pkey;
ALTER TABLE IF EXISTS ONLY public.database_health DROP CONSTRAINT IF EXISTS database_health_pkey;
ALTER TABLE IF EXISTS public.users ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.servers ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.server_checks ALTER COLUMN health_check_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.server_history ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.server_health ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.scheduler_timer ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.notifications ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.notification_subscribers ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.docker_containers ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.databases ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.database_health ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.users_id_seq;
DROP TABLE IF EXISTS public.users;
DROP SEQUENCE IF EXISTS public.servers_id_seq;
DROP TABLE IF EXISTS public.servers;
DROP SEQUENCE IF EXISTS public.health_check_id_seq;
DROP TABLE IF EXISTS public.server_checks;
DROP SEQUENCE IF EXISTS public.server_history_id_seq;
DROP TABLE IF EXISTS public.server_history;
DROP SEQUENCE IF EXISTS public.server_health_id_seq;
DROP TABLE IF EXISTS public.server_health;
DROP SEQUENCE IF EXISTS public.scheduler_timer_id_seq;
DROP TABLE IF EXISTS public.scheduler_timer;
DROP SEQUENCE IF EXISTS public.notifications_id_seq;
DROP TABLE IF EXISTS public.notifications;
DROP SEQUENCE IF EXISTS public.notification_subscribers_id_seq;
DROP TABLE IF EXISTS public.notification_subscribers;
DROP SEQUENCE IF EXISTS public.docker_containers_id_seq;
DROP TABLE IF EXISTS public.docker_containers;
DROP SEQUENCE IF EXISTS public.databases_id_seq;
DROP TABLE IF EXISTS public.databases;
DROP SEQUENCE IF EXISTS public.database_health_id_seq;
DROP TABLE IF EXISTS public.database_health;
DROP FUNCTION IF EXISTS public.update_updated_at_column();
--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: database_health; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.database_health (
    id integer NOT NULL,
    database_id integer NOT NULL,
    status character varying(20) NOT NULL,
    connection_time_ms numeric(10,2),
    is_connected boolean NOT NULL,
    query_time_ms numeric(10,2),
    error_message text,
    checked_at timestamp without time zone NOT NULL,
    CONSTRAINT chk_database_health_connection_time CHECK ((connection_time_ms >= (0)::numeric)),
    CONSTRAINT chk_database_health_query_time CHECK ((query_time_ms >= (0)::numeric)),
    CONSTRAINT chk_database_health_status CHECK (((status)::text = ANY ((ARRAY['healthy'::character varying, 'slow'::character varying, 'warning'::character varying, 'error'::character varying, 'offline'::character varying])::text[])))
);


--
-- Name: TABLE database_health; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.database_health IS 'Stores current health metrics for monitored databases';


--
-- Name: COLUMN database_health.connection_time_ms; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.database_health.connection_time_ms IS 'Time taken to establish connection in milliseconds';


--
-- Name: COLUMN database_health.query_time_ms; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.database_health.query_time_ms IS 'Time taken to execute test query in milliseconds';


--
-- Name: COLUMN database_health.checked_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.database_health.checked_at IS 'Timestamp when health check was performed';


--
-- Name: database_health_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.database_health_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: database_health_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.database_health_id_seq OWNED BY public.database_health.id;


--
-- Name: databases; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.databases (
    id integer NOT NULL,
    server_id integer NOT NULL,
    name character varying(255) NOT NULL,
    db_type character varying(50) NOT NULL,
    host character varying(255) NOT NULL,
    port integer NOT NULL,
    database_name character varying(255),
    service_name character varying(255),
    username character varying(255) NOT NULL,
    encrypted_password character varying(500) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_databases_db_type CHECK (((db_type)::text = ANY ((ARRAY['postgresql'::character varying, 'mysql'::character varying, 'oracle'::character varying, 'sqlite'::character varying, 'mongodb'::character varying, 'redis'::character varying, 'mariadb'::character varying, 'sqlserver'::character varying])::text[]))),
    CONSTRAINT chk_databases_port CHECK (((port > 0) AND (port <= 65535)))
);


--
-- Name: TABLE databases; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.databases IS 'Stores database connection details for monitoring';


--
-- Name: COLUMN databases.db_type; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.databases.db_type IS 'Type of database: postgresql, mysql, oracle, sqlite, mongodb, redis, mariadb, sqlserver';


--
-- Name: COLUMN databases.service_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.databases.service_name IS 'Service name for Oracle databases (TNS)';


--
-- Name: COLUMN databases.encrypted_password; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.databases.encrypted_password IS 'Encrypted database password for secure access';


--
-- Name: databases_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.databases_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: databases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.databases_id_seq OWNED BY public.databases.id;


--
-- Name: docker_containers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.docker_containers (
    id integer NOT NULL,
    server_id integer NOT NULL,
    container_id character varying(100) NOT NULL,
    name character varying(255) NOT NULL,
    image character varying(500) NOT NULL,
    status character varying(20) NOT NULL,
    ports character varying(500),
    last_seen_at timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    exit_code integer,
    state_changed_at timestamp without time zone,
    is_healthy boolean,
    CONSTRAINT chk_docker_containers_status CHECK (((status)::text = ANY ((ARRAY['running'::character varying, 'stopped'::character varying, 'paused'::character varying, 'restarting'::character varying, 'exited'::character varying, 'created'::character varying, 'dead'::character varying])::text[])))
);


--
-- Name: TABLE docker_containers; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.docker_containers IS 'Stores Docker container information from monitored servers';


--
-- Name: COLUMN docker_containers.container_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.docker_containers.container_id IS 'Docker container unique identifier';


--
-- Name: docker_containers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.docker_containers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: docker_containers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.docker_containers_id_seq OWNED BY public.docker_containers.id;


--
-- Name: notification_subscribers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notification_subscribers (
    id integer NOT NULL,
    user_id integer NOT NULL,
    user_name character varying(100) NOT NULL,
    delivery_address_email character varying(255),
    notification_channel character varying(20) NOT NULL,
    slack_webhook_url character varying(500),
    is_active boolean DEFAULT true NOT NULL,
    subscribed_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    first_name character varying(100),
    last_name character varying(100),
    CONSTRAINT chk_notification_channel CHECK (((notification_channel)::text = ANY ((ARRAY['email'::character varying, 'slack'::character varying, 'sms'::character varying])::text[])))
);


--
-- Name: TABLE notification_subscribers; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.notification_subscribers IS 'Stores user notification preferences and delivery channels';


--
-- Name: COLUMN notification_subscribers.user_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.notification_subscribers.user_id IS 'Foreign key to users table';


--
-- Name: COLUMN notification_subscribers.user_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.notification_subscribers.user_name IS 'Username for reference';


--
-- Name: COLUMN notification_subscribers.delivery_address_email; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.notification_subscribers.delivery_address_email IS 'Email address for email notifications';


--
-- Name: COLUMN notification_subscribers.notification_channel; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.notification_subscribers.notification_channel IS 'Delivery channel: email, slack, or sms';


--
-- Name: COLUMN notification_subscribers.slack_webhook_url; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.notification_subscribers.slack_webhook_url IS 'Slack webhook URL for Slack notifications (optional)';


--
-- Name: COLUMN notification_subscribers.is_active; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.notification_subscribers.is_active IS 'Whether the subscription is active';


--
-- Name: COLUMN notification_subscribers.subscribed_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.notification_subscribers.subscribed_at IS 'Timestamp when user subscribed';


--
-- Name: notification_subscribers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.notification_subscribers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: notification_subscribers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.notification_subscribers_id_seq OWNED BY public.notification_subscribers.id;


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notifications (
    id integer NOT NULL,
    user_id integer NOT NULL,
    title character varying(255) NOT NULL,
    message text NOT NULL,
    is_read boolean DEFAULT false NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: TABLE notifications; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.notifications IS 'Stores in-app notifications for users';


--
-- Name: COLUMN notifications.user_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.notifications.user_id IS 'Foreign key to users table';


--
-- Name: COLUMN notifications.title; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.notifications.title IS 'Notification title/subject';


--
-- Name: COLUMN notifications.message; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.notifications.message IS 'Notification message content';


--
-- Name: COLUMN notifications.is_read; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.notifications.is_read IS 'Whether the notification has been read by the user';


--
-- Name: COLUMN notifications.created_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.notifications.created_at IS 'Timestamp when notification was created';


--
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;


--
-- Name: scheduler_timer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.scheduler_timer (
    id integer NOT NULL,
    interval_minutes integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT scheduler_timer_interval_minutes_check CHECK (((interval_minutes >= 1) AND (interval_minutes <= 1440)))
);


--
-- Name: scheduler_timer_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.scheduler_timer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: scheduler_timer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.scheduler_timer_id_seq OWNED BY public.scheduler_timer.id;


--
-- Name: server_health; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.server_health (
    id integer NOT NULL,
    server_id integer NOT NULL,
    status character varying(20) NOT NULL,
    cpu_usage numeric(5,2),
    memory_usage numeric(5,2),
    disk_usage numeric(5,2),
    uptime character varying(100),
    checked_at timestamp without time zone NOT NULL,
    CONSTRAINT chk_server_health_cpu CHECK (((cpu_usage >= (0)::numeric) AND (cpu_usage <= (100)::numeric))),
    CONSTRAINT chk_server_health_disk CHECK (((disk_usage >= (0)::numeric) AND (disk_usage <= (100)::numeric))),
    CONSTRAINT chk_server_health_memory CHECK (((memory_usage >= (0)::numeric) AND (memory_usage <= (100)::numeric))),
    CONSTRAINT chk_server_health_status CHECK (((status)::text = ANY ((ARRAY['healthy'::character varying, 'unhealthy'::character varying, 'offline'::character varying, 'error'::character varying])::text[])))
);


--
-- Name: TABLE server_health; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.server_health IS 'Stores current health metrics for monitored servers';


--
-- Name: COLUMN server_health.checked_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.server_health.checked_at IS 'Timestamp when health check was performed';


--
-- Name: server_health_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.server_health_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: server_health_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.server_health_id_seq OWNED BY public.server_health.id;


--
-- Name: server_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.server_history (
    id integer NOT NULL,
    server_id integer NOT NULL,
    status character varying(20) NOT NULL,
    cpu_usage numeric(5,2),
    memory_usage numeric(5,2),
    disk_usage numeric(5,2),
    uptime character varying(100),
    checked_at timestamp without time zone NOT NULL,
    CONSTRAINT chk_server_history_cpu CHECK (((cpu_usage >= (0)::numeric) AND (cpu_usage <= (100)::numeric))),
    CONSTRAINT chk_server_history_disk CHECK (((disk_usage >= (0)::numeric) AND (disk_usage <= (100)::numeric))),
    CONSTRAINT chk_server_history_memory CHECK (((memory_usage >= (0)::numeric) AND (memory_usage <= (100)::numeric))),
    CONSTRAINT chk_server_history_status CHECK (((status)::text = ANY ((ARRAY['healthy'::character varying, 'unhealthy'::character varying, 'offline'::character varying, 'error'::character varying])::text[])))
);


--
-- Name: TABLE server_history; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.server_history IS 'Stores historical health metrics for trend analysis';


--
-- Name: COLUMN server_history.checked_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.server_history.checked_at IS 'Timestamp when historical metric was recorded';


--
-- Name: server_history_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.server_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: server_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.server_history_id_seq OWNED BY public.server_history.id;


--
-- Name: servers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.servers (
    id integer NOT NULL,
    user_name character varying(100) NOT NULL,
    ssh_password_encrypted character varying(500) NOT NULL,
    ip_address character varying(50) NOT NULL,
    port integer NOT NULL,
    status character varying(20) DEFAULT 'inactive'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_servers_port CHECK (((port > 0) AND (port <= 65535))),
    CONSTRAINT chk_servers_status CHECK (((status)::text = ANY ((ARRAY['up'::character varying, 'down'::character varying, 'decommissioned'::character varying, 'inactive'::character varying])::text[])))
);


--
-- Name: TABLE servers; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.servers IS 'Stores SSH server connection details for monitoring';


--
-- Name: COLUMN servers.ssh_password_encrypted; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.servers.ssh_password_encrypted IS 'Encrypted SSH password for server access';


--
-- Name: servers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.servers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: servers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.servers_id_seq OWNED BY public.servers.id;


--
-- Name: server_checks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.server_checks (
    health_check_id integer NOT NULL,
    name character varying(255) NOT NULL,
    command text NOT NULL,
    threshold integer NOT NULL,
    operator character varying(10) NOT NULL,
    check_status character varying(20) DEFAULT 'active'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_server_checks_status CHECK (((check_status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying])::text[]))),
    CONSTRAINT chk_server_checks_operator CHECK (((operator)::text = ANY ((ARRAY['>'::character varying, '<'::character varying, '='::character varying, '>='::character varying, '<='::character varying, '!='::character varying])::text[])))
);


--
-- Name: TABLE server_checks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.server_checks IS 'Stores custom health check configurations for servers';


--
-- Name: COLUMN server_checks.command; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.server_checks.command IS 'Shell command to execute on the server for health check';


--
-- Name: COLUMN server_checks.threshold; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.server_checks.threshold IS 'Threshold value to compare command output against using the operator';


--
-- Name: COLUMN server_checks.operator; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.server_checks.operator IS 'Comparison operator for threshold evaluation';


--
-- Name: health_check_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.health_check_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: health_check_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.health_check_id_seq OWNED BY public.server_checks.health_check_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    user_name character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    hashed_password character varying(255) NOT NULL,
    roles character varying(500) NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    is_superuser boolean DEFAULT false NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: TABLE users; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.users IS 'Stores user authentication and authorization information';


--
-- Name: COLUMN users.roles; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.roles IS 'JSON array of roles: superadmin, admin, or user';


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: database_health id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.database_health ALTER COLUMN id SET DEFAULT nextval('public.database_health_id_seq'::regclass);


--
-- Name: databases id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.databases ALTER COLUMN id SET DEFAULT nextval('public.databases_id_seq'::regclass);


--
-- Name: docker_containers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.docker_containers ALTER COLUMN id SET DEFAULT nextval('public.docker_containers_id_seq'::regclass);


--
-- Name: notification_subscribers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_subscribers ALTER COLUMN id SET DEFAULT nextval('public.notification_subscribers_id_seq'::regclass);


--
-- Name: notifications id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);


--
-- Name: scheduler_timer id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scheduler_timer ALTER COLUMN id SET DEFAULT nextval('public.scheduler_timer_id_seq'::regclass);


--
-- Name: server_health id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.server_health ALTER COLUMN id SET DEFAULT nextval('public.server_health_id_seq'::regclass);


--
-- Name: server_history id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.server_history ALTER COLUMN id SET DEFAULT nextval('public.server_history_id_seq'::regclass);


--
-- Name: servers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.servers ALTER COLUMN id SET DEFAULT nextval('public.servers_id_seq'::regclass);


--
-- Name: server_checks health_check_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.server_checks ALTER COLUMN health_check_id SET DEFAULT nextval('public.health_check_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: database_health database_health_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.database_health
    ADD CONSTRAINT database_health_pkey PRIMARY KEY (id);


--
-- Name: databases databases_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.databases
    ADD CONSTRAINT databases_pkey PRIMARY KEY (id);


--
-- Name: docker_containers docker_containers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.docker_containers
    ADD CONSTRAINT docker_containers_pkey PRIMARY KEY (id);


--
-- Name: notification_subscribers notification_subscribers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_subscribers
    ADD CONSTRAINT notification_subscribers_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: scheduler_timer scheduler_timer_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scheduler_timer
    ADD CONSTRAINT scheduler_timer_pkey PRIMARY KEY (id);


--
-- Name: server_health server_health_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.server_health
    ADD CONSTRAINT server_health_pkey PRIMARY KEY (id);


--
-- Name: server_history server_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.server_history
    ADD CONSTRAINT server_history_pkey PRIMARY KEY (id);


--
-- Name: servers servers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.servers
    ADD CONSTRAINT servers_pkey PRIMARY KEY (id);


--
-- Name: server_checks server_checks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.server_checks
    ADD CONSTRAINT server_checks_pkey PRIMARY KEY (health_check_id);


--
-- Name: docker_containers uq_docker_containers; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.docker_containers
    ADD CONSTRAINT uq_docker_containers UNIQUE (server_id, name);


--
-- Name: notification_subscribers uq_notification_subscribers; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_subscribers
    ADD CONSTRAINT uq_notification_subscribers UNIQUE (user_id, notification_channel);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_user_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_user_name_key UNIQUE (user_name);


--
-- Name: idx_database_health_checked_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_database_health_checked_at ON public.database_health USING btree (checked_at);


--
-- Name: idx_database_health_database_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_database_health_database_id ON public.database_health USING btree (database_id);


--
-- Name: idx_database_health_is_connected; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_database_health_is_connected ON public.database_health USING btree (is_connected);


--
-- Name: idx_database_health_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_database_health_status ON public.database_health USING btree (status);


--
-- Name: idx_databases_db_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_databases_db_type ON public.databases USING btree (db_type);


--
-- Name: idx_databases_host; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_databases_host ON public.databases USING btree (host);


--
-- Name: idx_databases_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_databases_name ON public.databases USING btree (name);


--
-- Name: idx_databases_server_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_databases_server_id ON public.databases USING btree (server_id);


--
-- Name: idx_docker_containers_container_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_docker_containers_container_id ON public.docker_containers USING btree (container_id);


--
-- Name: idx_docker_containers_last_seen; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_docker_containers_last_seen ON public.docker_containers USING btree (last_seen_at);


--
-- Name: idx_docker_containers_server_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_docker_containers_server_id ON public.docker_containers USING btree (server_id);


--
-- Name: idx_docker_containers_state_changed; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_docker_containers_state_changed ON public.docker_containers USING btree (state_changed_at);


--
-- Name: idx_docker_containers_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_docker_containers_status ON public.docker_containers USING btree (status);


--
-- Name: idx_notification_subscribers_active_channels; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_notification_subscribers_active_channels ON public.notification_subscribers USING btree (is_active, notification_channel);


--
-- Name: idx_notification_subscribers_channel; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_notification_subscribers_channel ON public.notification_subscribers USING btree (notification_channel);


--
-- Name: idx_notification_subscribers_is_active; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_notification_subscribers_is_active ON public.notification_subscribers USING btree (is_active);


--
-- Name: idx_notification_subscribers_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_notification_subscribers_user_id ON public.notification_subscribers USING btree (user_id);


--
-- Name: idx_notifications_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_notifications_created_at ON public.notifications USING btree (created_at);


--
-- Name: idx_notifications_is_read; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_notifications_is_read ON public.notifications USING btree (is_read);


--
-- Name: idx_notifications_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_notifications_user_id ON public.notifications USING btree (user_id);


--
-- Name: idx_notifications_user_unread; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_notifications_user_unread ON public.notifications USING btree (user_id, is_read);


--
-- Name: idx_server_health_checked_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_server_health_checked_at ON public.server_health USING btree (checked_at);


--
-- Name: idx_server_health_server_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_server_health_server_id ON public.server_health USING btree (server_id);


--
-- Name: idx_server_health_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_server_health_status ON public.server_health USING btree (status);


--
-- Name: idx_server_history_checked_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_server_history_checked_at ON public.server_history USING btree (checked_at);


--
-- Name: idx_server_history_server_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_server_history_server_id ON public.server_history USING btree (server_id);


--
-- Name: idx_server_history_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_server_history_status ON public.server_history USING btree (status);


--
-- Name: idx_servers_ip_address; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_servers_ip_address ON public.servers USING btree (ip_address);


--
-- Name: idx_servers_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_servers_status ON public.servers USING btree (status);


--
-- Name: idx_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_users_email ON public.users USING btree (email);


--
-- Name: idx_users_user_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_users_user_name ON public.users USING btree (user_name);


--
-- Name: docker_containers docker_containers_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER docker_containers_updated_at BEFORE UPDATE ON public.docker_containers FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: servers servers_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER servers_updated_at BEFORE UPDATE ON public.servers FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: users users_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER users_updated_at BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: database_health fk_database_health_database; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.database_health
    ADD CONSTRAINT fk_database_health_database FOREIGN KEY (database_id) REFERENCES public.databases(id) ON DELETE CASCADE;


--
-- Name: databases fk_databases_server; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.databases
    ADD CONSTRAINT fk_databases_server FOREIGN KEY (server_id) REFERENCES public.servers(id) ON DELETE CASCADE;


--
-- Name: docker_containers fk_docker_containers_server; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.docker_containers
    ADD CONSTRAINT fk_docker_containers_server FOREIGN KEY (server_id) REFERENCES public.servers(id) ON DELETE CASCADE;


--
-- Name: notification_subscribers fk_notification_subscribers_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_subscribers
    ADD CONSTRAINT fk_notification_subscribers_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: notifications fk_notifications_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT fk_notifications_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: server_health fk_server_health_server; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.server_health
    ADD CONSTRAINT fk_server_health_server FOREIGN KEY (server_id) REFERENCES public.servers(id) ON DELETE CASCADE;


--
-- Name: server_history fk_server_history_server; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.server_history
    ADD CONSTRAINT fk_server_history_server FOREIGN KEY (server_id) REFERENCES public.servers(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict goyVbMNb9NDuRWvqavsonqywmFH0a9tfUAJBBHfid80ecAdO441VOz2US9ZMuDO

