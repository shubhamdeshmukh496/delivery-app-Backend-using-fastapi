from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import ServiceDep, PartnerDep, PartnerServiceDep
from app.api.schema.delivery_partner import PartnerCreateSchema, PartnerUpdateSchema
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from app.api.dependencies import get_partner_access_token
from app.database.redis import add_jti_to_blacklist,is_jti_blacklisted

router = APIRouter(prefix = "/partner", tags = ["Delivery Partner"])

@router.post("/register")
async def register_delivery_partner(
    partner: PartnerCreateSchema,
    service: PartnerServiceDep,
):
    return await service.add(partner)

@router.post("/token")
async def login_delivery_partner(service:PartnerServiceDep, form_data: OAuth2PasswordRequestForm = Depends()):
    token = await service.token(form_data.username,form_data.password)
    return {"access_token":token,"token_type":"bearer"}

@router.post("/update")
async def update_delivery_partner(partner_update: PartnerUpdateSchema, partner: PartnerDep, service: PartnerServiceDep):
    update_data = partner_update.model_dump(exclude_none=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    # Apply updates to the existing partner instance
    for field, value in update_data.items():
        setattr(partner, field, value)

    # Just call service.update — commit/refresh will happen inside
    return await service.update(partner)

@router.get("/logout")
async def logout_delivery_partner( token_data: Annotated[dict, Depends(get_partner_access_token)]):
    await add_jti_to_blacklist(token_data['jti'])
    return {"message":"Successfully logged out"}