import json

CONFIG_PATH = "config.json"
with open(CONFIG_PATH, 'r') as config_file:
    config = json.load(config_file)


def azure_db():
    return config['db']['azure']['access_uri']


def azure_storage():
    return config['storage']['azure']['account_name'], config['storage']['azure']['access_key']


def secret_key():
    return config['secret_key']


def engine_url():
    return config['engine']['url']


def engine_credentials():
    return config['engine']['username'], config['engine']['secret']
