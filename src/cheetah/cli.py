import click
import logging
import configparser as cp
from cheetah.points import Point
from cheetah.daemon import Daemon


@click.command()
@click.option('-c', '--config', default='./config.ini',
              help='指定配置文件，默认当前目录下的 config.ini')
def daemon(config):
    c = cp.ConfigParser()
    c.read(config)
    logging.basicConfig(level=c['logging']['level'])
    d = Daemon(c)
    d.run()


@click.command()
@click.option('-c', '--config', default='./config.ini',
              help='指定配置文件，默认当前目录下的 config.ini')
@click.option('-f', '--records-file', required=True,
              help='从悦跑圈下载下来的xlsx格式的跑步记录文件')
def cli(config, records_file):
    c = cp.ConfigParser()
    c.read(config)
    logging.basicConfig(level=c['logging']['level'])
    datadir = c['cheetah']['datadir']
    point = Point(datadir, c['points'])

    point.award(records_file, lambda r: r[-1] * 2)
    point.award(
        records_file,
        lambda r: 2 if r[-1] > 2 else 1 if r[-1] > 1 else 0
    )
    point.persist()
