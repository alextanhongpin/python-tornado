from service.echo.interface import Service, Repository

class ServiceImpl(Service):
    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def echo(self, msg: str) -> str:
        if not msg or self.repo.has(msg):
            return self.repo.get_all()
        self.repo.create(msg)
        return self.repo.get_all()
