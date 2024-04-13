from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
import motor.motor_asyncio
from model import (Users, UserVerification, ResponseModel, ErrorResponseModel)
from passlib.context import CryptContext
from decouple import config
from datetime import timedelta
from auth import (authenticate_user)
from services.user_service import (add_user, all_user, generate_verification_code,
                                   send_verification_email, generate_expiration_time, check_phone_numbers, is_password_strong, create_access_token, create_refresh_token, check_user_existence, regenerate_verification_code)

MONGO_DETAILS = config('MONGO_DETAILS')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.Users
Users_collection = database.get_collection("users_collection")


router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# route pour enregistrer un utilisateur
@router.post("/", response_description="user create")
async def user_data(User: Users = Body(...)):
    try:
        username_exists = await check_user_existence(User.username,User.email)
        print("sgi",username_exists)
        if username_exists:
            return ResponseModel("", status.HTTP_400_BAD_REQUEST, "username ou email existe deja"),
        if check_phone_numbers(User.phone):
            if is_password_strong(User.password):
                hashed_password = bcrypt_context.hash(User.password)
                User.password = hashed_password
                verification_code = generate_verification_code()
                expiration_time = generate_expiration_time()
                User.verification_code = verification_code
                User.expiration_time = expiration_time
                User.is_verified = False
                print("data", User.verification_code)
                send_verification_email(User.email, User.verification_code)
                user = jsonable_encoder(User)
                print(user)
                new_user = await add_user(user)
                return ResponseModel(new_user, status.HTTP_201_CREATED, "Utilisateur ajouté avec succès")
            else:
                return ResponseModel("", status.HTTP_400_BAD_REQUEST, "Le mot de passe doit être fort, avec au moins 8 caractères, une lettre majuscule, un chiffre et un caractère spécial.")
        else:
            return ResponseModel("", status.HTTP_400_BAD_REQUEST, "Le numéro de téléphone est incorrect.")
    except Exception as ex:
        return ErrorResponseModel(str(ex), status.HTTP_500_INTERNAL_SERVER_ERROR, "Une erreur s'est produite lors de la création du client.")


# route de vérification d'un utilisateur à l'aide d'un code
@router.post("/verify")
async def verify_user(verification: UserVerification):
    verification_code = verification.verification_code
    user = await Users_collection.find_one({"verification_code": verification_code, "is_verified": False})
    if user:
        userData = Users(**user)
        await Users_collection.update_one(
            {"verification_code": verification_code, "is_verified": False},
            {"$set": {"is_verified": True}}
        )
        if datetime.now() <= userData.expiration_time:
            return {"message": "Connexion réussi"}
        else:
            return ResponseModel("", status.HTTP_401_UNAUTHORIZED, "Code de vérification expiré")
    else:
        return ResponseModel("", status.HTTP_400_BAD_REQUEST, "Code de vérification invalide")


@router.post("/refresh-code")
async def refresh_code(username: str, email:str):
    username_exists = await check_user_existence(username,email)
    if username_exists:
        new_verification_code = await regenerate_verification_code(username)

        if new_verification_code is None:
            raise HTTPException(status_code=401, detail="Compte déja vérifié")
        return ResponseModel("", status.HTTP_200_OK, "Nouveau code de vérification généré avec succès")
    else:
        return ResponseModel("", status.HTTP_404_NOT_FOUND, "Utilisateur non trouvé")


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    customer = await authenticate_user(form_data.username, form_data.password)
    # print(customer.is_verified)
    if customer is None:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    # print(customer.is_verified)
    if customer.is_verified == True:
        customer_info = {
            "name": customer.name,
            "firstName": customer.firstName,
            "username": customer.username,
            "phone": customer.phone,
            "address": customer.address,
            "is_verified": customer.is_verified,
            "email": customer.email,
        }
        # Création d'un refresh token
        refresh_token_expires = timedelta(days=5)
        refresh_token = create_refresh_token(
            data={"sub": customer_info}, expires_delta=refresh_token_expires
        )

        # création d'un JWT avec une durée d'expiration
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": customer_info}, expires_delta=access_token_expires)

        return {"access_token": access_token, "refresh_token": refresh_token}
    else:
        return HTTPException(status_code=401, detail="Compte non vérifier")


# route pour avoir la liste des utilisateurs
@router.get("/allUser", response_description="users récupéré")
async def get_user():
    users = await all_user()
    if users:
        return ResponseModel(users, status.HTTP_200_OK, "Liste des utilisateurs renvoyés")
    return ResponseModel(users, status.HTTP_200_OK, "Liste vide renvoyé")
