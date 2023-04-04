import requests 
import json 
from bs4 import BeautifulSoup as Soup
import re 
from rich.progress import Progress
import os 
def get_all_documents(year,in_links):
    links = []
    base_url = f"https://www.retsinformation.dk/api/documentsearch?o=80&ps=100&yl={year}&yh={year}"
    tmp_request = requests.get(base_url)
    tmp_json = json.loads(tmp_request.content)
    if int(tmp_json['pageCount']) != 0:
        for i in tmp_json['documents']:
            links.append(i['retsinfoLink'])
    if int(tmp_json['pageCount']) > 1: 
        for i in range(1,int(tmp_json['pageCount'])):
            print(f"{year}\t{i:02.0f}\t{len(in_links)+len(links):08.0f}")
            tmp_request = requests.get(base_url+f"&page={i}")
            tmp_json = json.loads(tmp_request.content)
            for i in tmp_json['documents']:
                links.append(i['retsinfoLink'])
    return links 

def get_accn(links): 
    accn_codes = []
    base_url = "https://www.retsinformation.dk/api/document"
    with open("finished.txt","r") as infile:
        done = json.load(infile)
    count = 0 
    with Progress() as progress:
        task_1 = progress.add_task("[red]Downloading",total=len(links))
        for link in links: 
            if link in done: 
                progress.update(task_1,advance=1)
                continue 
            done.append(link)
            tmp_url = base_url + link 
            tmp_request = requests.get(tmp_url)
            try: 
                tmp_json = json.loads(tmp_request.content) 
            except json.JSONDecodeError:
                with open("errors.txt","a") as outfile:
                    outfile.write(link + "\n")
                    progress.update(task_1,advance=1)
                
            for meta in tmp_json[0]['metadata']:
                if meta['displayName'] == 'Accession':
                    accn_codes.append(meta['displayValue'])
                    try: 
                        with open(f"./files/{meta['displayValue']}.json","w") as outfile:
                            json.dump(tmp_json[0],outfile,indent=4,ensure_ascii=False)
                        progress.update(task_1,advance=1)
                    except UnicodeEncodeError as e: 
                        with open("errors.txt","a") as outfile:
                            outfile.write(meta['displayValue'] + "\n")
                        progress.update(task_1,advance=1)
            if count % 20 == 0: 
                with open("finished.txt", "w") as outfile:
                    json.dump(done,outfile)
        done = []
        with open("finished.txt","w") as outfile:
            json.dump(done,outfile)
    return accn_codes


if __name__ == '__main__':
    if os.path.isfile("./years.json"):
        with open("./years.json","r") as infile: 
            years = json.load(infile)
        if max(years) != 2023:
            with open("./links.json","r") as infile:
                links = json.load(infile)
            for i in range(max(years)+1,2023):
                print(f"{i}\t00\t{len(links):08.0f}")
                links.extend(get_all_documents(i,links))
                with open("./links.json","w") as outfile:
                    json.dump(links,outfile,indent=4,ensure_ascii=False)
                years.append(i)
                with open("./years.json","r") as outfile: 
                    json.dump(years,outfile)
    else: 
        count = 0
        years = []
        links = []
        for i in range(1665,2023):
            print(f"{i}\t00\t{len(links):08.0f}")
            links.extend(get_all_documents(i,links))
            with open("./links.json","w") as outfile:
                json.dump(links,outfile,indent=4,ensure_ascii=False)
            years.append(i)
            if i < 1940 and i % 10 == 0: 
                with open("./years.json","w") as outfile: 
                    json.dump(years,outfile)
            elif i >= 1940: 
                with open("./years.json","w") as outfile: 
                    json.dump(years,outfile)
    get_accn(links)
