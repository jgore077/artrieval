from metaprocessor import *

p=processor.Processor("data/splits/test_original.json", delete=True)
p.mutate(visualContextualBins)
p.mutate(removeEmptyObjects)
visual_dupes, as_is_dupes = p.iterate(findDuplicateQuerys)
p.mutate(removeDuplicates, "test1.json", visual_dupes)
p.iterate(countBinFields, "counts.json")