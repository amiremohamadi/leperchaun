from interface import Job
from itertools import chain


class PrinterJob(Job):

    def __repr__(self):
        return 'printer'

    def _run(self):
        print('[PRINTER_JOB] {}'.format(self.input))
