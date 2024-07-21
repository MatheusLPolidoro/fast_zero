from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_access_token, settings


def test_create_access_token():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data_claims=data)
    result = decode(
        token, settings.SECRETE_KEY, algorithms=[settings.ALGORITHM]
    )
    assert result['sub'] == data['sub']
    assert result['exp']


def test_get_current_user_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_jwt_wrong_user(client, user, token):
    data = {'sub': 'invalid-user@test.com'}
    token = create_access_token(data_claims=data)
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_jwt_not_sub(client, user):
    data = {'iss': 'test@test.com'}
    token = create_access_token(data_claims=data)
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
