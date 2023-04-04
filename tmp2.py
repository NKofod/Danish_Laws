import requests 
import json 
from rich.progress import Progress
import time 
def get_all_documents(year,tmp_links):
    links = []
    base_url = f"https://www.retsinformation.dk/api/documentsearch?o=80&ps=100&yl={year}&yh={year}"
    tmp_request = requests.get(base_url)
    tmp_json = json.loads(tmp_request.content)
    if int(tmp_json['pageCount']) != 0:
        for i in tmp_json['documents']:
            links.append(i['retsinfoLink'])
    if int(tmp_json['pageCount']) > 1: 
        for i in range(1,int(tmp_json['pageCount'])):
            print(f"{year}\t{i+1:02.0f}\t{len(tmp_links)+len(links):08.0f}")
            tmp_request = requests.get(base_url+f"&page={i}")
            tmp_json = json.loads(tmp_request.content)
            for i in tmp_json['documents']:
                links.append(i['retsinfoLink'])
    return links 

def get_accn(links): 
    accn_codes = []
    base_url = "https://www.retsinformation.dk/api/document"
    with open("finished.txt","r") as infile:
        done = infile.read()
    count = 0 
    reached_current = False 
    with Progress() as progress:
        task_1 = progress.add_task("[red]Downloading",total=len(links))
        for link in links: 
            if done != "":
                if not reached_current and link != done: 
                    progress.update(task_1,advance=1)
                    count += 1 
                    continue 
                elif not reached_current and link == done:
                    reached_current = True 

            
            count += 1 
            print(f"Finished {(count/len(links))*100:07.4f} %")
            tmp_url = base_url + link 
            tmp_request_not_working = True 
            while tmp_request_not_working:
                try:
                    tmp_request = requests.get(tmp_url)
                    tmp_request_not_working = False 
                except KeyboardInterrupt:
                    quit()
                except:
                    print("Waiting a moment...")
                    time.sleep(5)
                    
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
                            outfile.write(link + "\n")
                        progress.update(task_1,advance=1)
            if count % 20 == 0: 
                with open("finished.txt", "w") as outfile:
                    outfile.write(link)
    return accn_codes


if __name__ == '__main__':
    with open("years.json","r") as infile:
        years = json.load(infile)
    if len(years) != 0:
        min_year = max(years) +1 
    else: 
        min_year = 1665
    with open("links.json","r") as infile: 
        links = json.load(infile)
    for i in range(min_year,2024):
        print(f"{i}\t01\t{len(links):08.0f}")
        links.extend(get_all_documents(i,links))
        with open("./links.json","w") as outfile:
            json.dump(links,outfile,indent=4,ensure_ascii=False)
        years.append(i) 
        with open("./years.json","w") as outfile:
            json.dump(years,outfile)
    
    get_accn(links)
