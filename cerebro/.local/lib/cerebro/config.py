import os
import tomllib


def load(path=None):
    path = path or os.path.expanduser("~/.config/cerebro/config.toml")
    with open(path, "rb") as f:
        return tomllib.load(f)