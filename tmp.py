import json 

tmp_dict = {}
for i in ["A","B","C"]: 
    tmp_dict[i] = {}
    for j in range(1900,2024):
        tmp_dict[i][j] = False 
        
with open("finished_combos.json","w") as outfile:
    json.dump(tmp_dict,outfile)    
