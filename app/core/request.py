import enum

from pydantic import BaseModel



class OrderDirection(enum.StrEnum):
    ASC = 'asc'
    DESC = 'desc'

class OrderField(enum.StrEnum):
    pass

class OrderBy(BaseModel):
    field: OrderField | str
    direction: OrderDirection
    

def generate_order_by(request_entry: list[str], order_field: OrderField) -> list[OrderBy]:
    """Generate a list of OrderBy objects from request entries."""
    order_by_list = []
    for entry in request_entry:
        parts = entry.split(":")
        field = parts[0]
        direction = OrderDirection.ASC
        if len(parts) > 1 and parts[1].upper() == 'DESC':
            direction = OrderDirection.DESC
        order_by_list.append(OrderBy(field=order_field(field), direction=direction))
    return order_by_list
        

        