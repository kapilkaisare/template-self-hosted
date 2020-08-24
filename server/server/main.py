'''
Project Title
'''

from fastapi import FastAPI

from .routes import health, login

app = FastAPI()

app.include_router(health.router)
app.include_router(login.router)