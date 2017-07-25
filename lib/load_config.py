import os
from yaml import load, dump

"""
    Base class to make configuration files available
"""


class Config:

    def __init__(self):

        config_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\config.yml'
        local_config_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\config.local.yml'

        if os.path.isfile(config_file):
            with open(config_file, 'r') as config_yml:
                global_config = load(config_yml)
        if os.path.isfile(local_config_file):
            with open(local_config_file, 'r') as local_config_yml:
                local_config = load(local_config_yml)
        else:
            local_config = {}

        try:
            config = global_config
            config.update(local_config)
        except UnboundLocalError:
            raise

        self.config = config
