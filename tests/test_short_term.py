from src.short_term import ShortTermMemory


def test_sliding_compaction_preserves_durable_constraint():
    memory = ShortTermMemory(strategy="sliding", max_recent_messages=4, pressure_tokens=99999)
    memory.add("user", "Constraint: REVIEW-DEADLINE-1600 is Friday at 16:00 and must not be forgotten.")
    for i in range(10):
        memory.add("assistant" if i % 2 else "user", f"filler turn {i}")
    text = memory.render()
    assert "REVIEW-DEADLINE-1600" in text
    assert "Friday" in text
    assert "16:00" in text
    assert memory.compactions > 0


def test_buffer_does_not_compact():
    memory = ShortTermMemory(strategy="buffer", max_recent_messages=2)
    for i in range(8):
        memory.add("user", f"message {i}")
    assert memory.compactions == 0
    assert "message 0" in memory.render()
