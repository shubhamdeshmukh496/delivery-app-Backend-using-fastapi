from jose import jwt,JWTError
from datetime import datetime, timedelta,timezone
from fastapi import HTTPException, status
import uuid
from app.config import security_settings

def generate_access_token(data : dict) -> str:
    return jwt.encode({**data,"jti": str(uuid.uuid4()),"exp": datetime.now(timezone.utc) + timedelta(minutes=15)},
                                 key=security_settings.JWT_SECRET,
                                 algorithm=security_settings.JWT_ALGORITHM)

def decode_access_token(token: str) -> dict | None :
    try:
        payload = jwt.decode(token,key = security_settings.JWT_SECRET,algorithms = [security_settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
