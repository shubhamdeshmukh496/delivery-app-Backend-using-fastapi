from app.services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.api.schema.delivery_partner import PartnerCreateSchema, PartnerUpdateSchema
from app.database.models import DeliveryPartner, Shipment
from sqlalchemy import select, any_
from typing import Sequence

class DeliveryService(UserService):
    def __init__(self,session : AsyncSession):
        super().__init__(DeliveryPartner,session)
    async def add(self, delivery_partner: PartnerCreateSchema):
        return await self._add_user(delivery_partner.model_dump())

    async def token(self, email, password):
        return await self._generate_token(email, password)

    async def update(self, partner: DeliveryPartner):
        return await self._update(partner)

    async def get_partner_by_zipcode(self, zipcode: int) -> Sequence[DeliveryPartner]:
        result = await self.session.scalars(select(DeliveryPartner).where(zipcode == any_(DeliveryPartner.serviceable_zip_codes)))
        return result.all()
    

    
    async def assign_shipment(self, shipment:Shipment):
        eligible_partners =  await self.get_partner_by_zipcode(shipment.destination)
        for partner in eligible_partners:
            if partner.current_handling_capacity > 0:
                # partner.shipments.append(shipment)
                shipment.delivery_partner_id = partner.id
                return partner
        
        raise HTTPException(
            status_code =  status.HTTP_409_CONFLICT,
            detail="No eligible delivery partner found"
        )
