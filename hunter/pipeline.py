from logger import DefaultLogger
from modules import modules
import json


class Pipeline:

    def __init__(self):
        self.starter_job = None

    def log_err(self, msg):
        if self.logger is not None:
            self.logger.err(msg)

    def log_info(self, msg):
        if self.logger is not None:
            self.logger.info(msg)

    def run(self):
        if self.starter_job is None:
            # impossible to get this state
            self.log_err('no starter job in pipeline')

        self.starter_job.run()

    def teardown(self):
        # teardown processes recursively
        self.starter_job.teardown()


def load_jobs(jobs):
    mark = set()

    def _find_job(name):
        for job in jobs:
            if job['name'] == name:
                return job
        return None

    def _load_job(ctx):
        name = ctx['name']
        pipes = ctx.get('pipeTo', [])
        direct = ctx.get('pipeDirect', False)

        if len(pipes) > 2 and direct:
            raise Exception(
                'module {} with direct property enabled got more than 1 pipes'.
                format(name))

        module = modules.get(name)
        if module is None:
            raise Exception('module {} not found'.format(name))
        job = module()
        job.direct = direct
        job.ctx = ctx

        # keep track of jobs to detect possible cycles in config
        # if name in mark:
        #     raise Exception(
        #         'cycle detected in config: {} piped more than once'.format(
        #             name))
        # mark.add(name)

        for pipe in pipes:
            j = _find_job(pipe)
            if j is None:
                raise Exception('pipe {} not found in config'.format(pipe))
            job.pipes.append(_load_job(j))

        return job

    # find starer
    starter = [job for job in jobs if job.get('startJob')]
    if len(starter) == 0 or len(starter) > 1:
        raise Exception(
            'only one starter job is required in config, found {}'.format(
                len(starter)))
    starter = starter[0]
    return _load_job(starter)


def build_pipeline(config, domain):
    '''create pipeline runner based on config'''
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
        pipeline.starter_job = load_jobs(jobs)
        pipeline.starter_job.input = domain

        return pipeline
