from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Seller
from app.api.schema.seller import SellerCreateSchema
from passlib.context import CryptContext
# from sqlalchemy import select
# from fastapi import HTTPException, status
# from app.utils import generate_access_token
# from app.services.base import BaseService
from app.services.user import UserService
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SellerService(UserService):
    def __init__(self, session: AsyncSession):
        super().__init__(Seller, session)
    async def add(self,seller_create: SellerCreateSchema):
        # seller = Seller(
        #     **seller_create.model_dump(exclude = ["password"]),
        #     hashed_password = bcrypt_context.hash(seller_create.password)
        # )
        # return await self._add(seller)
        return await self._add_user(seller_create.model_dump())

    async def token(self, email, password):
        return await self._generate_token(email, password)