from logger import DefaultLogger
import argparse
import json


class Pipeline:

    def __init__(self):
        self.jobs = []

    def run(self):
        for job in self.jobs:
            job.run()


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
