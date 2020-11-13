import os.path
import yaml


class Config(object):
    '''
    Config Class
    '''
    __instance = None

    class __Config:

        __file_name = 'getmymsg.yaml'

        def __init__(self):
            file_name = Config.__Config.__file_name
            if not os.path.isfile(file_name):
                raise Exception('File {} not exist.'.format(file_name))
            stream = open(file_name, 'r')
            data = yaml.safe_load(stream)
            self.__validate__(data)
            self.__data = data
            stream.close()

        def __validate__(self, data):
            pass

        def __getattr__(self, name):
            return self.__data.get(name)

    def __new__(cls):
        if Config.__instance is None:
            Config.__instance = Config.__Config()
        return Config.__instance

    def __setattr__(self, *args, **kwargs):
        raise Exception('')

    def __getattr__(self, name):
        return getattr(Config.__instance, name)
