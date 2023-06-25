import uuid

import allure
import pytest
import requests
from assertpy import assert_that
from waiting import wait


def test_create(orders_client, order_dto, fake):
    order_id = orders_client.orders.post(order_dto)
    order_after = orders_client.orders.get_by_id(order_id)
    with allure.step("Checking fields in created order"):
        assert_that(order_after.dict()) \
            .has_quantity(order_dto.quantity) \
            .has_stocks(order_dto.stocks) \
            .has_id(order_id)
        assert_that(["pending", "executed", "canceled"]).contains(order_after.status)


def test_delete(orders_client, fake, order_dto):
    order_id = orders_client.orders.post(order_dto)
    orders_client.orders.delete(order_id)
    with allure.step("Check for 404 status when trying to request deleted order"):
        with pytest.raises(requests.exceptions.HTTPError) as err:
            orders_client.orders.get_by_id(order_id)
        assert_that(err.value.response.status_code).is_equal_to(404)
    with allure.step("Check that list of all orders doesn't contain deleted order"):
        assert_that([*map(lambda x: x.dict(), orders_client.orders.get_all())]
                    ).extracting("id").does_not_contain(order_id)


def test_statuses(orders_client, order_dto):
    order_id = orders_client.orders.post(order_dto)
    with allure.step("wait for order to be executed"):
        wait(lambda: orders_client.orders.get_by_id(order_id).status == "executed", timeout_seconds=30)


def test_delete_non_existent(orders_client, fake):
    with allure.step("Check that 404 status returned when deleting non-existent order"):
        with pytest.raises(requests.exceptions.HTTPError) as err:
            orders_client.orders.delete(str(uuid.uuid4()))
        assert_that(err.value.response.status_code).is_equal_to(404)


@pytest.mark.parametrize("order", (dict(stocks="AMD", quantity="invalid type"),
                                   dict(stocks=123.345, quantity=123.4),
                                   dict(quantity=123.4),
                                   dict(stocks="AMD")))
def test_create_negative_invalid_type(orders_client, order):
    with allure.step("Check that 422 status returned when creating order with invalid/missing fields"):
        with pytest.raises(requests.exceptions.HTTPError) as err:
            orders_client.orders.post(order)
        assert_that(err.value.response.status_code).is_equal_to(422)
