import configparser as cp
from cheetah.daemon import Daemon


if __name__ == '__main__':
    config = cp.ConfigParser()
    config.read('./config.ini')

    logging.basicConfig(level=config['logging']['level'])
    d = Daemon(config)
    d.add_jobs()
    d.run()
