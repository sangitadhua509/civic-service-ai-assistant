"""
Generates a human-readable, guaranteed-unique reference number for a
service application. We deliberately generate this AFTER the row has
already been inserted and has a real database id — using the id
guarantees uniqueness for free (no risk of two applications getting
the same reference number), instead of relying on a timestamp or
random string that could theoretically collide.

Format: SA-000123 (SA = Service Application, then the id zero-padded
to 6 digits). A citizen reading this out over the phone can say
"SA dash zero zero zero one two three" unambiguously.
"""


def generate_reference_no(application_id: int) -> str:
    return f"SA-{application_id:06d}"
