from fastapi.security import OAuth2PasswordBearer

oauth2_bearer_seller = OAuth2PasswordBearer(tokenUrl="/seller/token")
oauth2_bearer_partner = OAuth2PasswordBearer(tokenUrl="/partner/token")