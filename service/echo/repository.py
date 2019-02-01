from service.echo.interface import Repository

class RepositoryImpl(Repository):
    __msgs = []
    def get_all(self):
        return self.__msgs

    def create(self, msg: str):
        self.__msgs.append(msg)

    def has(self, msg: str) -> bool:
        return msg in self.__msgs
