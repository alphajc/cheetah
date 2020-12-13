import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from cheetah.points import Point


class Daemon:
    def __init__(self, config):
        datadir = config['cheetah']['datadir']
        self.point = Point(datadir, config['points'])
        self.sched = BlockingScheduler()
        self.logger = logging.getLogger(__name__)

    def _award_by_day(self):
        self.logger.info('Award by day')

        """调取下载过去一天的数据，并返回文件名"""
        records_fname = '202012_十方教育跑团跑步数据统计_1201-1208_pypq.xlsx'
        records_fpath = os.path.join(self.datadir, records_fname)

        self.point.award(records_fpath, lambda r: r[-1] * 2)
        self.persist()

    def _award_by_week(self):
        self.logger.info('Award by week')

        """调取下载过去一周的数据，并返回文件名"""
        records_fname = '202012_十方教育跑团跑步数据统计_1201-1208_pypq.xlsx'
        records_fpath = os.path.join(self.datadir, records_fname)

        self.point.award(
            records_fpath,
            lambda r: 2 if r[-1] > 2 else 1 if r[-1] > 1 else 0
        )
        self.persist()

    def _award_by_month(self):
        self.logger.info('Award by month')

        self.point.roll_monthly_list()
        self.persist()

    def run(self):
        self.sched.start()

    def add_jobs(self):
        self.sched.add_job(
            self._award_by_month,
            'cron', day=1, hour=0, minute=10
        )
        self.sched.add_job(
            self._award_by_week,
            'cron', day_of_week='mon', hour=0, minute=20
        )
        self.sched.add_job(
            self._award_by_day,
            'cron', hour=0, minute=30
        )
