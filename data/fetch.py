import importlib
import pkgutil
from inspect import getmembers


def fetch_data_functions():
    package = importlib.import_module('data')
    submodules = {}
    for _, name, _ in pkgutil.walk_packages(package.__path__):
        if name != 'fetch':
            full_name = package.__name__ + '.' + name
            submodules[name] = importlib.import_module(full_name)

    methods = {}
    for module in submodules.keys():
        functions_list = [f for f in getmembers(submodules[module])]
        methods[module] = {}
        for name, f in functions_list:
            if name == 'get_data':
                methods[module]['function'] = f

    return methods