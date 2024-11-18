import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from metaprocessor import Processor, setSplit

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/setSplit.py <input_file.json>")
        sys.exit(1)

    input_file = sys.argv[1]

    processor=Processor(input_file)

    processor.iterate(setSplit)