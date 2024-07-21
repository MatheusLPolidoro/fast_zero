from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.routers import auth, todos, users
from fast_zero.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'olá mundo!'}


@app.get('/html/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_html():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <title>EXERCICIO HTML</title>
    </head>
    <body>
        <h1>Olá Mundo!</h1>
        <p>Aplicando na pratica o exercicio da aula 2</p>
    </body>
    </html>
    """
