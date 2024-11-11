import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from metaprocessor import Processor, setSplit

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python setSplit.py <input_file.json> <output_file.json>")
        sys.exit(1)

    input_file = sys.argv[1]
    cleaned_file = sys.argv[2]

    processor=Processor(input_file)

    processor.mutate(setSplit, cleaned_file)