from pathlib import Path

from polyglot_commerce.core.data import load_prolog_dataset


def test_load_prolog_dataset_parses_expected_sections() -> None:
    source = Path("legacy/academic_project/store.pl")
    dataset = load_prolog_dataset(source)

    assert len(dataset.products) >= 5
    assert "potions" in dataset.category_discounts
    assert any(year >= 1 for year in dataset.loyalty_discounts)
    assert "lisboa" in dataset.shipping_costs
