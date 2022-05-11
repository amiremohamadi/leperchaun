'''only put the name of your module here'''

from enumer import EnumerJob
from flinks import FlinksJob
from httpx import HttpxJob
from nuclei import NucleiJob
from printer import PrinterJob
from unique import UniqueJob
from rabbitmq import RabbitmqJob

modules = {
    'enumer': EnumerJob,
    'flinks': FlinksJob,
    'httpx': HttpxJob,
    'nuclei': NucleiJob,
    'printer': PrinterJob,
    'unique': UniqueJob,
    'rabbitmq': RabbitmqJob,
}
