from typing import Any, Callable, TypeVar, overload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.request import OrderBy

T = TypeVar('T')

def order_by_entry_to_str(order_by: OrderBy, mapper: dict[str, str]) -> str:
    field = mapper.get(order_by.field, order_by.field)
    return f'{field} {order_by.direction}'

def order_by_clause(order_by: list[OrderBy], mapper: dict[str, str]) -> str:
    return ", ".join([order_by_entry_to_str(order, mapper) for order in order_by])

def list_to_sql_array(values: list[Any]) -> str:
    if not values:
        return "NULL"
    formatted_values = ", ".join(f"'{value}'" if isinstance(value, str) else str(value) for value in values)
    return f"({formatted_values})"

def where_in_clause(field_name: str, values: list[Any]) -> str:
    if not values:
        return "1=1"
    placeholders = ", ".join([f":{field_name}_{i}" for i in range(len(values))])
    return f"{field_name} IN ({placeholders})"

class SqlQuery:
    def __init__(self, session: AsyncSession, query: str, params: dict[str, Any] | None = None):
        self.session = session
        self.query = query
        self.params = params or {}

    async def aggregate(self) -> Any:
        cursor = await self.session.execute(text(self.query), self.params) if self.params else await self.session.execute(text(self.query))
        row = cursor.fetchone()
        if not row:
            return None
        return row[0]

    async def persist(self) -> None:
        await self.session.execute(text(self.query), self.params) if self.params else await self.session.execute(text(self.query))
        await self.session.commit()

    @overload
    async def fetch_one(self, transformer: None = None) -> dict[str, Any] | None: ...
    
    @overload
    async def fetch_one(self, transformer: Callable[[dict[str, Any]], T]) -> T | None: ...

    async def fetch_one(self, transformer: Callable[[dict[str, Any]], Any] | None = None) -> dict[str, Any] | Any | None:
        cursor = await self.session.execute(text(self.query), self.params) if self.params else await self.session.execute(text(self.query))
        row = cursor.fetchone()
        if not row:
            return None
        if transformer:
            return transformer(row._asdict())
        return row._asdict()

    @overload
    async def fetch_all(self, transformer: None = None) -> list[dict[str, Any]]: ...
    
    @overload
    async def fetch_all(self, transformer: Callable[[dict[str, Any]], T]) -> list[T]: ...

    async def fetch_all(self, transformer: Callable[[dict[str, Any]], Any] | None = None) -> list[dict[str, Any]] | list[Any]:
        cursor = await self.session.execute(text(self.query), self.params) if self.params else await self.session.execute(text(self.query))
        if transformer:
            return [transformer(row._asdict()) for row in cursor]
        return [row._asdict() for row in cursor]
    
    async def delete(self) -> None:
        await self.session.execute(text(self.query), self.params) if self.params else await self.session.execute(text(self.query))
        await self.session.commit()