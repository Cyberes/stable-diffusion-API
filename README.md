# stable-diffusion-api

_CLI and server for Stable Diffusion._

CLI and server for [AUTOMATIC1111's Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui).

### Features

The goal is to separate the compute server running the WebUI from the client and enable abstraction of the WebUI's features to enable powerful integration into other projects.

Yeah.

* CLI application.
* HTTP API via Django server running on the same machine as the WebUI.
* Python library (`StableDiffusionAPI`)

### Usage

#### CLI

1. Copy `config.sample.yml` to `config.yml`
2. Run `./stable-diffusion.py`

You can install the CLI application with `./stable-diffusion.py install`. Make sure to add the path the app gives you to your PATH.

### Python Library

Located in `StableDiffusionAPI`. The main file is `api.py`. It's really not that complicated.

```python
import StableDiffusionAPI

api = StableDiffusionAPI.API(config)
r = api.create_hypernetwork('poo poo pee pee')
print(r)
```
