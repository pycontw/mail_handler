from invoke.collection import Collection
from invoke.context import Context
from invoke.tasks import task


@task
def clean(ctx: Context) -> None:
    """Remove all the tmp files in .gitignore"""
    ctx.run("git clean -Xdf")


@task
def dist(ctx: Context) -> None:
    """Build distribution"""
    ctx.run("poetry build")


build_ns = Collection("build")
build_ns.add_task(clean)  # type: ignore[arg-type]
build_ns.add_task(dist)  # type: ignore[arg-type]
