from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Shipment, ShipmentStatus
from app.api.schema.shipment import ShipmentCreateSchema
from datetime import datetime, timedelta
from app.database.models import Seller
from uuid import UUID
from app.services.base import BaseService
from app.services.delivery_partner import DeliveryService
class ShipmentService(BaseService):
    def __init__(self, session : AsyncSession, partner_service : DeliveryService):
        super().__init__(Shipment,session)
        self.partner_service = partner_service
    async def get(self,id : UUID) -> Shipment | None:
        return await self._get(id)

    async def add(self,shipment_create : ShipmentCreateSchema, seller : Seller):
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status = ShipmentStatus.PLACED,
            estimated_delivery = datetime.now() + timedelta(days=5),
            seller_id = seller.id  # Example logic for estimated delivery
        )
        partner = await self.partner_service.assign_shipment(
            new_shipment
        )
        # Add the delivery partner foreign key
        new_shipment.delivery_partner_id = partner.id
        return await self._add(new_shipment)
       
    async def update(self, id:UUID, shipment_update : dict):
        shipment = await self.session.get(Shipment, id)
        for key, value in shipment_update.items():
            setattr(shipment, key, value)

        return await self._update(shipment)

             
    async def delete(self, id:UUID):
        await self._delete(await self.get(id))