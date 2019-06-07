import json

CONFIG_PATH = "config.json"
with open(CONFIG_PATH, 'r') as config_file:
    config = json.load(config_file)


def test_credentials():
    return config['test']['username'], config['test']['password']