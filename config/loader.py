import copy
import json
import os

from typing import List, Union, Optional, Any

_config = {}
_config_path = os.path.join(os.path.dirname(__file__), 'config.json')


def _get_config_mtime():
    return os.path.getmtime(_config_path)


def _load_config():
    global _config

    _last_mtime = _get_config_mtime()

    with open(_config_path, 'r') as f:
        raw_config = json.load(f)

    _config = copy.deepcopy(raw_config)


def get(*subkeys: str) -> Any:
    """
    Returns typed value from host-specific config.
    :param subkeys: path to config value
    :return: config value
    """
    subkeys = list(subkeys)
    data = _config

    while subkeys:
        subkey = subkeys.pop(0)
        data = data[subkey]
    if isinstance(data, dict) or isinstance(data, list):
        return copy.deepcopy(data)
    return data


if not _config:
    _load_config()