"""
TEMPORARY STORAGE — Phase 2 only.

Real databases (PostgreSQL, coming in Phase 3) keep data on disk, so it
survives server restarts and can be safely shared between many users at
once. Right now we're just using plain Python dictionaries in memory,
which means: every time you stop and restart `uvicorn`, all this data
disappears. That's fine for Phase 2 — the point here is to learn how
the API endpoints behave, not to build permanent storage yet.

Each "table" is a dict of {id: record_dict}, plus a counter to hand out
the next id. This mimics what a real database's auto-increment primary
key does.
"""

departments: dict[int, dict] = {}
services: dict[int, dict] = {}
citizens: dict[int, dict] = {}

_next_department_id = 1
_next_service_id = 1
_next_citizen_id = 1


def next_department_id() -> int:
    global _next_department_id
    value = _next_department_id
    _next_department_id += 1
    return value


def next_service_id() -> int:
    global _next_service_id
    value = _next_service_id
    _next_service_id += 1
    return value


def next_citizen_id() -> int:
    global _next_citizen_id
    value = _next_citizen_id
    _next_citizen_id += 1
    return value
