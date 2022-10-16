import os

import validators
import yaml


def validate_url(url):
    return validators.url(url)


class Config:
    """
    Manage a config file.
    """

    def __init__(self, config: str, file_path=True):
        if file_path:
            if os.path.isfile(config):
                with open(config, 'r') as file:
                    temp = yaml.safe_load(file)
            else:
                raise FileNotFoundError('Could not find', config)
        elif isinstance(config, dict):
            raise Exception(f'Invalid config object {type(config)}. Must be a path to the config file or a dict of the proper config values.')

        # need to do pyyaml verification

        self.webui_base_url = temp['webui_base_url']
        self.default_prompt_template = temp['default_prompt_template']
        self.timeout = temp['timeout']
        self.target_server = temp['target_server']
        self.timeout = temp['timeout']
        self.django_base_url = temp['django_base_url']

        # x = self.validate(temp)
        # if x:
        #     self.webui_base_url, self.default_prompt_template, self.timeout = x
        # else:
        #     raise Exception('Config file failed validation:', config)

    # def validate(self, yaml_struct):
    #     if 'webui_base_url' in yaml_struct and validate_url(f'{yaml_struct["webui_base_url"]}'):
    #         webui_base_url = f'{yaml_struct["webui_base_url"]}/api/predict/'
    #     else:
    #         raise Exception(f'Config not valid: webui_base_url')
    #
    #     if 'default_prompt_template' in yaml_struct and yaml_struct['default_prompt_template'] is not None:
    #         default_prompt_template = yaml_struct['default_prompt_template']
    #     else:
    #         raise Exception(f'Config not valid: default_prompt_template')
    #
    #     if 'timeout' in yaml_struct and yaml_struct['timeout'] is not None:
    #         timeout = yaml_struct['timeout']
    #     else:
    #         raise Exception(f'Config not valid: timeout')
    #
    #     return webui_base_url, default_prompt_template, timeout,
