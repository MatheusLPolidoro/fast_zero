from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act (Agir)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmar)
    assert response.json() == {'message': 'olá mundo!'}  # Assert (Afirmar)


def test_html_deve_retornar_ok_e_pagina_html(client):
    response = client.get('/html')

    assert response.status_code == HTTPStatus.OK
    assert (
        response.text
        == """
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
    )
