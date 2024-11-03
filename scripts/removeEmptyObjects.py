import json
import sys

def removeEmptyObjects(metadata: dict, output_file: str):
    for key in list(metadata.keys()):
        if metadata[key]['description'] == "" or metadata[key]['visual'] is None or metadata[key]['visual'] == {}:
            del metadata[key]
    with open(output_file, 'w', encoding='utf-8') as outputfile:
        json.dump(metadata, outputfile, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file.json> <output_file.json>")
        sys.exit(1)

    input_file = sys.argv[1]
    cleaned_file = sys.argv[2]

    with open(input_file, 'r', encoding='utf-8') as infile:
        metadata = json.load(infile)
        
    removeEmptyObjects(metadata, cleaned_file)
