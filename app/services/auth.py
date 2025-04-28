import firebase_admin
from firebase_admin import auth
from fastapi import HTTPException, Header
from typing import Optional

def verify_token(authorization: Optional[str] = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing.")

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme.")

        decoded_token = auth.verify_id_token(token)
        return decoded_token  # contains user info like uid, email, etc.

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")
