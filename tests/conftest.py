import faker
import pytest
from waiting import wait

from orders_client.client import OrdersClient
from orders_client.models import OrderRequestDTO


def pytest_addoption(parser):
    parser.addoption(
        "--host", default="http://backend", action="store", help="host"
    )
    parser.addoption("--port", default="5000", action="store", help="port")


@pytest.fixture()
def host(request) -> str:
    return request.config.getoption("--host")


@pytest.fixture()
def port(request) -> str:
    return request.config.getoption("--port")


@pytest.fixture()
def orders_client(host, port) -> OrdersClient:
    client = OrdersClient(host, port)
    wait(client.check_health, timeout_seconds=30, expected_exceptions=Exception)
    return client


@pytest.fixture()
def order_dto(fake):
    return OrderRequestDTO(stocks=fake.currency()[0], quantity=fake.pydecimal())


@pytest.fixture()
def fake() -> faker.Faker:
    return faker.Faker()
