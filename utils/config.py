import json

CONFIG_PATH = "config.json" 
_config = None

def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)

def get_config():
    global _config
    if _config is None:
        _config = load_config(CONFIG_PATH)
    return _config