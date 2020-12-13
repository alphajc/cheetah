import click
import logging
import configparser as cp
from cheetah.points import Point
from cheetah.daemon import Daemon


config = cp.ConfigParser()
config.read('./config.ini')
logging.basicConfig(level=config['logging']['level'])


@click.command()
def daemon():
    d = Daemon(config)
    d.run()


@click.command()
@click.option('-f', '--records-file', required=True, help='从悦跑圈下载下来的积分文件')
def cli(records_file):
    datadir = config['cheetah']['datadir']
    point = Point(datadir, config['points'])

    point.award(records_file, lambda r: r[-1] * 2)
    point.award(
        records_file,
        lambda r: 2 if r[-1] > 2 else 1 if r[-1] > 1 else 0
    )
    point.persist()
