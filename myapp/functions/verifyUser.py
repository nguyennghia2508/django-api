from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import TokenError, AccessToken
from django.conf import settings
import jwt
from ..db_connection import db
import os
from dotenv import load_dotenv

load_dotenv()

def token_decode(request):
    authorization_header = request.headers.get('Authorization')

    if authorization_header:
        try:
            token = authorization_header.split(' ')[1]
            decoded_token = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
            return decoded_token
        except TokenError as e:
            # Handle token errors appropriately
            return False
        except jwt.DecodeError as e:
            # Handle decode errors appropriately
            return False
    else:
        return False

def verify_token(request):
    decoded_token = token_decode(request)

    if decoded_token:
        user_id = decoded_token.get('id')
        try:
            user = db['user'].find_one({'_id': user_id})
            request.user = user
            return True
        except user.DoesNotExist:
            return False
    else:
        return False
