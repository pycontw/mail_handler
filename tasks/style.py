from invoke.context import Context
from invoke.tasks import task

from tasks.common import COMMON_TARGETS_AS_STR, VENV_PREFIX


@task
def ruff(ctx: Context) -> None:
    """Check style through ruff"""
    ctx.run(f"{VENV_PREFIX} ruff check {COMMON_TARGETS_AS_STR}")


@task
def mypy(ctx: Context) -> None:
    """Check style through mypy"""
    ctx.run(f"{VENV_PREFIX} mypy")


@task
def black_check(ctx: Context) -> None:
    """Check style through black"""
    ctx.run(f"{VENV_PREFIX} black --check {COMMON_TARGETS_AS_STR}")


@task
def commit_check(ctx):
    """Check commit message through commitizen"""
    ctx.run(f"{VENV_PREFIX} cz -nr 3 check --rev-range v0.1.1..", warn=True)


@task(pre=[ruff, mypy, black_check, commit_check], default=True)
def run(ctx: Context) -> None:
    """Check style through linter (Note that pylint is not included)"""
    pass


@task
def black(ctx):
    ctx.run(f"{VENV_PREFIX} black {COMMON_TARGETS_AS_STR}")


@task(pre=[ruff, black])
def reformat(ctx: Context) -> None:
    """Reformat python files through black and ruff"""
    pass
