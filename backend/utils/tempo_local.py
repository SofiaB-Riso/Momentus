import os
from datetime import datetime
from zoneinfo import ZoneInfo


def fuso_local():
    return ZoneInfo(os.getenv("APP_TIMEZONE", "America/Sao_Paulo"))


def agora_local():
    return datetime.now(fuso_local()).replace(tzinfo=None)
