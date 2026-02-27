from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Customer:
    id: int
    name: str
    district: str
    loyalty_years: int


@dataclass
class Product:
    id: int
    name: str
    category: str
    price: float
    stock: int

    def copy(self) -> "Product":
        return Product(
            id=self.id,
            name=self.name,
            category=self.category,
            price=self.price,
            stock=self.stock,
        )


@dataclass(frozen=True)
class CartLine:
    item_id: int
    quantity: int


@dataclass(frozen=True)
class QuoteLine:
    item_id: int
    item_name: str
    category: str
    quantity: int
    unit_price: float
    line_subtotal: float


@dataclass(frozen=True)
class Quote:
    customer_id: int
    customer_name: str
    lines: List[QuoteLine]
    subtotal: float
    category_discount: float
    loyalty_discount: float
    shipping_cost: float
    total: float


@dataclass(frozen=True)
class OrderRecord:
    order_id: str
    timestamp_utc: str
    customer: Customer
    lines: List[CartLine]
    quote: Quote


@dataclass(frozen=True)
class PrologDataset:
    products: Dict[int, Product]
    category_discounts: Dict[str, float]
    loyalty_discounts: Dict[int, float]
    shipping_costs: Dict[str, float]


def round2(value: float) -> float:
    return round(float(value), 2)
