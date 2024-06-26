from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='matt', password='senha_muito_boa', email='matt@exemple.com'
    )
    # unity of work
    session.add(user)  # criação de espaço na memoria
    session.commit()  # pega todas as alterações feitas e as efetiva
    # session.refresh(user)  # faz a sincronizaçãodos dados com o banco
    session.scalar(select(User).where(User.email == 'matt@exemple.com'))

    assert user.id == 1
    assert user.username == 'matt'
