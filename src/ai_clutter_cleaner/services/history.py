"""Action history service."""

from typing import Literal

from src.ai_clutter_cleaner.database.repositories import FileRepository


class ActionHistory:
    """Track and manage file action history."""

    def __init__(self):
        self.repo = FileRepository()

    def record_action(
        self,
        action_type: Literal["move", "copy", "delete", "scan"],
        source_path: str,
        destination_path: str | None = None,
        status: Literal["pending", "completed", "failed"] = "completed",
        error_message: str | None = None,
    ) -> None:
        """
        Record a file action in the history.

        Args:
            action_type: Type of action
            source_path: Source file path
            destination_path: Destination path (if applicable)
            status: Action status
            error_message: Error message if failed
        """
        # This would insert into the file_actions table
        # For now, we'll implement basic tracking
        pass

    def get_recent_actions(self, limit: int = 50) -> list[dict]:
        """
        Get recent file actions.

        Args:
            limit: Maximum number of actions to return

        Returns:
            List of action dictionaries
        """
        # This would query the file_actions table
        # For now, return empty list
        return []

    def get_actions_by_type(self, action_type: str) -> list[dict]:
        """
        Get actions of a specific type.

        Args:
            action_type: Type of action to filter by

        Returns:
            List of action dictionaries
        """
        return []


# Global history instance
_history_instance: ActionHistory | None = None


def get_history() -> ActionHistory:
    """Get or create the global history instance."""
    global _history_instance
    if _history_instance is None:
        _history_instance = ActionHistory()
    return _history_instance


def record_action(
    action_type: str, source: str, destination: str | None = None
) -> None:
    """
    Record a file action in the history.

    Args:
        action_type: Type of action (move, copy, etc.)
        source: Source path
        destination: Destination path (if applicable)
    """
    history = get_history()
    history.record_action(action_type, source, destination)
