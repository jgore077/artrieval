
import os.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from metaprocessor import Processor,findDuplicateQuerys


data_path=sys.argv[1]

processor=Processor(data_path)
print(f"Total number of objects in the dataset: {len(processor.metadata)}")
v,a=processor.iterate(findDuplicateQuerys)
print(f"Visual Duplicates Querys: {len(v)}",f"As-Is Duplicate Querys: {len(a)}")

v_num=0
a_num=0
for v_arr,a_arr in zip(v.values(),a.values()):
    v_num+=len(v_arr)
    a_num+=len(a_arr)
    
print(f"Visual Querys: {v_num}",f"As-Is Querys: {a_num}")