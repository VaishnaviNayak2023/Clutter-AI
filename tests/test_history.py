"""Tests for the history service."""

from src.ai_clutter_cleaner.services.history import ActionHistory, get_history, record_action


def test_record_action():
    """Test recording an action."""
    # Should not raise an exception
    record_action("move", "/source/path", "/dest/path")
    assert True


def test_get_history_singleton():
    """Test that get_history returns the same instance."""
    history1 = get_history()
    history2 = get_history()

    assert history1 is history2


def test_action_history_initialization():
    """Test ActionHistory initialization."""
    history = ActionHistory()
    assert history is not None


def test_get_recent_actions():
    """Test getting recent actions."""
    history = get_history()
    actions = history.get_recent_actions(limit=10)

    # Should return a list (even if empty)
    assert isinstance(actions, list)


def test_get_actions_by_type():
    """Test getting actions by type."""
    history = get_history()
    actions = history.get_actions_by_type("move")

    # Should return a list (even if empty)
    assert isinstance(actions, list)
