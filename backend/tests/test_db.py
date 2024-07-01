from sqlalchemy import select

from src.database.models import User


def test_create_user(session):
    new_user = User(name='Teste', email='test@test.com', password='test')

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.name == 'Teste'))

    assert user.name == 'Teste'
