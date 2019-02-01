from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def create(self, msg: str):
        raise NotImplementedError

    @abstractmethod
    def has(self, msg: str):
        raise NotImplementedError

class Service(ABC):
    @abstractmethod
    def echo(self, msg: str) -> str:
        raise NotImplementedError
