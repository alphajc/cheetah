import os
import requests
import logging
from asyncio import sleep
from urllib.parse import unquote
from operator import itemgetter

"""
JoyRun 悦跑圈
"""
class JoyRun:
    def __init__(self, config):
        self.session = requests.session()
        self.config = config
        self._login()

    """登录"""
    def _login(self):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/87.0.4280.66 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://crew-admin.thejoyrun.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://crew-admin.thejoyrun.com/html/login.html',
            'Accept-Language': 'en-CN,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6'
        }

        payloads = {
            'userName': self.config['uid'],
            'password': self.config['password']
        }

        r = self.session.post(
            'https://crew-admin.thejoyrun.com/index.php?c=Login&m=login',
            data=payloads)

        if int(r.json()['ret']) == 0:
            logging.info('登录成功！')


    """导出运动记录"""
    async def export_running_records(self, begin_time, end_time):
        """generate record"""
        payloads = {
            'crewid': self.config['gid'],
            'datelineFrom': begin_time.strftime('%Y-%m-%d %H:%M:%S'),
            'datelineTo': end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'meterMin': self.config.get('meter_min', 2500),
            'meterMax': self.config.get('meter_max', ''),
            'speedMax': self.config.get('speed_max', ''),
            'speedMin': self.config.get('speed_min', ''),
            'runingType': '0',
            'nodeid': '0',
            'uid': self.config['uid']
        }
        logging.debug(payloads)

        r = self.session.post('https://crew-admin.thejoyrun.com/index.php?'
                          'c=Stat&m=runDataStatistics', data=payloads)

        if int(r.json()['ret']) == 0:
            logging.info('生成跑步记录成功！')
        else:
            logging.error('生成跑步记录出错！')
            return

        """wait url"""
        async def get_download_filename():
            payloads = {
                'pageNum': '1',
                'pageSize': '10',
                'uid': '135253241'
            }

            res = self.session.post('https://crew-admin.thejoyrun.com/index.php'
                                    '?c=Stat&m=getDataList', data=payloads)
            latest_file = max(res.json()['data']['pageList'],
                              key=itemgetter('fileId'))
            while latest_file['exportStatus'] == 1:
                print('.', end='')
                await sleep(3)
                res = self.session.post('https://crew-admin.thejoyrun.com'
                                        '/index.php?c=Stat&m=getDataList',
                                        data=payloads)
                if res.json()['ret'] == 0:
                    logging.info('下载链接已获取！')
                latest_file = max(res.json()['data']['pageList'],
                                  key=itemgetter('fileId'))

            return unquote(latest_file['fileDownloadUrl'])

        filename = await get_download_filename()

        """download"""
        r = self.session.get('https://crew-admin.thejoyrun.com/download.php',
                             params={'filename': filename})

        filepath = os.path.join(self.config['datadir'], filename.split('/')[-1])
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)

        logging.info('下载成功！')

        return filepath

