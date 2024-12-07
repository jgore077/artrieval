
import os.path
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from metaprocessor import Processor,findDuplicateQuerys


data_path=sys.argv[1]

processor=Processor(data_path)
print(f"Total number of objects in the dataset: {len(processor.metadata)}")
v,a=processor.iterate(findDuplicateQuerys)
print(f"Visual Duplicates Querys: {len(v)}",f"As-Is Duplicate Querys: {len(a)}")

with open("v_dupes.json",'w',encoding="utf-8") as f:
    json.dump(v,f,indent=4,ensure_ascii=False)
with open("a_dupes.json",'w',encoding="utf-8") as f2:
    json.dump(a,f2,indent=4,ensure_ascii=False)

v_num=0
a_num=0
for v_arr,a_arr in zip(v.values(),a.values()):
    v_num+=len(v_arr)
    a_num+=len(a_arr)
    
print(f"Visual Querys: {v_num}",f"As-Is Querys: {a_num}")