from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from ..core.data import default_customers
from ..core.models import CartLine, Customer, OrderRecord, Product, PrologDataset, Quote, QuoteLine, round2


class CommerceService:
    def __init__(self, dataset: PrologDataset) -> None:
        self._customers: Dict[int, Customer] = {customer.id: customer for customer in default_customers()}
        self._baseline_products = {product_id: product.copy() for product_id, product in dataset.products.items()}
        self._products = {product_id: product.copy() for product_id, product in dataset.products.items()}
        self._category_discounts = dict(dataset.category_discounts)
        self._loyalty_discounts = dict(sorted(dataset.loyalty_discounts.items()))
        self._shipping_costs = dict(dataset.shipping_costs)
        self._orders: List[OrderRecord] = []

        self._started_at = self._now_utc()
        self._request_count = 0
        self._quote_count = 0
        self._order_count = 0
        self._errors = 0
        self._revenue = 0.0
        self._discounts = 0.0

    def health(self) -> dict:
        self._request_count += 1
        return {
            "status": "ok",
            "service": "polyglot-commerce-integration-hub",
            "startedAt": self._started_at,
            "timestamp": self._now_utc(),
        }

    def integration_status(self, root: Path) -> dict:
        self._request_count += 1
        return self._integration_payload(root)

    def _integration_payload(self, root: Path) -> dict:
        legacy_dir = root / "legacy" / "academic_project"
        return {
            "javaLegacy": (legacy_dir / "Main.java").exists(),
            "ocamlLegacy": (legacy_dir / "main.ml").exists(),
            "prologRules": (legacy_dir / "store.pl").exists(),
            "legacyPath": str(legacy_dir),
        }

    def list_customers(self) -> List[dict]:
        self._request_count += 1
        return self._customers_payload()

    def _customers_payload(self) -> List[dict]:
        return [
            {
                "id": customer.id,
                "name": customer.name,
                "district": customer.district,
                "loyaltyYears": customer.loyalty_years,
            }
            for customer in self._customers.values()
        ]

    def list_products(self) -> List[dict]:
        self._request_count += 1
        return self._products_payload()

    def _products_payload(self) -> List[dict]:
        return [
            {
                "id": product.id,
                "name": product.name,
                "category": product.category,
                "price": round2(product.price),
                "stock": product.stock,
                "categoryDiscount": self._category_discounts.get(product.category.lower(), 0.0),
                "lowStock": product.stock <= 5,
            }
            for product in self._products.values()
        ]

    def list_orders(self) -> List[dict]:
        self._request_count += 1
        return self._orders_payload()

    def _orders_payload(self) -> List[dict]:
        return [self._order_to_dict(order) for order in self._orders]

    def metrics(self) -> dict:
        self._request_count += 1
        return self._metrics_payload()

    def _metrics_payload(self) -> dict:
        avg_order_value = self._revenue / self._order_count if self._order_count else 0.0
        return {
            "startedAt": self._started_at,
            "timestamp": self._now_utc(),
            "requests": self._request_count,
            "quotes": self._quote_count,
            "orders": self._order_count,
            "errors": self._errors,
            "revenue": round2(self._revenue),
            "discounts": round2(self._discounts),
            "avgOrderValue": round2(avg_order_value),
            "inventoryCount": sum(product.stock for product in self._products.values()),
        }

    def dashboard(self, root: Path) -> dict:
        self._request_count += 1
        return {
            "metrics": self._metrics_payload(),
            "customers": self._customers_payload(),
            "inventory": self._products_payload(),
            "recentOrders": self._orders_payload()[:5],
            "integration": self._integration_payload(root),
        }

    def quote(self, customer_id: int, lines: List[CartLine]) -> dict:
        self._request_count += 1
        try:
            quote = self._build_quote(customer_id, lines, apply_stock=False)
            self._quote_count += 1
            return {
                "message": "Quote generated successfully",
                "quote": self._quote_to_dict(quote),
                "inventory": self.list_products(),
            }
        except ValueError:
            self._errors += 1
            raise

    def create_order(self, customer_id: int, lines: List[CartLine]) -> dict:
        self._request_count += 1
        try:
            quote = self._build_quote(customer_id, lines, apply_stock=True)
            order_id = f"ORD-{self._order_count + 1:05d}"
            customer = self._customers[customer_id]
            record = OrderRecord(
                order_id=order_id,
                timestamp_utc=self._now_utc(),
                customer=customer,
                lines=lines,
                quote=quote,
            )
            self._orders.insert(0, record)

            self._order_count += 1
            self._revenue += quote.total
            self._discounts += quote.category_discount + quote.loyalty_discount

            return {
                "message": "Order registered successfully",
                "order": self._order_to_dict(record),
                "inventory": self.list_products(),
            }
        except ValueError:
            self._errors += 1
            raise

    def reset(self) -> dict:
        self._request_count += 1
        self._products = {product_id: product.copy() for product_id, product in self._baseline_products.items()}
        self._orders.clear()
        self._quote_count = 0
        self._order_count = 0
        self._errors = 0
        self._revenue = 0.0
        self._discounts = 0.0
        self._started_at = self._now_utc()

        return {
            "message": "Session reset completed",
            "inventory": self.list_products(),
        }

    def _build_quote(self, customer_id: int, lines: List[CartLine], apply_stock: bool) -> Quote:
        if not lines:
            raise ValueError("At least one line item is required.")

        if customer_id not in self._customers:
            raise ValueError(f"Customer not found: {customer_id}")

        customer = self._customers[customer_id]
        quote_lines: List[QuoteLine] = []
        subtotal = 0.0
        category_discount = 0.0

        for line in lines:
            if line.quantity <= 0:
                raise ValueError(f"Quantity must be > 0 for item {line.item_id}")
            product = self._products.get(line.item_id)
            if not product:
                raise ValueError(f"Product not found: {line.item_id}")
            if line.quantity > product.stock:
                raise ValueError(f"Insufficient stock for item {line.item_id}; available {product.stock}")

            line_subtotal = product.price * line.quantity
            subtotal += line_subtotal

            discount_rate = self._category_discounts.get(product.category.lower(), 0.0)
            category_discount += line_subtotal * discount_rate

            quote_lines.append(
                QuoteLine(
                    item_id=product.id,
                    item_name=product.name,
                    category=product.category,
                    quantity=line.quantity,
                    unit_price=round2(product.price),
                    line_subtotal=round2(line_subtotal),
                )
            )

        loyalty_rate = self._loyalty_rate(customer.loyalty_years)
        loyalty_discount = (subtotal - category_discount) * loyalty_rate
        shipping = self._shipping_costs.get(customer.district.lower(), 8.0)
        total = subtotal - category_discount - loyalty_discount + shipping

        if apply_stock:
            for line in lines:
                self._products[line.item_id].stock -= line.quantity

        return Quote(
            customer_id=customer.id,
            customer_name=customer.name,
            lines=quote_lines,
            subtotal=round2(subtotal),
            category_discount=round2(category_discount),
            loyalty_discount=round2(loyalty_discount),
            shipping_cost=round2(shipping),
            total=round2(total),
        )

    def _loyalty_rate(self, years: int) -> float:
        applicable = [threshold for threshold in self._loyalty_discounts if years >= threshold]
        if not applicable:
            return 0.0
        return self._loyalty_discounts[max(applicable)]

    def _quote_to_dict(self, quote: Quote) -> dict:
        return {
            "customerId": quote.customer_id,
            "customerName": quote.customer_name,
            "lines": [
                {
                    "itemId": line.item_id,
                    "itemName": line.item_name,
                    "category": line.category,
                    "quantity": line.quantity,
                    "unitPrice": line.unit_price,
                    "lineSubtotal": line.line_subtotal,
                }
                for line in quote.lines
            ],
            "subtotal": quote.subtotal,
            "categoryDiscount": quote.category_discount,
            "loyaltyDiscount": quote.loyalty_discount,
            "shippingCost": quote.shipping_cost,
            "total": quote.total,
        }

    def _order_to_dict(self, order: OrderRecord) -> dict:
        return {
            "orderId": order.order_id,
            "timestampUtc": order.timestamp_utc,
            "customer": {
                "id": order.customer.id,
                "name": order.customer.name,
                "district": order.customer.district,
                "loyaltyYears": order.customer.loyalty_years,
            },
            "lines": [{"itemId": line.item_id, "quantity": line.quantity} for line in order.lines],
            "quote": self._quote_to_dict(order.quote),
        }

    @staticmethod
    def _now_utc() -> str:
        return datetime.now(timezone.utc).isoformat()
