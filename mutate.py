from metaprocessor import Processor,FUNCTION_DICT
import argparse


parser=argparse.ArgumentParser()
parser.add_argument("-m","--metadata",type=str,required=True)
parser.add_argument("-f","--function", type=str,required=True)
parser.add_argument("-o","--output" ,type=str,required=True)

args = parser.parse_args()

processor=Processor(args.metadata)

func=args.function

if func not in FUNCTION_DICT:
    raise KeyError(f"{func} not in {FUNCTION_DICT.keys()}")

processor.mutate(FUNCTION_DICT[func],args.output)