from invoke import task, Context

@task
def start(ctx: Context):
    ctx.run("python3 demo.py", pty=True)

@task
def lint(ctx: Context):
    ctx.run("pylint tui", pty=True)

@task
def format(ctx: Context):
    ctx.run("autopep8 --in-place --recursive tui", pty=True)

@task
def profile(ctx: Context):
    ctx.run("py-spy record --format speedscope -- python3 demo.py", pty=True)
