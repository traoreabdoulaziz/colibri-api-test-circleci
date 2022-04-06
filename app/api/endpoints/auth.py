#This file is responsible to create all functions use to authentication


import jwt
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .model import User, User_Pydantic, UserIn_Pydantic 
from passlib.hash import bcrypt     
from ..config.auth import JWT_SECRET,ACCESS_TOKEN_EXPIRE_MINUTES

auth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')






async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_passsword(password=password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user =  await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='invalid username or password'
        )
    
    return await User_Pydantic.from_tortoise_orm(user)





# @auth_router.get('/token', tags=["Authentication"])
# async def index(token: str = Depends(oauth2_scheme)):
#     return {'the_token' : token}



@auth_router.post('/users', response_model=User_Pydantic, tags=["Users"], include_in_schema=False)#
async def create_user(user: UserIn_Pydantic):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)


# @auth_router.get('/users/me', tags=["Users"], include_in_schema=False)
# async def get_user(user: User_Pydantic = Depends(get_current_user)):
#     return user