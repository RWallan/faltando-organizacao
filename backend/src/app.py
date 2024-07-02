from fastapi import FastAPI

from src.routes import user_router

app = FastAPI()


@app.get('/')
def health_check():
    return {'status': 'ok'}


app.include_router(user_router)
