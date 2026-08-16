from src.router import route_query
from src.utils import load_dataset, load_knowledge


def test_groundtruth_covers_four_memory_layers():
    dataset = load_dataset()
    layers = {case["expected_layer"] for case in dataset["evaluations"]}
    assert {"short_term", "long_term", "episodic", "semantic", "mixed"}.issubset(layers)
    assert len(dataset["evaluations"]) >= 10


def test_user_isolation_case_exists():
    dataset = load_dataset()
    case = next(c for c in dataset["evaluations"] if c["id"] == "E09")
    assert case["user_id"] == "lan-lab17"
    assert "ORCHID-27" in case["must_not_contain"]


def test_semantic_markers_exist():
    docs = load_knowledge()
    text = "\n".join(str(x) for x in docs)
    assert "PAYMENT-RULE-3" in text
    assert "CONN-POOL-FIRST" in text


def test_router_can_select_multiple_layers():
    layers = route_query("Hay chon huong dan retry payment phu hop voi preference ca nhan")
    assert "semantic" in layers
    assert "long_term" in layers


def test_golden_set_is_twenty_cases_when_released():
    import pytest

    from src.utils import GOLDEN_PATH, load_golden_evaluations

    if not GOLDEN_PATH.exists():
        pytest.skip("golden_eval.json not released in this checkout")
    cases = load_golden_evaluations()
    assert len(cases) == 20
    assert [c["id"] for c in cases] == [f"G{i:02d}" for i in range(1, 21)]
    layers = {c["expected_layer"] for c in cases}
    assert {"short_term", "long_term", "episodic", "semantic", "mixed"}.issubset(layers)
