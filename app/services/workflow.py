"""
This file is the single source of truth for "what status changes are
allowed." Instead of letting an officer set ANY status on ANY
application (which could let "submitted" jump straight to "approved"
with no review step, or bounce back and forth forever), we define
exactly which moves are legal as a dictionary: current status -> set
of statuses it's allowed to move to next.

If a status isn't a key here at all (or the target isn't in its set),
the move is rejected. An empty set means "this is a final status —
nothing can change it anymore."
"""

from fastapi import HTTPException, status as http_status

APPLICATION_TRANSITIONS: dict[str, set[str]] = {
    "submitted": {"under_review", "rejected"},
    "under_review": {"approved", "rejected"},
    "approved": set(),   # final
    "rejected": set(),   # final
}

GRIEVANCE_TRANSITIONS: dict[str, set[str]] = {
    "open": {"in_progress", "resolved"},
    "in_progress": {"resolved"},
    "resolved": set(),  # final
}


def validate_transition(current_status: str, new_status: str, allowed: dict[str, set[str]]) -> None:
    if new_status == current_status:
        return  # no-op, allow re-sending the same status without error

    valid_next_steps = allowed.get(current_status, set())
    if new_status not in valid_next_steps:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Cannot move from '{current_status}' to '{new_status}'. "
                f"Allowed next steps: {sorted(valid_next_steps) or 'none — this is a final status'}"
            ),
        )
