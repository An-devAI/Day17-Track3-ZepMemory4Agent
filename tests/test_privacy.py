import pytest

from src.privacy_guard import can_write_type, minimize_pii, require_memory_consent


def test_synthetic_users_opt_in():
    assert require_memory_consent("minh-lab17")["memory_opt_in"] is True
    assert can_write_type("minh-lab17", "preference") is True


def test_pii_minimizer():
    text = minimize_pii("mail me at a.person@example.com or +84 912 345 678")
    assert "example.com" not in text
    assert "912" not in text


def test_unknown_user_is_denied():
    with pytest.raises(PermissionError):
        require_memory_consent("unknown-user")
