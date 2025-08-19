from typing import Annotated, TypeAlias
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.services.shipment import ShipmentService
from app.services.seller import SellerService
from app.services.delivery_partner import DeliveryService
from app.utils import decode_access_token
from app.core.security import oauth2_bearer_seller, oauth2_bearer_partner
from fastapi import HTTPException, status
from app.database.models import Seller, DeliveryPartner
from app.database.redis import is_jti_blacklisted
SessionDep = Annotated[AsyncSession,Depends(get_db)]


#Shipment Service Dependency
def get_shipment_service(session: SessionDep) -> ShipmentService:
    return ShipmentService(session,DeliveryService(session))

ServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]




#seller service dependency
def get_seller_service(session: SessionDep) -> SellerService:
    return SellerService(session)

SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]


#partner service dependency
def get_partner_service(session: SessionDep) -> DeliveryService:
    return DeliveryService(session)

PartnerServiceDep: TypeAlias = Annotated[DeliveryService, Depends(get_partner_service)]


# Access token data dep

async def _get_access_token(token: str) -> dict:
    data = decode_access_token(token)
    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
        )
    return data

#seller access token
async def get_seller_access_token(token: Annotated[str,Depends(oauth2_bearer_seller)]) -> dict:
    return await _get_access_token(token)
#partner access token
async def get_partner_access_token(token: Annotated[str,Depends(oauth2_bearer_partner)]) -> dict:
    return await _get_access_token(token)


#get Logged in seller
async def get_current_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token)],
    session: SessionDep,
):
    seller = await session.get(Seller, token_data["user"]["id"])
    if seller is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller not found",
        )
    return seller

#get logged in partner
async def get_current_partner(
    token_data: Annotated[dict, Depends(get_partner_access_token)],
    session: SessionDep,
):
    partner = await session.get(DeliveryPartner, token_data["user"]["id"])
    if partner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery Partner not found",
        )
    return partner

# log in Seller dep
SellerDep = Annotated[
    Seller,
    Depends(get_current_seller),
]

#partner dependency
PartnerDep = Annotated[
    DeliveryPartner,
    Depends(get_current_partner),
]