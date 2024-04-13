import motor.motor_asyncio
from repository.user_repository import (UserRepository)
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from passlib.context import CryptContext
import phonenumbers
from decouple import config
from config import SECRET_KEY, ALGORITHM
from passlib.context import CryptContext
import jwt
import time


MONGO_DETAILS = config('MONGO_DETAILS')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.Users
Users_collection = database.get_collection("users_collection")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# fonction pour générer un code de vérification
def generate_verification_code():
    return str(random.randint(1000, 9999))


# fonction pour la date d'expiration du code
def generate_expiration_time():
    return datetime.now() + timedelta(minutes=1)


# fonction pour envoyer un email avec le code
def send_verification_email(recipient_email, verification_code):
    subject = "Vérification de votre compte"
    message = f"Votre code de vérification est : {verification_code}"
    sender_email = "savanehassansy@gmail.com"
    sender_password = "jgcs ptdf pzou qqag"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
    except Exception as e:
        print("Erreur d'envoi d'e-mail :", str(e))


def validate_password_strength(password):
    if (
        len(password) < 8 or
        not any(char.isupper() for char in password) or
        not any(char.isdigit() for char in password) or
        not any(char in "!@#$%^&*£µ(),._?\":{}|<>" for char in password)
    ):
        raise ValueError(
            "Le mot de passe doit être fort, avec au moins 8 caractères, une lettre majuscule, un chiffre et un caractère spécial.")
    return password


def is_password_strong(password):
    try:
        validate_password_strength(password)
        return True
    except ValueError:
        return False


def check_phone_numbers(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if phonenumbers.is_valid_number(parsed_number):
            return True
        else:
            return False
    except phonenumbers.phonenumberutil.NumberFormatException:
        print("Format de numéro de téléphone incorrect.")


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}


async def check_user_existence(username,email):
    existing_user = await Users_collection.find_one({"username": username})
    existing_user_email = await Users_collection.find_one({"email": email})
    return existing_user is not None or existing_user_email is not None



async def regenerate_verification_code(username):
        # Générer un nouveau code de vérification et la nouvelle expiration
        new_verification_code = generate_verification_code() 
        new_expiration_time = generate_verification_code() 
        
        user_data = await Users_collection.find_one({"username":username})
        
        if user_data.get("is_verified") == False:
            await Users_collection.update_one(
                {"username": username},
                {"$set": {
                    "verification_code": new_verification_code,
                    "expiration_time": new_expiration_time
                }}
            )
            if user_data and user_data.get("email"):
                    send_verification_email(user_data["email"],new_verification_code)
            return new_verification_code
        else:
            return None

        
            

# récupérer les donnés de tout les utilisateur dans la base de donné
async def all_user():
    users = []
    async for data in Users_collection.find():
        users.append(UserRepository.UserDataView(data))
    return users


# enregisté un utilisateur dans la base de donné
async def add_user(user_data: dict) -> dict:
    users = await Users_collection.insert_one(user_data)
    users_data = await Users_collection.find_one({"_id": users.inserted_id})
    
    return UserRepository.UserData(users_data)
