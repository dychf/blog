import yaml

def read_config():
    with open('src/config.yaml', 'r') as file:
        data = yaml.safe_load(file)
    return data
    
config = read_config()