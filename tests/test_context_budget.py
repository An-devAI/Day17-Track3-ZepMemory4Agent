from src.context_budget import ContextBudgetManager


def test_teaching_budget_ratios():
    manager = ContextBudgetManager(10000)
    assert manager.layer_limit("short_term") == 1000
    assert manager.layer_limit("long_term") == 400
    assert manager.layer_limit("episodic") == 300
    assert manager.layer_limit("semantic") == 300


def test_assemble_preserves_priority_order():
    manager = ContextBudgetManager(1000)
    merged, breakdown = manager.assemble(
        {
            "semantic": "semantic evidence",
            "episodic": "episode evidence",
            "long_term": "profile evidence",
            "short_term": "recent evidence",
        }
    )
    assert merged.index("<SHORT_TERM>") < merged.index("<LONG_TERM>")
    assert merged.index("<LONG_TERM>") < merged.index("<EPISODIC>")
    assert merged.index("<EPISODIC>") < merged.index("<SEMANTIC>")
    assert set(breakdown) == {"short_term", "long_term", "episodic", "semantic"}
