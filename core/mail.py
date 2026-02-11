from fastapi_mail import FastMail
from pydantic import SecretStr

from config.setting import settings


def create_mail_instance() -> FastMail:
    """创建 FastMail 实例"""
    mail_config = {
        "MAIL_USERNAME": settings.MAIL_USERNAME,
        "MAIL_PASSWORD": SecretStr(settings.MAIL_PASSWORD),
        "MAIL_FROM": settings.MAIL_FROM,
        "MAIL_PORT": settings.MAIL_PORT,
        "MAIL_SERVER": settings.MAIL_SERVER,
        "MAIL_FROM_NAME": settings.MAIL_FROM_NAME,
        "MAIL_STARTTLS": settings.MAIL_STARTTLS,
        "MAIL_SSL_TLS": settings.MAIL_SSL_TLS,
        "USE_CREDENTIALS": settings.USE_CREDENTIAL,
        "VALIDATE_CERTS": settings.VALIDATE_CERTS
    }
    return FastMail(mail_config)
