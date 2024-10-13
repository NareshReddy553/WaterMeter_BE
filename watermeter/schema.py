from typing import Optional
from ninja import Schema

from account.schema.flat_schema import FlatResponseSchema
from account.schema.user_schema import UserProfileResponseSchema


class waterMeterProcessResponseSchema(Schema):
    kilolitres: int
    serial_number: str
    flat: Optional[FlatResponseSchema] = None
    user:Optional[UserProfileResponseSchema]=None
    
class CreateWaterMeterSchema(Schema):
    flat_id:int
    kiloliters:int