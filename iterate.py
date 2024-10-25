from metaprocessor import Processor,ITERATION_DICT
import argparse


parser=argparse.ArgumentParser()
parser.add_argument("-m","--metadata",type=str,required=True)
parser.add_argument("-i,","--iteration", type=str,required=True)
parser.add_argument("-o","--output" ,type=str,required=True )

args = parser.parse_args()

processor=Processor(args.metadata)

iteration=args.iteration

if iteration not in ITERATION_DICT:
    raise KeyError(f"{iteration} not in {ITERATION_DICT.keys()}")

processor.iterate(ITERATION_DICT[iteration],args.output)