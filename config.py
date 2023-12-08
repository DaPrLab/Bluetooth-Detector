import tomllib
from typing import Any


def get_config() -> dict[str : str | dict[str:Any]]:
    with open("config.toml", "rb") as file:
        config: dict[str : str | dict[str:Any]] = tomllib.load(file)
    return config
