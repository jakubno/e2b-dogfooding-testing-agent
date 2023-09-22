from e2b import Session


async def _run_process(session: Session, cmd: str, rootdir: str = "/code"):
    proc = await session.process.start(
        cmd,
        rootdir=rootdir,
        on_stdout=lambda data: print(data.line),
        on_stderr=lambda data: print(f"[STDERR]: {data.line}"),
    )
    output = await proc
    return output


async def _init(session: Session, project: str) -> None:
    await _run_process(session, f"git clone https://github.com/jakubno/{project}.git")
    await _run_process(
        session, "sudo pip install -r requirements.txt", rootdir=f"/code/{project}"
    )
    await _run_process(session, "sudo pip install pytest", rootdir=f"/code/{project}")

    with open("src/conftest.py", "r") as f:
        conftest = f.read().replace("$PREFIX", f"/code/{project}")
    await session.filesystem.write(f"/code/{project}/conftest.py", conftest)
    await session.filesystem.make_dir(f"/code/{project}/tests/prompts/")


async def _cleanup(session: Session, project: str) -> None:
    await session.filesystem.remove(f"/code/{project}/conftest.py")
