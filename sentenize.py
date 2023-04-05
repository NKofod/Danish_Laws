import json
from bs4 import BeautifulSoup as Soup 
import os 
import re 
from joblib import Parallel, delayed
import multiprocessing
     

file_list = list(os.walk("./files/"))[0][2]

with open(f"./files/{file_list[3]}","r",encoding="latin-1") as infile:
    tmp_file = json.load(infile)
    
def sentenize(filename): 
    try: 
        with open(filename,"r",encoding="latin-1") as infile:
            raw_file = json.load(infile)
        raw_soup = Soup(raw_file['documentHtml'],features='lxml')
        

        current_sentence = ""
        out_sentences = []
        try: 
            for para in raw_soup.find_all('p'):
                tmp_string = str(para.text.strip())
                if tmp_string != "":
                    if tmp_string[-1] == "." or tmp_string[-1] == ":": 
                        current_sentence +=" " + tmp_string
                        while re.search("[a-åA-Å]\.\s[A-Z]",current_sentence):
                            out_sentences.append(current_sentence[:re.search("[a-åA-Å]\.\s[A-Z]",current_sentence).start()+2].strip())
                            current_sentence = current_sentence[re.search("[a-åA-Å]\.\s[A-Z]",current_sentence).start()+2:].strip()
                        out_sentences.append(current_sentence)
                        current_sentence = ""
                    else:
                        if current_sentence != "":
                            current_sentence += " " + tmp_string
                        else:
                            current_sentence = tmp_string
        except AttributeError:
            print(filename)
    except KeyboardInterrupt:
        quit() 
    except:
        return False
    return out_sentences


# what are your inputs, and what operation do you want to 
# perform on each input. For example...
inputs = range(10) 
def processInput(file,count):
    if count % 100 == 0:
        print(count)
    sentences = sentenize(f"./files/{file}")
    if sentences:
        with open(f"./text_files/{file[:-5]}.txt","w") as outfile:
            for sentence in sentences:
                outfile.write(sentence + "\n")

num_cores = multiprocessing.cpu_count()
    
Parallel(n_jobs=num_cores)(delayed(processInput)(i,idx) for idx, i in enumerate(file_list))

