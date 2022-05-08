import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hunter.interface import Job, Logger


class TestInterface(unittest.TestCase):

    def test_job_interface(self):

        class MyJob(Job):

            def __repr__(self):
                return 'my job'

            def _run(self):
                return ['result1', 'result2']

        # only list is acceptable
        with self.assertRaises(TypeError) as context:
            MyJob('bad input')
            self.assertTrue(
                'job my job input is not type of list' in context.exception)

        job = MyJob(['input1', 'input2'])
        self.assertEqual(['result1', 'result2'], job.run())
        self.assertEqual(os.path.dirname(os.path.realpath(__file__)), job.dir)

    def test_logger_interface(self):

        class MyLogger(Logger):
            queue = []

            def write_to_error_log(self, msg):
                self.queue.append('write {} to error log {}'.format(
                    msg, self.error_log))

            def send_to_bot(self, msg):
                self.queue.append('send {} to bot {}'.format(msg, self.token))

            def info(self, msg):
                self.queue.append('info {}'.format(msg))

        logger = MyLogger(token='TOKEN', error_log='ERROR_LOG')
        logger.err('msg')
        self.assertEqual(logger.queue, [
            'info msg', 'write msg to error log ERROR_LOG',
            'send msg to bot TOKEN'
        ])


if __name__ == '__main__':
    unittest.main()
