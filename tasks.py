from invoke import task


@task
def init(cmd):
    cmd.run('pipenv install --dev', pty=True)


@task
def pylint(cmd):
    cmd.run('pipenv run pylint mail_renderer.py mail_sender.py', pty=True)


@task
def flake8(cmd):
    cmd.run('pipenv run flake8', pty=True)


@task
def mypy(cmd):
    cmd.run('pipenv run mypy mail_renderer.py mail_sender.py', pty=True)


@task
def lint(cmd):
    pylint(cmd)
    flake8(cmd)
    mypy(cmd)
