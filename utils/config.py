import json

CONFIG_PATH = "config.json"

def load_config(config_file='config.json'):
    with open(config_file, 'r') as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)
    
config = load_config()