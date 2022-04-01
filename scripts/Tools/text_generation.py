import random
import requests


def list_duplicates_of(seq, item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item, start_at + 1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs


def FetchPoem():
    line_request = random.randrange(1, 100)
    response = requests.get("https://poetrydb.org/linecount,poemcount/{count};1".format(count=line_request))

    return response.json()


def FetchData(poem_to_parse):
    try:
        line_break_indices = list_duplicates_of(poem_to_parse[0]['lines'], "")
    except ValueError:
        line_break_indices = []
    return line_break_indices


def ParseText(poem_to_parse, line_break_indices):
    stances = []
    if len(line_break_indices) > 0:
        start = 0
        for i in range(len(line_break_indices)):
            stance_lines = poem_to_parse[0]['lines'][start:line_break_indices[i]]
            start = line_break_indices[i] + 1
            stances.append(stance_lines)
        stances.append(poem_to_parse[0]['lines'][start:])
    else:
        stances.append(poem_to_parse[0]['lines'])

    return stances
