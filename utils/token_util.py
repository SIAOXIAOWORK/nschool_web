import jwt

def create_jwt(user_data):
    encoded_jwt = jwt.encode(user_data, "nschool", algorithm="HS256")
    return encoded_jwt

