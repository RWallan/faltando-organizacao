from fastapi import FastAPI

from src import routes

app = FastAPI()


@app.get('/')
def health_check():
    return {'status': 'ok'}


app.include_router(routes.user_router)
app.include_router(routes.auth_router)
