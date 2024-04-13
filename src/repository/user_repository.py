
class UserRepository:
    
    def UserData(data) -> dict:
        return {
            "id": str(data["_id"]),
            "name": data["name"],
            "firstName": data["firstName"],
            "username": data["username"],
            "address": data["address"],
            "phone": data["phone"],
            "email": data["email"],
            "password": data["password"],
            "expiration_time":data["expiration_time"],
            "is_verified": data["is_verified"]
        }
        
    def UserDataView(data) -> dict:
        return {
            "id": str(data["_id"]),
            "name": data["name"],
            "firstName": data["firstName"],
            "username": data["username"],
            "address": data["address"],
            "phone": data["phone"],
            "email": data["email"],
            "is_verified": data["is_verified"]
        }
