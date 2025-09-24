"""Tiny client for the Open 5e API."""

from __future__ import annotations

from typing import Any, Dict, Final, FrozenSet, Mapping

import httpx

# Module-level configuration:
DEFAULT_TIMEOUT: Final[float] = 10.0
DEFAULT_RETRIES: Final[int] = 3

# API endpoints:
SPELLS_URL: Final[str] = 'https://api.open5e.com/v2/spells/'
MONSTERS_URL: Final[str] = 'https://api.open5e.com/v1/monsters/'
MAGIC_ITEMS_URL: Final[str] = 'https://api.open5e.com/v1/magicitems/'

# Allowed filters:
SPELLS_FILTERS: Final[FrozenSet[str]] = frozenset((
    'name',
    'classes__name__in',
    'level',
    'level__range',
    'range',
    'range__range',
    'school__name',
    'school__name__in',
    'duration',
    'duration__in',
    'concentration',
    'verbal',
    'somatic',
    'material',
    'material_consumed',
    'casting_time',
))

MONSTERS_FILTERS: Final[FrozenSet[str]] = frozenset((
    'name',
    'name__icontains',
    'desc',
    'desc__icontains',
    'cr',
    'cr__range',
    'hit_points',
    'armor_class',
    'type',
    'type__contains',
    'size',
))

MAGIC_ITEMS_FILTERS: Final[FrozenSet[str]] = frozenset((
    'name',
    'name__icontains',
    'desc',
    'desc__contains',
    'type',
    'type__contains',
    'rarity',
    'requires_attunement',
))


def _only_allowed(
    filters: Mapping[str, Any],
    allowed: FrozenSet[str],
) -> Dict[str, Any]:
    """Return only supported filter keys with non-None values."""
    cleaned: Dict[str, Any] = {}
    for key, item_value in filters.items():
        if key in allowed and item_value is not None:
            cleaned[key] = item_value
    return cleaned


class Open5e:  # noqa: SC200
    """Minimal client around Open 5e endpoints."""

    def __init__(
        self,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
    ) -> None:
        """Create a client with timeouts and basic retries."""
        self._client = httpx.Client(
            timeout=httpx.Timeout(timeout),
            transport=httpx.HTTPTransport(retries=retries),
        )

    def spells(self, **filters: Any) -> Dict[str, Any]:
        """Fetch spells with allowed filters only."""
        query_params = _only_allowed(filters, SPELLS_FILTERS)
        return self._request(SPELLS_URL, query_params=query_params)

    def monsters(self, **filters: Any) -> Dict[str, Any]:
        """Fetch monsters with allowed filters only."""
        query_params = _only_allowed(filters, MONSTERS_FILTERS)
        return self._request(MONSTERS_URL, query_params=query_params)

    def magic_items(self, **filters: Any) -> Dict[str, Any]:
        """Fetch magic items with allowed filters only."""
        query_params = _only_allowed(filters, MAGIC_ITEMS_FILTERS)
        return self._request(MAGIC_ITEMS_URL, query_params=query_params)

    def _request(
        self,
        url: str,
        *,
        query_params: Mapping[str, Any],
    ) -> Dict[str, Any]:
        """Perform a GET and return JSON (raises for HTTP errors)."""
        response = self._client.get(url, params=query_params)
        response.raise_for_status()
        return response.json()
