from logger import DefaultLogger
import argparse
import json


class Pipeline:

    def name(self, name):
        self.name = name

    def version(self, version):
        self.version = version

    def logger(self, logger=None):
        self.logger = logger


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
                        default='pipeline.toml',
                        help='pipeline config file')
    args = parser.parse_args()

    try:
        build_pipeline(args.config)
    except FileNotFoundError:
        print('config file not found')
    except Exception as err:
        print('error happened: {}'.format(err))
