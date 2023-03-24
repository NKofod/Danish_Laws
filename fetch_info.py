from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
import time 
import json 

with open("Results.json","r") as infile:
    links = json.load(infile)

link_dict = {}
tmp_count = 0
with open("Info.json","r") as infile:
    out_dict = json.load(infile)
links = [i for i in links if f"https://www.retsinformation.dk{i}" not in out_dict.keys()]

for i in range(8):
    link_dict[i] = []
    for j in range(tmp_count, tmp_count + int(links/8)):
        link_dict[i].append(links[j])


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

with open("Info.json","r") as infile:
    out_dict = json.load(infile)

with open("running.json","r") as infile:
    running = json.load(infile)
if len(running) == 0: 
    test = 0
else: 

count = 0
for link in links: 
    count += 1 
    url = f"https://www.retsinformation.dk{link}"
    if url in out_dict.keys():
        continue 
    print(count)
    driver.get(url)
    time.sleep(1.5)
    try: 
        duplicate = driver.find_element(By.CLASS_NAME, "eli-dublicate-modal")
        buttons = driver.find_elements(By.TAG_NAME,"button")
        buttons = [i for i in buttons if i.text == "Vælg"]
        print(buttons)
        buttons[0].click()

        time.sleep(1)
        elem = driver.find_element(By.CLASS_NAME,"metadata-box-content")
        info = elem.get_attribute('innerHTML')
        out_dict[url + "0"] = str(info) 
        if count % 10 == 0:
            with open("Info.json","w") as outfile: 
                json.dump(out_dict,outfile,indent=4,ensure_ascii=False)
        driver.get(url)
        time.sleep(1.5)
        duplicate = driver.find_element(By.CLASS_NAME, "eli-dublicate-modal")
        buttons = driver.find_elements(By.TAG_NAME,"button")
        buttons = [i for i in buttons if i.text == "Vælg"]
        print(buttons)
        buttons[1].click()
        time.sleep(1)
        elem = driver.find_element(By.CLASS_NAME,"metadata-box-content")
        info = elem.get_attribute('innerHTML')
        out_dict[url + "1"] = str(info) 
        if count % 10 == 0:
            with open("Info.json","w") as outfile: 
                json.dump(out_dict,outfile,indent=4,ensure_ascii=False)
    except KeyboardInterrupt:
        quit()
    except:
        elem = driver.find_element(By.CLASS_NAME,"metadata-box-content")
        info = elem.get_attribute('innerHTML')
        out_dict[url] = str(info) 
        if count % 10 == 0:
            with open("Info.json","w") as outfile: 
                json.dump(out_dict,outfile,indent=4,ensure_ascii=False)
    