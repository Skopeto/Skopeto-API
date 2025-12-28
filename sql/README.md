# Database Schemas

This directory contains database schema files for multiple database systems.

## Available Schemas

### PostgreSQL (schema.sql)
**Primary/Production Schema**
- Full featured with advanced constraints
- Supports JSONB for roles field
- Best for production deployments
- Auto-increment via SERIAL
- Rich trigger support

**Usage:**
```bash
psql -U username -d database_name -f schema.sql
```

### Oracle (schema_oracle.sql)
**Enterprise Database Schema**
- Uses NUMBER for integers
- VARCHAR2 instead of VARCHAR
- Sequences for auto-increment
- NUMBER(1) for boolean (0/1)
- Full enterprise features

**Usage:**
```bash
sqlplus username/password@database @schema_oracle.sql
```

### MySQL (schema_mysql.sql)
**Popular Open-Source Schema**
- AUTO_INCREMENT for IDs
- TINYINT(1) for boolean
- UTF8MB4 charset support
- InnoDB engine for transactions
- ON UPDATE CURRENT_TIMESTAMP built-in

**Usage:**
```bash
mysql -u username -p database_name < schema_mysql.sql
```

### SQLite (schema_sqlite.sql)
**Lightweight/Development Schema**
- AUTOINCREMENT for IDs
- INTEGER for boolean (0/1)
- TEXT for VARCHAR fields
- REAL for decimal numbers
- Perfect for development/testing

**Usage:**
```bash
sqlite3 database.db < schema_sqlite.sql
```

## Key Differences

| Feature | PostgreSQL | Oracle | MySQL | SQLite |
|---------|-----------|--------|-------|--------|
| Auto-increment | SERIAL | Sequence | AUTO_INCREMENT | AUTOINCREMENT |
| Boolean | BOOLEAN | NUMBER(1) | TINYINT(1) | INTEGER |
| String | VARCHAR | VARCHAR2 | VARCHAR | TEXT |
| Decimal | NUMERIC | NUMBER | DECIMAL | REAL |
| Timestamp | TIMESTAMP | TIMESTAMP | TIMESTAMP | TEXT |
| Foreign Keys | ✅ Always | ✅ Always | ✅ InnoDB | ⚠️ Requires PRAGMA |

## Schema Structure

All schemas include:

### Tables
1. **users** - Authentication and authorization
2. **servers** - SSH server connection details
3. **server_health** - Current health metrics
4. **server_history** - Historical health data
5. **docker_containers** - Container information

### Indexes
- Performance indexes on frequently queried columns
- Foreign key indexes
- Timestamp indexes for historical queries

### Triggers
- `updated_at` auto-update on record modification
- Auto-increment triggers (Oracle only)

### Constraints
- Foreign key relationships with CASCADE delete
- CHECK constraints for data validation
- UNIQUE constraints for data integrity

## Notes

- **PostgreSQL**: Recommended for production use
- **Oracle**: Use when enterprise features are required
- **MySQL**: Good balance of features and performance
- **SQLite**: Best for development, testing, or embedded applications

## Migration

When switching between databases:
1. Export data from current database
2. Run new schema script
3. Transform and import data (mind data type differences)
4. Update application configuration
5. Test thoroughly

## Boolean Values

Different databases handle booleans differently:
- **PostgreSQL**: TRUE/FALSE or 1/0
- **Oracle**: 1 = TRUE, 0 = FALSE
- **MySQL**: 1 = TRUE, 0 = FALSE
- **SQLite**: 1 = TRUE, 0 = FALSE
