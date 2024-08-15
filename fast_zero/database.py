from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.settings import Settings

# Certifique-se de que a URL do banco de dados seja uma string
database_url = Settings().DATABASE_URL

if isinstance(database_url, bytes):
    database_url = database_url.decode('utf-8')

engine = create_engine(database_url)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
