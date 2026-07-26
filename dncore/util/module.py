import sys
from importlib import import_module
from importlib.abc import MetaPathFinder
from importlib.machinery import ModuleSpec
from importlib.util import spec_from_file_location
from inspect import isfunction
from typing import Callable

__all__ = [
    "import_module_from_file_location",
    "import_module_from_spec",
]


class NameSpecFinder(MetaPathFinder):
    def __init__(self, name: str, spec: ModuleSpec | Callable[[], ModuleSpec]):
        self.name = name
        if isfunction(spec):
            self.spec = spec
        else:
            self.spec = lambda: spec

    def find_spec(self, fullname, *_):
        return self.spec() if fullname == self.name else None


def import_module_from_file_location(name, location):
    """
    https://qiita.com/kzm4269/items/e7e67ab6c1dd278c3d16
    """
    finder = NameSpecFinder(name, lambda: spec_from_file_location(name, location))
    sys.meta_path.insert(0, finder)
    try:
        return import_module(name)
    finally:
        sys.meta_path.remove(finder)


def import_module_from_spec(name, spec: ModuleSpec):
    finder = NameSpecFinder(name, spec)
    sys.meta_path.insert(0, finder)
    try:
        return import_module(name)
    finally:
        sys.meta_path.remove(finder)
