from polyglot_commerce.core.data import dataset_from_legacy
from polyglot_commerce.core.models import CartLine
from polyglot_commerce.engine.service import CommerceService


def test_quote_and_order_flow_updates_metrics_and_stock() -> None:
    service = CommerceService(dataset_from_legacy())

    quote = service.quote(1, [CartLine(item_id=1, quantity=2)])
    assert quote["quote"]["total"] > 0

    before_stock = next(item for item in service.list_products() if item["id"] == 1)["stock"]
    order = service.create_order(1, [CartLine(item_id=1, quantity=1)])
    assert order["order"]["orderId"].startswith("ORD-")

    after_stock = next(item for item in service.list_products() if item["id"] == 1)["stock"]
    assert after_stock == before_stock - 1

    metrics = service.metrics()
    assert metrics["orders"] == 1
    assert metrics["quotes"] >= 1
