import random
import requests
import json

poems = []


def FetchPoem():
    line_request = random.randrange(1, 300)
    response = requests.get("https://poetrydb.org/linecount,poemcount/{count};1".format(count=line_request))
    return response.json()


for i in range(10000):
    poem_to_add = FetchPoem()
    if len(poem_to_add) == 1:
        if poem_to_add[0] not in poems:
            poem_to_add = poem_to_add[0]
            poem_to_add['id'] = len(poems) + 1
            poems.append(poem_to_add)
            print(len(poems))


with open("../database/poems.json", "w") as f:
    json.dump(poems, f, indent=4)


