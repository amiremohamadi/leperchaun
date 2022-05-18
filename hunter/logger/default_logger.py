from interface import Logger
import json
import grequests
import requests

# TODO: make logger async


class DefaultLogger(Logger):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.prepare_err_log()

    def prepare_err_log(self):
        if self.error_log is None:
            return
        try:
            self.error_log = open(self.error_log, 'a')
        except FileNotFoundError:
            print('[logger] set_err_log: file not found')
        except Exception as err:
            print('[logger] set_err_log: {}'.format(err))

    def send_to_bot(self, msg):
        if self.token is None:
            return
        try:
            data = json.dumps({
                'username': 'test',
                'content': msg,
            })
            requests.post(self.token,
                          headers={'Content-Type': 'application/json'},
                          data=data)
        except Exception as err:
            print('[logger] send_to_bot: {}'.format(err))

    def write_to_error_log(self, msg):
        if self.error_log is None:
            return
        try:
            self.error_log.write('{}\n'.format(msg))
            self.error_log.flush()
        except Exception as err:
            print('[logger] write_to_error_log: {}'.format(err))

    def info(self, msg):
        print(msg)

    def teardown(self):
        if self.error_log:
            self.error_log.close()
