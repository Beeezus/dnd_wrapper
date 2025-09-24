from __future__ import annotations

from typing import Any, Final, Mapping

import httpx


class Open5e:

    _SPELLS_URL: Final[str] = "https://api.open5e.com/v2/spells/"
    _MONSTERS_URL: Final[str] = "https://api.open5e.com/v1/monsters/"
    _MAGIC_ITEMS_URL: Final[str] = "https://api.open5e.com/v1/magicitems/"


    _SPELLS_FILTERS: Final[frozenset[str]] = frozenset({
        "name", "name__icontains",
        "classes__key__in",
        "level", "level__range",
        "range", "range__range",
        "school__key", "school__name", "school__name__in",
        "duration",
        "concentration", "verbal", "somatic", "material", "material_consumed",
        "casting_time",
    })

    _MONSTERS_FILTERS: Final[frozenset[str]] = frozenset({
        "name", "name__icontains",
        "desc", "desc__icontains",
        "cr",
        "hit_points", "hit_points__range",
        "armor_class", "armor_class__range",
        "type", "type__contains",
        "size", "size__contains",
    })

    _MAGIC_ITEMS_FILTERS: Final[frozenset[str]] = frozenset({
        "slug", "slug__in",
        "name", "name__icontains",
        "desc", "desc__in", "desc__contains",
        "type", "type__contains",
        "rarity", "rarity__contains",
        "requires_attunement",
    })

    def __init__(
        self,
        *,
        timeout: float = 10.0,
        retries: int = 3
    ) -> None:

        self._client = httpx.Client(
            timeout=httpx.Timeout(timeout),
            transport=httpx.HTTPTransport(retries=retries),
        )

    def spells(self, **filters: Any) -> dict[str, Any]:
        params = self._only_allowed(filters, self._SPELLS_FILTERS)
        return self._request(self._SPELLS_URL, params=params)

    def monsters(self, **filters: Any) -> dict[str, Any]:
        params = self._only_allowed(filters, self._MONSTERS_FILTERS)
        return self._request(self._MONSTERS_URL, params=params)

    def magic_items(self, **filters: Any) -> dict[str, Any]:
        params = self._only_allowed(filters, self._MAGIC_ITEMS_FILTERS)
        return self._request(self._MAGIC_ITEMS_URL, params=params)

    @staticmethod
    def _only_allowed(filters: Mapping[str, Any], allowed: frozenset[str]) -> dict[str, Any]:
        return {k: v for k, v in filters.items() if k in allowed}

    def _request(self, url: str, *, params: Mapping[str, Any]) -> dict[str, Any]:
        try:
            resp = self._client.get(url, params=params)
        except httpx.HTTPError as exc:
            raise exc

        return resp.json()
