'''only put the name of your module here'''

from enumer import EnumerJob
from flinks import FlinksJob
from httpx import HttpxJob
from nuclei import NucleiJob
from fallparams import FallparamsJob
from reflector import ReflectorJob
from printer import PrinterJob
from unique import UniqueJob
from qreplace import QreplaceJob
from rabbitmq import RabbitmqJob

modules = {
    'enumer': EnumerJob,
    'flinks': FlinksJob,
    'httpx': HttpxJob,
    'nuclei': NucleiJob,
    'fallparams': FallparamsJob,
    'reflector': ReflectorJob,
    'printer': PrinterJob,
    'unique': UniqueJob,
    'qreplace': QreplaceJob,
    'rabbitmq': RabbitmqJob,
}
