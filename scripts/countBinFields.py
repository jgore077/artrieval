import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from metaprocessor import Processor,countBinFields

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python countBinFields.py <input_file.json> <output_file.json>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    processor=Processor(input_file)
        
    processor.iterate(countBinFields, output_file)