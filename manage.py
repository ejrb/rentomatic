#!/usr/bin/env python

import json
import os
import subprocess
import time
from contextlib import closing

import click
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def setenv(variable, default):
    os.environ[variable] = os.getenv(variable, default)


APPLICATION_CONFIG_PATH = 'config'
DOCKER_PATH = 'docker'


def app_config_file(config):
    return os.path.join(APPLICATION_CONFIG_PATH, f'{config}.json')


def docker_compose_file(config):
    return os.path.join(DOCKER_PATH, f'{config}.yml')


def read_json_configuration(config):
    with open(app_config_file(config)) as f:
        config_data = json.load(f)

    config_data = {i['name']: i['value'] for i in config_data}

    return config_data


def configure_app(config):
    configuration = read_json_configuration(config)

    for key, value in configuration.items():
        setenv(key, value)


@click.group()
def cli():
    pass


def docker_compose_cmdline(commands_string=None):
    config = os.getenv('APPLICATION_CONFIG')
    configure_app(config)

    compose_file = docker_compose_file(config)

    if not os.path.isfile(compose_file):
        raise ValueError(f'The file {compose_file} does not exist')

    command_line = [
        'docker-compose',
        '-p',
        config,
        '-f',
        compose_file
    ]

    if commands_string:
        command_line.extend(commands_string.split(' '))

    return command_line


def run_sql(statements):
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOSTNAME'),
        port=os.getenv('POSTGRES_PORT'),
    )

    with closing(conn):
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        with closing(cursor):
            for statement in statements:
                cursor.execute(statement)


def wait_for_logs(cmdline, message):
    logs = subprocess.check_output(cmdline)
    while message not in logs.decode('utf-8'):
        time.sleep(1)
        logs = subprocess.check_output(cmdline)


@cli.command()
@click.argument('args', nargs=-1)
def test(args):
    os.environ['APPLICATION_CONFIG'] = 'test'
    configure_app(os.getenv('APPLICATION_CONFIG'))

    cmdline = docker_compose_cmdline('up -d')
    subprocess.call(cmdline)

    try:
        cmdline = docker_compose_cmdline('logs postgres')
        wait_for_logs(cmdline, 'ready to accept connections')
        cmdline = docker_compose_cmdline('logs mongo')
        wait_for_logs(cmdline, 'Waiting for connections')

        run_sql([f'CREATE DATABASE {os.getenv("APPLICATION_DB")}'])

        cmdline = [
            'pytest',
            '-svv',
            '--cov=application',
            '--cov-report=term-missing'
        ]
        cmdline.extend(args)
        subprocess.call(cmdline)
    finally:
        cmdline = docker_compose_cmdline('down')
        subprocess.call(cmdline)


if __name__ == '__main__':
    cli()
