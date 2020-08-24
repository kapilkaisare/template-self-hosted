'''
The health endpoint of the service
'''

from fastapi import Depends, APIRouter

from ..auth import oauth2_scheme

router = APIRouter()

@router.get('/health/')
async def report_good_health(token: str = Depends(oauth2_scheme)):
    '''
    A dummy endpoint to prove that the service is up and running
    '''
    return {'name': 'project', 'status': 'healthy', 'token': token}