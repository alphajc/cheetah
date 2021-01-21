import os
import logging
import asyncio
from datetime import date, datetime, timedelta
# from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from xlrd.biffh import XLRDError
from cheetah.points import Point
from cheetah.joy_run import JoyRun


class Daemon:
    def __init__(self, config):
        datadir = config['cheetah']['datadir']
        self.point = Point(datadir, config['points'])
        # self.sched = BlockingScheduler()
        self.sched = AsyncIOScheduler()
        self.logger = logging.getLogger(__name__)
        self.joy_run = JoyRun(config['cheetah'])

    async def _award_by_day(self):
        self.logger.info('Award by day')

        """调取下载过去一天的数据，并返回文件名"""
        today = date.today()
        records_fpath  = await self.joy_run.export_running_records(
            today-timedelta(days=1),
            today)

        try:
            self.point.award(records_fpath, lambda r: r[-1] * 2)
        except XLRDError as e:
            self.logger.warning(e)
            asyncio.sleep(10)
            self._award_by_day()
        self.point.persist()

    async def _award_by_week(self):
        self.logger.info('Award by week')

        """调取下载过去一周的数据，并返回文件名"""
        today = date.today()
        records_fpath = await self.joy_run.export_running_records(
            today-timedelta(weeks=1),
            today)

        try:
            self.point.award(
                records_fpath,
                lambda r: 2 if r[-1] > 2 else 1 if r[-1] > 1 else 0
            )
        except XLRDError as e:
            self.logger.warning(e)
            asyncio.sleep(10)
            self._award_by_week()
        self.point.persist()

    def _award_by_month(self):
        self.logger.info('Award by month')

        self.point.roll_monthly_list()
        self.persist()

    def run(self):
        self.sched.start()
        print('Press Ctrl+{0} to exit'
              .format('Break' if os.name == 'nt' else 'C'))
        try:
            asyncio.get_event_loop().run_forever()
        except (KeyboardInterrupt, SystemExit):
            pass

    def add_jobs(self):
        self.sched.add_job(
            self._award_by_month,
            'cron', day=1, hour=6, minute=10
        )
        self.sched.add_job(
            self._award_by_week,
            'cron', day_of_week='mon', hour=6, minute=20
        )
        self.sched.add_job(
            self._award_by_day,
            'cron', hour=6, minute=30
        )
