"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mcpplibhub` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``cpplibhub.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``cpplibhub.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import logging

# import sys
import click

from cpplibhub.settings import Settings

# from cpplibhub.file_utils import dir_exists


def init_logger():
    logging.basicConfig(filename=Settings.PROJECT_LOGGER_FILE, level=logging.INFO)


def create_new_project(*, interactive, project_name):
    if interactive:
        project_name = input("Enter project name: ")

    print(f"* Creating project '{project_name}'")


@click.command()
@click.version_option()
@click.argument('create', default="")
@click.option("--project_name", default="",
              help="Specify project name.")
@click.option("-i", "--interactive", default=False, is_flag=True,
              help="Interactive project creation mode. User has to answer the questions.")
def main(*,  # argv=sys.argv,
         create,
         interactive,
         project_name,
         **_  # kwargs
         ):
    """
    Simple dependency management tool for C++ and C projects.
    """
    Settings.check_home_dir_integrity()
    init_logger()
    Settings.load()
    print(f"Settings loaded: {Settings.parser.sections()}")
    print(f"libhub_root: {Settings.parser['PATHS']['libhub_root']}")

    try:
        print(f"just_another_key: {Settings.parser['PATHS']['just_another_key']}")
    except KeyError:
        pass

    if create:
        create_new_project(interactive=interactive, project_name=project_name)

    return 0


# TODO: Create Bootstrap class or think out better architecture
# TODO: use https://github.com/cookiecutter/cookiecutter for creating templates
