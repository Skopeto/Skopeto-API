from app.core.sql_query import SqlQuery

async def get_next_id(repo, seq_name: str) -> int:
    query = f"""
    SELECT nextval('{seq_name}') AS next_id
    """

    sql_query = SqlQuery(repo.session, query, {})
    result = await sql_query.fetch_one()

    if not result or  not isinstance(result, dict):
        raise Exception("Sequence Failed")
    
    return result['next_id']