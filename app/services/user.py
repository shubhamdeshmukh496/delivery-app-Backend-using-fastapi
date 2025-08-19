from app.services.base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
# from app.database.models import User
from app.utils import generate_access_token
from passlib.context import CryptContext
from sqlalchemy import select
from fastapi import HTTPException, status
from typing import Type, TypeVar

ModelType = TypeVar("ModelType")
# from app.api.schema.seller import SellerCreateSchema
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class UserService(BaseService):
    def __init__(self, model:Type[ModelType], session: AsyncSession):
        # super().__init__(User, session)  ## Here we can also do normal init with model and session.

    # OR WE CAN DO LIKE THIS
    # def __init__(self, model: Type[User], session: AsyncSession)
        self.model = model
        self.session = session

    async def _add_user(self, data: dict):
        password = data.pop("password")
        user = self.model(
            **data,
            hashed_password=bcrypt_context.hash(password),
        )
        return await self._add(user)
    


    async def _get_by_email(self, email):
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )
    


    async def _generate_token(self, email, password) -> str:
        # Validate the credentials
        user = await self._get_by_email(email)

        if user is None or not bcrypt_context.verify(
            password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or password is incorrect",
            )

        return generate_access_token(
            data={
                "user": {
                    "name": user.name,
                    "id": str(user.id),
                },
            }
        )
