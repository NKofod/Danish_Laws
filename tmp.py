import requests 
import json 
from bs4 import BeautifulSoup as Soup

with open("Results.json","r") as infile: 
    tmp_dict = json.load(infile)
print(len(tmp_dict))