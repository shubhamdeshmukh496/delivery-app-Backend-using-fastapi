from pydantic import BaseModel, Field
from datetime import datetime
from app.database.models import ShipmentStatus
import uuid
from pydantic import ConfigDict
class ShipmentCreateSchema(BaseModel):
    content : str
    weight : float
    destination : int

class ShipmentUpdateSchema(BaseModel):
    status: ShipmentStatus | None = Field(default=None)

class ShipmentResponseSchema(BaseModel):
    id: uuid.UUID
    content: str
    weight: float
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime
    seller_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

