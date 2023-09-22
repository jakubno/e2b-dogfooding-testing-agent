import ast

import pytest


def get_imports(module_name):
    try:
        with open(module_name, "r") as file:
            tree = ast.parse(file.read())
    except FileNotFoundError:
        return None

    imports = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(f"import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            imports.append(
                f"from {node.module} import {', '.join(map(lambda alias: alias.name, node.names))}"
            )

    return imports


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    rep = yield

    if rep.when == "call" and rep.failed == True:
        test_name = item.name
        location = item.location[0]
        stacktrace = rep.longreprtext

        imports = "\n".join(get_imports(item.location[0]))
        with open(
            f"$PREFIX/tests/prompts/{location.replace('/', '.').replace('.py', '')}-{test_name}.txt",
            "w",
        ) as f:
            f.write(f"Test named: {test_name}\n\n")
            f.write(f"Test location {location}\n\n")
            f.write(f"Test imports:\n{imports}\n\n")
            f.write(f"Test failed with following stacktrace:\n{stacktrace}\n")

    return rep
