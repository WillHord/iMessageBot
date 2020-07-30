import json

#TODO: create json if json is not present - Reset json

def getwhoisJson():
        with open('whois.json', 'r') as data:
            tempjson = json.load(data)
        return tempjson

def writetowhoisJson(dictionary):
    with open('whois.json', 'w') as whoisjson:
        json.dump(dictionary, whoisjson, indent=4,
                separators=(", ", ": "),
                sort_keys=True)