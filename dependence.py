from core.mail import create_mail_instance
from models import AsyncSessionFactory


async def get_session():
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        await session.close()


async def get_mail():
    mail = create_mail_instance()
    yield mail
