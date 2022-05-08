from logger import DefaultLogger
from enumer import EnumerJob
import argparse
import json


class Pipeline:

    def __init__(self):
        self.jobs = {}

    def run(self):
        stack = []
        for (_, job) in self.jobs.items():
            if job.starter:
                stack.append(job)

        while len(stack) > 0:
            job = stack.pop()
            self.logger.info('{} job started'.format(job))
            print(job.run())


def preprocess_jobs(jobs):
    '''get a list of jobs and make dict of them to make traversing job-graph easier and more efficient'''
    jobs_dict = {}

    for job in jobs:
        name = job['name']
        if name == 'enumer':
            jobs_dict[name] = EnumerJob(['birjand.ac.ir'])
            jobs_dict[name].starter = True

    return jobs_dict


def build_pipeline(config):
    '''create pipeline runner based on config'''
    try:
        with open(config, 'r') as config:
            config = json.load(config)
            pipeline = Pipeline()

            # optional
            pipeline.name = config.get('name')
            pipeline.version = config.get('version')

            # optional
            if logger := config.get('logger'):
                _logger = DefaultLogger(token=logger.get('token'),
                                        error_log=logger.get('error_log'))
                pipeline.logger = _logger

            jobs = config.get('pipeline', [])
            pipeline.jobs = preprocess_jobs(
                jobs)  # TODO better error handling in case of key error

            return pipeline
    except FileNotFoundError:
        print('config file not found')
    except Exception as err:
        print('error happened {}'.format(err))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='pipeline runner')
    parser.add_argument('--config',
                        '-c',
                        action='store',
                        type=str,
                        default='pipeline.json',
                        help='pipeline config file')
    args = parser.parse_args()

    try:
        pipeline = build_pipeline(args.config)
        pipeline.run()
    except FileNotFoundError:
        print('config file not found')
    except Exception as err:
        print('error happened: {}'.format(err))
