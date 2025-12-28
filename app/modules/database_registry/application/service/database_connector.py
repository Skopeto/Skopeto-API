import asyncpg
import aiomysql
import oracledb
from app.modules.database_registry.domain.entity.database import Database
from app.core.encrypt import decrypt_password

class DatabaseConnector: 
    
    async def connect(self, database: Database):
        password = decrypt_password(database.encrypted_password)
        
        match database.db_type:
            case 'postgres':
                return await asyncpg.connect(
                    host=database.host,
                    port=database.port,
                    user=database.username,
                    password=password,
                    database=database.database_name,
                    timeout=10
                )
            case 'mysql':
                return await aiomysql.connect(
                    host=database.host,
                    port=database.port,
                    user=database.username,
                    password=password,
                    db=database.database_name
                )
            case 'oracle':
                return await oracledb.connect_async(
                    user=database.username,
                    password=password,
                    dsn=f"{database.host}:{database.port}/{database.service_name}"
                )
            case _:
                raise ValueError(f"Unsupported database type: {database.db_type}")
    
    async def execute_test_query(self, connection, db_type: str):
        match db_type:
            case 'postgres':
                return await connection.fetchval('SELECT 1')
            
            case 'mysql':
                async with connection.cursor() as cursor:
                    await cursor.execute('SELECT 1')
                    return await cursor.fetchone()
            
            case 'oracle':
                cursor = connection.cursor()
                await cursor.execute('SELECT 1 FROM DUAL')
                result = await cursor.fetchone()
                await cursor.close()
                return result
            
            case _:
                raise ValueError(f"Unsupported database type: {db_type}")
    
    async def close_connection(self, connection, db_type: str):
        match db_type:
            case 'postgres':
                await connection.close()
            
            case 'mysql':
                connection.close()
            
            case 'oracle':
                await connection.close()
            
            case _:
                pass