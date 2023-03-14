import requests 
from bs4 import BeautifulSoup as Soup 
import time
import json 

base_url = "https://www.retsinformation.dk/eli/accn/"

with open("log.json","r") as infile: 
    checked = json.load(infile)
with open("active.json","r") as infile: 
    active = json.load(infile)
with open("finished_combos.json","r") as infile: 
    checked_combos = json.load(infile)
count = 0

try: 
    for level in ["A","B","C"]:
        for year in range(1900,2024):
            if checked_combos[level][year]:
                continue 
            for num in range(0,10000000):
                    tmp_url = f"{base_url}{level}{year}{num:07d}/xml"
                    if tmp_url in checked:
                        continue 
                    count += 1
                    if num % 10 == 0: 
                        print(f"{year} - {num}")
                    tmp_req = requests.get(tmp_url)
                    tmp_soup = Soup(tmp_req.content)
                    if "No document found matching ELI request" != tmp_soup.text: 
                        active.append(tmp_url)
                        print("FOUND ONE!!!")
                    checked.append(tmp_url)
                    if count == 1000000:
                        raise GeneratorExit
            checked_combos[level][year] = True 
            checked = []
except KeyboardInterrupt:
    with open("log.json","w") as outfile: 
        json.dump(checked,outfile,indent=4,ensure_ascii=False)
    with open("active.json","w") as outfile: 
        json.dump(active,outfile,indent=4,ensure_ascii=False)
except GeneratorExit: 
    with open("log.json","w") as outfile: 
        json.dump(checked,outfile,indent=4,ensure_ascii=False)
    with open("active.json","w") as outfile: 
        json.dump(active,outfile,indent=4,ensure_ascii=False)