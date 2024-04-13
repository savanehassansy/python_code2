from datetime import datetime

# from pytest_mock import mocker
import pytest
from pytest_mock import mocker
from services.user_service import (
    generate_expiration_time,generate_verification_code,check_phone_numbers,is_password_strong,
    validate_password_strength,add_user,
    send_verification_email
)

def test1():
    current_tme = datetime.now()
    result = generate_expiration_time()
    assert isinstance(result, datetime) #vérification si result est du format datetime
    assert result > current_tme #vérifions si result est supéieur par rapport a current_time
    
    
def test2():
    code = generate_verification_code()
    assert len(code) == 4  #vérifions si code a une longueur est égal à 4
    assert code.isdigit()  #vérifions si code est composé de chiffre
    
def test3():
    result = is_password_strong(password="Azerty@10")
    assert result == True


# Vérification du numéro de téléphone
def test4():
    result = check_phone_numbers(phone_number="+2250787050192")
    assert result == True
    
def test5():
    result = validate_password_strength(password="Azerty@10")
    assert result == 'Azerty@10'
    


def test_send_verification_email(mocker):
    # Configuration du mock pour smtplib.SMTP
    smtp_mock = mocker.patch("smtplib.SMTP")
    smtp_instance = smtp_mock.return_value

    # Appels de la fonction send_verification_email
    recipient_email = "savanehassansy09@gmail.com.com"
    verification_code = "1234"

    send_verification_email(recipient_email, verification_code)

    # Vérifications
    smtp_mock.assert_called_once_with('smtp.gmail.com', 587)
    

@pytest.mark.asyncio
async def test_add_customer():
    customer_data = {
            "name": "john_doe",
            "firstName": "John",
            "address": "123 Main St",
            "phone": "555-555-5555",
            "email": "john@example.com",
            "password": "hashed_password",
            "role": False
        }
    
    result = await add_user(customer_data)
    assert result.name == customer_data["name"]
    assert result.email == customer_data["email"]