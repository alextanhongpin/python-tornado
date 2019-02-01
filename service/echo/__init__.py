from service.echo.interface import Service, Repository
from service.echo.service import ServiceImpl
from service.echo.repository import RepositoryImpl

def make_service() -> Service:
    repo = RepositoryImpl()
    service = ServiceImpl(repo)
    return service 
