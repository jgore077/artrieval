from metaprocessor import Processor,visualContextualBins

processor_ob=Processor('metadata.json')


processor_ob.mutate(visualContextualBins,'bins.json')