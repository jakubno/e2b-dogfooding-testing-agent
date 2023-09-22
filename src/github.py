import json
import os
import random

from dotenv import load_dotenv
from e2b import Session

from src.utils import _run_process

load_dotenv()

GITHUB_PAT = os.getenv("GITHUB_PAT")

unique = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=5))


async def configure_github(session: Session, project: str) -> None:
    await _run_process(
        session,
        "git config --global user.email jakub@e2b.dev",
        rootdir=f"/code/{project}",
    )
    await _run_process(
        session, "git config --global user.name jakubno", rootdir=f"/code/{project}"
    )
    await _run_process(
        session,
        "git config --global credential.helper store",
        rootdir=f"/code/{project}",
    )

    await _run_process(
        session,
        f"git remote set-url origin https://jakubno:{GITHUB_PAT}@github.com/jakubno/{project}.git",
        rootdir=f"/code/{project}",
    )

    await _run_process(
        session, f"git checkout -b agent/{unique}", rootdir=f"/code/{project}"
    )


async def commit_changes(session: Session, project: str) -> None:
    await _run_process(session, "git add .", rootdir=f"/code/{project}")
    await _run_process(session, "git reset -- .gitconfig", rootdir=f"/code/{project}")
    await _run_process(
        session, "git reset -- __pycache__/**", rootdir=f"/code/{project}"
    )
    await _run_process(
        session, "git reset -- **/__pycache__/**", rootdir=f"/code/{project}"
    )

    await _run_process(
        session, "git commit -m 'Fix failing test'", rootdir=f"/code/{project}"
    )
    await _run_process(
        session, f"git push origin agent/{unique}", rootdir=f"/code/{project}"
    )

    data = {
        "title": "Your code is fixed, baby! :muscle:",
        "body": "Please pull these awesome changes in!",
        "head": f"agent/{unique}",
        "base": "main",
    }
    command = f"""curl -L -X POST -H "Accept: application/vnd.github+json" -H "Authorization: Bearer {GITHUB_PAT}" -H "X-GitHub-Api-Version: 2022-11-28" https://api.github.com/repos/jakubno/e2b-dogfooding-tests-repo/pulls -d '{json.dumps(data)}'"""
    await _run_process(session, command)
