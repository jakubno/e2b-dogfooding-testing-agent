import ast
import asyncio
import os
import openai
from e2b import Session
from dotenv import load_dotenv

from src.github import configure_github, commit_changes
from src.llm import specify_file_path, fix_file
from src.utils import _init, _run_process, _cleanup

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
E2B_API_KEY = os.getenv("E2B_API_KEY")


PROJECT = "e2b-dogfooding-tests-repo"


async def testing_loop(session: Session):
    for i in range(3):
        await _run_process(session, "sudo pytest", rootdir=f"/code/{PROJECT}")

        failed_tests = await session.filesystem.list(f"/code/{PROJECT}/tests/prompts/")
        if len(failed_tests) == 0:
            return

        for failed_test in failed_tests:
            failed_test_code = await session.filesystem.read(
                f"/code/{PROJECT}/tests/prompts/{failed_test.name}"
            )
            path = specify_file_path(failed_test_code)
            module_path, function_name = path.split("::")

            module = await session.filesystem.read(f"/code/{PROJECT}/{module_path}.py")
            parsed = ast.parse(module)

            class_name = None
            if "." in function_name:
                class_name = function_name.split(".")[0]
                function_name = function_name.split(".")[1]

            for node in ast.walk(parsed):
                if class_name:
                    if isinstance(node, ast.ClassDef) and node.name == class_name:
                        for class_node in ast.walk(node):
                            if (
                                isinstance(class_node, ast.FunctionDef)
                                and class_node.name == function_name
                            ):
                                function_code = ast.get_source_segment(
                                    module, class_node
                                )
                                break
                        break
                else:
                    if isinstance(node, ast.FunctionDef) and node.name == function_name:
                        function_code = ast.get_source_segment(module, node)
                        break
            else:
                print("Function not found")
                continue

            fixed_code = fix_file(path, function_code, failed_test)
            module = module.replace(function_code, fixed_code)

            await session.filesystem.write(f"/code/{PROJECT}/{module_path}.py", module)
            await session.filesystem.remove(
                f"/code/{PROJECT}/tests/prompts/{failed_test.name}"
            )
    else:
        raise Exception("Failed to fix tests")


async def main():
    session = await Session.create("Python3", api_key=E2B_API_KEY)
    await _init(session, PROJECT)
    await configure_github(session, PROJECT)

    await testing_loop(session)

    await _cleanup(session, PROJECT)

    await commit_changes(session, PROJECT)

    await session.close()


asyncio.run(main())
