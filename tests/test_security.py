from jwt import decode

from fast_zero.security import ALGORITHM, SECRETE_KEY, create_access_token


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data_claims=data)
    result = decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
    assert result['sub'] == data['sub']
    assert result['exp']
