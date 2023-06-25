import allure
from requests import Response
from requests import Session
from typing import List, Union, Dict

from .models import OrderResponseDTO, OrderRequestDTO


def check_for_errors(resp: Response, *args, **kwargs):
    with allure.step(f"Executing {resp.request.method} request to {resp.request.url}"):
        request_body = resp.request.body or ""
        request_body = request_body if isinstance(request_body, str) else request_body.decode()
        allure.attach(request_body, "Request body")
        allure.attach(resp.text, "Response body")
        allure.attach(str(resp.status_code), "Response status code")
    resp.raise_for_status()


class OrdersApi:
    def __init__(self, session: Session, base: str):
        self.base = f"{base}/orders"
        self.session = session
        self.session.hooks["response"] = check_for_errors

    def post(self, order: Union[OrderRequestDTO, Dict]) -> str:
        order_body = order if isinstance(order, dict) else order.dict()
        return self.session.post(self.base, json=order_body).json()["id"]

    def get_all(self) -> List[OrderResponseDTO]:
        return [OrderResponseDTO(**kw) for kw in self.session.get(self.base).json()]

    def get_by_id(self, order_id) -> OrderResponseDTO:
        return OrderResponseDTO(**self.session.get(f"{self.base}/{order_id}").json())

    def delete(self, order_id):
        return self.session.delete(f"{self.base}/{order_id}").text


class OrdersClient:
    def __init__(self, host, port):
        self.base = f"{host}:{port}"
        self.session = Session()

    def check_health(self):
        return self.session.get(f"{self.base}/healthcheck")

    @property
    def orders(self):
        return OrdersApi(self.session, self.base)
