import requests
import json
import random

def get_random_something(content_type):
    """Options are nouns, things, and words"""
    def get_random_list():
        with open(f'data/random_{content_type}.json') as jsonfile:
            json_content = json.load(jsonfile)
            random_list = json_content['data']
            return random_list
    def get_random_item():
        random_item = random.choice(get_random_list())
        return random_item
    return get_random_list, get_random_item

get_random_words, get_random_word = get_random_something('words')
get_random_things, get_random_thing = get_random_something('things')
get_random_nouns, get_random_noun = get_random_something('nouns')