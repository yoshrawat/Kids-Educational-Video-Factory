# domain/interfaces/publisher_provider.py
from abc import ABC, abstractmethod


class PublisherProvider(ABC):

    @abstractmethod
    async def upload(self, path: str, title: str, description: str):
        pass