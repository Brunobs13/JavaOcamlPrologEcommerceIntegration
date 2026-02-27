from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

from .models import Customer, Product, PrologDataset

ITEM_PATTERN = re.compile(r"item\((\d+),\s*'([^']+)',\s*'([^']+)',\s*([0-9]+(?:\.[0-9]+)?),\s*(\d+)\)\.")
DISCOUNT_PATTERN = re.compile(r"discount\('([^']+)',\s*([0-9]+(?:\.[0-9]+)?)\)\.")
LOYALTY_PATTERN = re.compile(r"loyalty_discount\(([^,]+),\s*([0-9]+(?:\.[0-9]+)?)\)\.")
SHIPPING_PATTERN = re.compile(r"shipping_cost\('([^']+)',\s*([0-9]+(?:\.[0-9]+)?)\)\.")


def load_prolog_dataset(file_path: Path) -> PrologDataset:
    if not file_path.exists():
        raise FileNotFoundError(f"Prolog source not found: {file_path}")

    products: Dict[int, Product] = {}
    category_discounts: Dict[str, float] = {}
    loyalty_discounts: Dict[int, float] = {}
    shipping_costs: Dict[str, float] = {}

    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("%"):
            continue

        item_match = ITEM_PATTERN.fullmatch(line)
        if item_match:
            item_id = int(item_match.group(1))
            products[item_id] = Product(
                id=item_id,
                name=item_match.group(2),
                category=item_match.group(3).lower(),
                price=float(item_match.group(4)),
                stock=int(item_match.group(5)),
            )
            continue

        discount_match = DISCOUNT_PATTERN.fullmatch(line)
        if discount_match:
            category_discounts[discount_match.group(1).lower()] = float(discount_match.group(2))
            continue

        loyalty_match = LOYALTY_PATTERN.fullmatch(line)
        if loyalty_match:
            years_token = loyalty_match.group(1).strip()
            if years_token.startswith(">"):
                years = int(years_token.replace(">", "")) + 1
            else:
                years = int(years_token)
            loyalty_discounts[years] = float(loyalty_match.group(2))
            continue

        shipping_match = SHIPPING_PATTERN.fullmatch(line)
        if shipping_match:
            shipping_costs[shipping_match.group(1).lower()] = float(shipping_match.group(2))
            continue

    if not products:
        raise ValueError("No products parsed from Prolog file.")

    return PrologDataset(
        products=products,
        category_discounts=category_discounts,
        loyalty_discounts=loyalty_discounts,
        shipping_costs=shipping_costs,
    )


def default_customers() -> List[Customer]:
    return [
        Customer(1, "Ana Silva", "Aveiro", 2),
        Customer(2, "Bruno Costa", "Lisboa", 4),
        Customer(3, "Carla Martins", "Porto", 6),
        Customer(4, "Diogo Pereira", "Aveiro", 1),
        Customer(5, "Eva Rocha", "Lisboa", 8),
    ]


def dataset_from_legacy() -> PrologDataset:
    root = Path(__file__).resolve().parents[3]
    return load_prolog_dataset(root / "legacy" / "academic_project" / "store.pl")
