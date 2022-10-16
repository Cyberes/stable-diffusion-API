from .config import Config
from .gradio_functions import function_mapping
from .action import APIAction


# from helpers import

class API:
    def __init__(self, config_elm: Config):
        self.config = config_elm

    def __send(self, json_data, mode='oneshot'):
        json_data['session_hash'] = '_'  # I haven't looked at gradio's code but I think session_hash manages different "users" connected to the instance. I think setting session_hash to "_" bypasses it. Might have to randomize it if we run into issues.
        if mode == 'oneshot':
            return APIAction(self.config).send(json_data)
        elif mode == 'async':
            a = APIAction(self.config)
            r = a.send_async(json_data)
            return a, r

    # API functions are down here!
    # These are the functions you call to do stuff
    def create_hypernetwork(self, name):
        return self.__send({"fn_index": function_mapping['create_hypernetwork'], "data": [name, ["768", "320", "640", "1280"]]})

    def train_hypernetwork(self, name, dataset, lr=0.005, batch=1, log='hypernetwork_training', steps=100000, sample_img_n=500, sample_emb_n=500, template=None, read_params=False, create=False, mode='oneshot'):
        if create:
            x = self.create_hypernetwork(name)
            assert x[0] != 200, 'Backend reported error creating hypernetwork.'
        json_data = {
            'fn_index': function_mapping['train_hypernetwork'],
            'data': [
                name,  # name
                lr,  # learning rate
                batch,  # batch size
                dataset,  # Dataset directory
                log,  # Log directory
                steps,  # Max steps
                sample_img_n,  # Save an image to log directory every N steps, 0 to disable
                sample_emb_n,  # Save a copy of embedding to log directory every N steps, 0 to disable
                (self.config.default_prompt_template if template is None or False else template),  # Prompt template file
                read_params,  # Read parameters (prompt, etc...) from txt2img tab when making previews
                '',
                '',
                20,
                'Euler a',
                7,
                -1,
                512,  # width
                512,  # height
                '',
                '',
            ],
        }
        return self.__send(json_data, mode)
