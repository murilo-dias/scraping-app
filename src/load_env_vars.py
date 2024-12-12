import os
from dotenv import load_dotenv

load_dotenv()


def load_env_vars():
    LATITUDE = os.getenv("LATITUDE")
    LONGITUDE = os.getenv("LONGITUDE")
    URL_SITE = os.getenv("URL_SITE")
    URL_WEBHOOK = os.getenv("URL_WEBHOOK")

    if not LATITUDE or not LONGITUDE or not URL_SITE or not URL_WEBHOOK:
        raise ValueError("Uma ou mais variáveis de ambiente estão ausentes.")

    return LATITUDE, LONGITUDE, URL_SITE, URL_WEBHOOK
