from model import (
    Users
)
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.user_service import (decodeJWT)
import motor.motor_asyncio
from decouple import config
from passlib.context import CryptContext

MONGO_DETAILS = config('MONGO_DETAILS')


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(username: str, password: str):
    # Connexion à la base de données MongoDB
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
    database = client.Users
    Users_collection = database.get_collection("users_collection")
    user_data = await Users_collection.find_one({"username": username})
    print(user_data)

    if user_data:
        user = Users(**user_data)
        if bcrypt_context.verify(password, user.password):
            return user
    return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                print("1")
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                print("2")
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        print("payload", payload)
        if payload:

            is_verified = payload.get("sub", {}).get("is_verified")
            print(is_verified)
            if is_verified == True:
                print("true")
                isTokenValid = True
            else:
                print("false")
                isTokenValid = False
        print("istok", isTokenValid)
        return isTokenValid
