import sys
import json
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from metaprocessor import Processor,removeDuplicates

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python removeDuplicates.py <input_file.json> <output_file.json>")
        sys.exit(1)

    input_file = sys.argv[1]
    cleaned_file = sys.argv[2]
    # requires running findDuplicateQuerys.py script to obtain dupe files
    with open("v_dupes.json", 'r', encoding="utf-8") as f:
        v_dupes = json.load(f)
    with open("a_dupes.json", 'r', encoding="utf-8") as f2:
        a_dupes = json.load(f2)

    processor=Processor(input_file)
        
    processor.mutate(removeDuplicates, cleaned_file, v_dupes, a_dupes)
