from fastapi import FastAPI
from mangum import Mangum


import jwt
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .api.endpoints.model import User, User_Pydantic, UserIn_Pydantic
from .api.endpoints.auth import authenticate_user, JWT_SECRET
from passlib.hash import bcrypt     


from tortoise.contrib.fastapi import register_tortoise

from .api.api import router as api_router

app = FastAPI(title='Colibri api')
@app.get("/",  tags=["Endpoint Test"])
def main_endpoint_test():
    return {"message": "Welcome to API COLIBRI"}


@app.post('/token', tags=["Authentication"])
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(username=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail='invalid username or password'
                )

    user_obj = await User_Pydantic.from_tortoise_orm(user)

    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return {'access_token' : token, 'token_type': 'bearer'}

app.include_router(api_router, prefix="/api")


register_tortoise(
        app, 
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.api.endpoints.model']},
        generate_schemas=True,
        add_exception_handlers=True

    )


# to make it work with Amazon Lambda, we create a handler object
#handler = Mangum(app=app)

