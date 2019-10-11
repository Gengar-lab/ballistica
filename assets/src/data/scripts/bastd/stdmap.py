# Copyright (c) 2011-2019 Eric Froemling
"""Defines standard map type."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ba

if TYPE_CHECKING:
    from typing import Dict, Any, Optional


def _get_map_data(name: str) -> Dict[str, Any]:
    import json
    print('Would get map data', name)
    with open('data/data/maps/' + name + '.json') as infile:
        mapdata = json.loads(infile.read())
    assert isinstance(mapdata, dict)
    return mapdata


class StdMap(ba.Map):
    """A map completely defined by asset data.

    """
    _data: Optional[Dict[str, Any]] = None

    @classmethod
    def _getdata(cls) -> Dict[str, Any]:
        if cls._data is None:
            cls._data = _get_map_data('bridgit')
        return cls._data

    def __init__(self) -> None:
        super().__init__()
