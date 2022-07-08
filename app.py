from fastapi import FastAPI
from routes.user import user

app = FastAPI()

app.include_router(user)

#vai puxar user o user que é a aplicação