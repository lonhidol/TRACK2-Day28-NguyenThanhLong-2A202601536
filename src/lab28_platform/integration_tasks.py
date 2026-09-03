"""Four student-owned boundaries used by the live platform.

Run ``uv run pytest starter-tests -q`` while completing these functions.  Do
not change their signatures: Kafka, Delta, Feast and ``/ready`` call them.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from lab28_platform.contracts import IngestionEvent


def event_headers(
    traceparent: str | None, idempotency_key: str
) -> list[tuple[str, bytes]]:
    """Return byte-valued Kafka headers for trace and replay correlation.

    ``idempotency-key`` is always required.  Omit ``traceparent`` when no trace
    is active rather than sending an empty, invalid W3C header.
    """
    headers = [("idempotency-key", idempotency_key.encode())]
    if traceparent:
        headers.append(("traceparent", traceparent.encode()))
    return headers


def dedupe_latest(events: Iterable[IngestionEvent]) -> list[IngestionEvent]:
    """Return one newest event per idempotency key, in deterministic key order.

    Compare ``(occurred_at, event_id)`` so ties do not depend on Kafka delivery
    order.  The Spark Delta MERGE calls this through ``delta_store``.
    """
    seen: dict[str, IngestionEvent] = {}
    for event in events:
        key = event.idempotency_key
        if key not in seen:
            seen[key] = event
        else:
            is_newer = (event.occurred_at, event.event_id) > (
                seen[key].occurred_at, seen[key].event_id
            )
            if is_newer:
                seen[key] = event
    return [seen[k] for k in sorted(seen.keys())]


def feast_online_request(asker_id: str) -> dict[str, Any]:
    """Build the Feast ``/get-online-features`` request for ``asker_activity_v1``."""
    from lab28_platform.contracts import FEATURE_REFS
    return {
        "entities": {"asker_id": [asker_id]},
        "features": list(FEATURE_REFS),
        "full_feature_names": False,
    }


def readiness_status(probes: Iterable[dict[str, Any]]) -> str:
    """Return ``ready``, ``degraded`` or ``not_ready`` from probe severity."""
    mandatory_failed = False
    optional_failed = False
    for probe in probes:
        if not probe["ready"]:
            if probe.get("mandatory", True):
                mandatory_failed = True
            else:
                optional_failed = True
    if mandatory_failed:
        return "not_ready"
    elif optional_failed:
        return "degraded"
    return "ready"
