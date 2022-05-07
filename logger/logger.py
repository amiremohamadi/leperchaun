from abc import abstractmethod


class Logger:
    '''inherit and implement this class to create and customize your own logger'''

    def __init__(self, token=None, error_log=None):
        self.token = token
        self.error_log = error_log

    def err(self, msg):
        self.write_to_error_log(msg)
        self.send_to_bot(msg)

    @abstractmethod
    def send_to_bot(self, msg):
        raise NotImplementedError

    @abstractmethod
    def write_to_error_log(self, msg):
        '''error log can be a unix socket or file or etc. based on your implementation'''
        raise NotImplementedError

    @abstractmethod
    def teardown(self):
        '''release all the resources Eg. file descriptors'''
        raise NotImplementedError
