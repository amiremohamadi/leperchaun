'''only put the name of your module here'''

from enumer import EnumerJob
from flinks import FlinksJob
from httpx import HttpxJob
from nuclei import NucleiJob
from printer import PrinterJob
from writer import WriterJob
from unique import UniqueJob
from rabbitmq import RabbitmqJob

modules = {
    'enumer': EnumerJob,
    'flinks': FlinksJob,
    'httpx': HttpxJob,
    'nuclei': NucleiJob,
    'printer': PrinterJob,
    'writer': WriterJob,
    'unique': UniqueJob,
    'rabbitmq': RabbitmqJob,
}
