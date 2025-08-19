from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import ServiceDep, SellerServiceDep
from app.api.schema.seller import SellerCreateSchema
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from app.core.security import oauth2_bearer_seller
from app.api.dependencies import get_seller_access_token
from app.database.redis import add_jti_to_blacklist,is_jti_blacklisted
router = APIRouter(prefix = "/seller", tags = ["seller"])

@router.post("/register")
async def register_seller(service: SellerServiceDep, seller: SellerCreateSchema):
    return await service.add(seller)

@router.post("/token")
async def create_token(service:SellerServiceDep, form_data: OAuth2PasswordRequestForm = Depends()):
    token = await service.token(form_data.username,form_data.password)
    return {"access_token":token,"token_type":"bearer"}

@router.get("/logout")
async def logout_seller( token_data: Annotated[dict, Depends(get_seller_access_token)]):
    await add_jti_to_blacklist(token_data['jti'])
    return {"message":"Successfully logged out"}