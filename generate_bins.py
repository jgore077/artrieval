from metaprocessor import Processor,visualContextualBins,removeEmptyObjects

p=Processor("metadata.json", delete=True)
p.mutate(visualContextualBins)
p.mutate(removeEmptyObjects,"bins.json")