from metaprocessor import *

p=processor.Processor("metadata.json", delete=True)
p.mutate(visualContextualBins)
p.mutate(removeEmptyObjects,"test.json")