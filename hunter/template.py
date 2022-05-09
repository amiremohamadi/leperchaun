'''
template generator
every module has a specific template, to make it easier we can use template generator
'''

import os

module_template = '''from interface import Job


class {}Job(Job):

    def __repr__(self):
        return '{}'

    def _run(self):
        pass'''

init_template = '''from .{} import {}Job'''

success_msg = '''module successfully created. in order to use it, add `'{}': {}Job` to modules list inside `modules.py`.'''


def module_generate(name):
    module = module_template.format(name.title(), name)
    init = init_template.format(name, name.title())

    dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    os.mkdir(dir)

    module_path = os.path.join(dir, '{}.py'.format(name))
    init_path = os.path.join(dir, '__init__.py')

    with open(module_path, 'w') as module_fd, open(init_path, 'w') as init_fd:
        module_fd.write(module)
        init_fd.write(init)

    print(success_msg.format(name, name.title()))
