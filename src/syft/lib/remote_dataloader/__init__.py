# stdlib
from typing import Any as TypeAny
from typing import List as TypeList
from typing import Tuple as TypeTuple

# syft relative
from ...ast import add_classes
from ...ast import add_methods
from ...ast import add_modules
from ...ast.globals import Globals
from ...core.remote_dataloader import RemoteDataset


def create_remote_dataloader_ast(client: TypeAny = None) -> Globals:
    ast = Globals(client)

    modules = [
        "syft",
        "syft.core",
        "syft.core.remote_dataloader",
    ]

    classes: TypeList[TypeTuple[str, str, TypeAny]] = [
        (
            "syft.core.remote_dataloader.RemoteDataset",
            "syft.core.remote_dataloader.RemoteDataset",
            RemoteDataset,
        ),
    ]

    methods: TypeList[TypeTuple[str, str]] = [
        (
            "syft.core.remote_dataloader.RemoteDataset.create_dataset",
            "syft.lib.python._SyNone",
        ),
        ("syft.core.remote_dataloader.RemoteDataset.__len__", "syft.lib.python.Int"),
        ("syft.core.remote_dataloader.RemoteDataset.__getitem__", "torch.Tensor"),
    ]

    add_modules(ast, modules)
    add_classes(ast, classes)
    add_methods(ast, methods)

    for klass in ast.classes:
        klass.create_pointer_class()
        klass.create_send_method()
        klass.create_storable_object_attr_convenience_methods()

    return ast
