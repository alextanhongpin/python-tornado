from service.echo.interface import Repository

class RepositoryImpl(Repository):
    _msg = ''
    def get_msg(self):
        return self._msg

    def set_msg(self, msg: str):
        self._msg = msg
