import os
import json
import argparse
import requests
import config
import attack
import pdb

def flatten_dict(nested_dict, parent_key='', sep='.'):
    items = []
    for key, value in nested_dict.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


parser = argparse.ArgumentParser(description="Third-party attack experiment script")
parser.add_argument("-r", "--response_file", action="store_true", help="Response json file")
parser.add_argument("-o", "--output_file", action="store_true", help="Response json file")
parser.add_argument("atk_mode", type=str, help="Attack mode")
parser.add_argument("atk_method", type=str, help="How to attack")
args = parser.parse_args()

atk_mode = args.atk_mode
atk_method = args.atk_method

# The API key and url
os.environ["API_KEY"] = config.API_KEY
# os.environ["X-RapidAPI-Host"] = config.API_HOST

# os.environ["TOKENIZERS_PARALLELISM"] = "false"


url = config.API_URL

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, 'question_set_weather.json')

# pdb.set_trace() 
with open(file_path) as question_set:
    question_set_json = json.load(question_set)
    question_set.close()

    questions = question_set_json['Questions']
    locations = question_set_json['Locations']

    for idx, question in enumerate(questions):
        print(question)
        location = locations[idx]

        querystring = {
            "key": config.API_KEY,
            "q": location,
            "aqi": "no"
        }

        response_json = requests.get(url, params=querystring).json()
        response_json = flatten_dict(response_json)

        attack.Attack.attack_methods(config.API_NAME, atk_mode, response_json, question, atk_method, backdoor=False)

    for idx, question in enumerate(questions):
        location = locations[idx]

        querystring = {
            "key": config.API_KEY,
            "q": location,
            "aqi": "no"
        }

        response_json = requests.get(url, params=querystring).json()
        response_json = flatten_dict(response_json)
        
        attack.Attack.attack_methods(config.API_NAME, atk_mode, response_json, question, atk_method, backdoor=True)
