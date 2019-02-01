from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def get_msg(self):
        pass

    @abstractmethod
    def set_msg(self, msg: str):
        pass

class Service(ABC):
    @abstractmethod
    def echo(self, msg: str) -> str:
        return ''
