import unittest
import os
import sys
import types

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hunter.interface import Job, Logger


class TestInterface(unittest.TestCase):

    def test_job_interface(self):

        result = []

        class MyJob(Job):

            def __repr__(self):
                return 'my job'

            def _run(self):
                result.append('result1')
                result.append('result2')
                return None

        job = MyJob()
        job.run()
        self.assertEqual(['result1', 'result2'], result)
        self.assertEqual(os.path.dirname(os.path.realpath(__file__)), job.dir)

    def test_direct_pipe(self):

        result = []

        class MyJob(Job):

            def __repr__(self):
                return 'my job'

            def _run(self):

                def _generator():
                    yield 'result1'

                return _generator()

        class AppenderJob(Job):

            def __repr__(self):
                return 'appender job'

            def _run(self):
                result.append(self.input)

        job1 = MyJob()
        job2 = AppenderJob()
        job1.pipes = [job2]
        job1.direct = True
        job1.run()
        self.assertTrue(isinstance(result[0], types.GeneratorType))

    def test_job_pipeline(self):

        result = []

        class MyJob(Job):

            def __repr__(self):
                return 'my job'

            def _run(self):

                def _generator():
                    yield 'result1'
                    yield 'result2'

                return _generator()

        class AppenderJob(Job):

            def __repr__(self):
                return 'appender job'

            def _run(self):
                result.append(self.input)

        job1 = MyJob()
        job2 = AppenderJob()
        job1.pipes = [job2]
        job1.run()
        self.assertEqual(['result1', 'result2'], result)

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
