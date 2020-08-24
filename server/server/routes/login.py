'''
The login endpoint of the service
'''

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..auth import oauth2_scheme, fake_hash_password
from ..app.models.user import User, UserInDB

router = APIRouter()

fake_users_db = {
    'johndoe': {
        'user_email': 'johndoe',
        'hashed_password': 'password1',
        'disabled': False
    },
    'alice': {
        'user_email': 'alice',
        'hashed_password': 'password2',
        'disabled': True
    }
}

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user

async def generate_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return user

async def generate_current_active_user(current_user: User = Depends(generate_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')
    print('OleOleOle')
    print(current_user)
    return current_user

@router.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail='Incorrect username or password')

    return {'access_token': user.user_email, 'token_type': 'bearer'}

@router.get('/logins/me')
async def get_current_user(current_user: User = Depends(generate_current_active_user)):
    '''
    Return current user
    '''
    print('YoYoYo')
    return current_user