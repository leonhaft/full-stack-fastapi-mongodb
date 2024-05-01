from typing import Optional, List, Union, Type
from app.core.config import settings
from app.__version__ import __version__
from motor import motor_asyncio, core
from beanie import View, init_beanie, Document

from pymongo.driver_info import DriverInfo

DRIVER_INFO = DriverInfo(name="full-stack-fastapi-mongodb", version=__version__)


class _MongoClientSingleton:
    mongo_client: motor_asyncio.AsyncIOMotorClient | None

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(_MongoClientSingleton, cls).__new__(cls)
            cls.instance.mongo_client = motor_asyncio.AsyncIOMotorClient(
                settings.MONGO_DATABASE_URI, driver=DRIVER_INFO
            )
        return cls.instance


def MongoDatabase() -> core.AgnosticDatabase:
    return _MongoClientSingleton().mongo_client[settings.MONGO_DATABASE]


async def init_MongoDatabase(models: Optional[List[Union[Type[Document], Type["View"], str]]] = None):
    db = _MongoClientSingleton().mongo_client[settings.MONGO_DATABASE]
    await init_beanie(database=db, document_models=models)


async def ping():
    await MongoDatabase().command("ping")


__all__ = ["MongoDatabase", "ping"]
