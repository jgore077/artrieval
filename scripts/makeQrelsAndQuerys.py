
import os.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from metaprocessor import Processor,makeQrelAndQuerys


data_path=sys.argv[1]
AS_IS_QREL="as_is.tsv"
AS_IS_QUERYS="as_is.json"
VISUAL_QREL="visual.tsv"
VISUAL_QUERYS="visual.json"

processor=Processor(data_path)

processor.iterate(makeQrelAndQuerys,AS_IS_QREL,AS_IS_QUERYS,as_is=True)
processor.iterate(makeQrelAndQuerys,VISUAL_QREL,VISUAL_QUERYS)