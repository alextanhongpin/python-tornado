from service.echo.interface import Service, Repository

class ServiceImpl(Service):
    def __init__(self, repo: Repository): 
        self.repo = repo

    def echo(self, msg: str) -> str:
        result = self.repo.get_msg()
        if not result:
            self.repo.set_msg(msg)
            return self.repo.get_msg()
        return result
