import logging as log
import os
import shutil
import sys

import click
import googletrans

DEF_LOG = 'schwurbler.log'


def log_exception(extype, value, trace):
    """
    Hook to log uncaught exceptions to the logging framework. Register this as
    the excepthook with `sys.excepthook = log_exception`.
    """
    log.exception("Uncaught exception: ", exc_info=(extype, value, trace))


def setup_logging(log_file):
    """
    Sets up the logging framework to log to the given log_file and to STDOUT.
    If the path to the log_file does not exist, directories for it will be
    created.
    """
    if os.path.exists(log_file):
        backup = f'{log_file}.1'
        shutil.move(log_file, backup)

    file_handler = log.FileHandler(log_file, "w", "utf-8")
    term_handler = log.StreamHandler()
    handlers = [term_handler, file_handler]
    fmt = "%(asctime)s %(levelname)-8s %(message)s"
    log.basicConfig(handlers=handlers, format=fmt, level=log.DEBUG)

    sys.excepthook = log_exception

    log.info("Started schwurbler logging to: %s", log_file)


@click.group()
@click.option("--log-file", type=click.Path(dir_okay=False), default=DEF_LOG)
def cli(log_file=None):
    """
    Click group that ensures at least log and configuration file are present,
    since the rest of the application uses those.

    :param log_file:
        The file to log to. An existing file will be backed up to {log_file}.1
    :param cfg_file:
        Config file to read.
    """
    setup_logging(log_file)


def validate_path(path):
    path = [step.lower().strip() for step in path.split(',')]
    if len(path) < 2:
        raise ValueError('Path needs to be at least two languages long.')
    for step in path:
        if step not in googletrans.LANGUAGES:
            raise ValueError('Language not known: {}'.format(step))
    return path


def path_schwurbel(path, text):
    log.debug('Performing path schwurbel %s on: %s', path, text)
    trans = googletrans.Translator()

    translated = text
    for src, dest in zip(path, path[1:]):
        translated = trans.translate(translated, src=src, dest=dest)
        log.debug('Got intermediate schwurbel: %s', translated)
        assert translated.src == src
        assert translated.dest == dest
        translated = translated.text

    log.debug('Got final schwurbel: %s', translated)

    return translated


@cli.command()
@click.option('--path', default='en,ja,en')
@click.argument('text')
def fixed_schwurbel(path, text):
    path = validate_path(path)
    path_schwurbel(path, text)


if __name__ == '__main__':
    cli()
