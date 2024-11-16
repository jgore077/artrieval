
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from metaprocessor import Processor,makeQrelAndQuerys,findDuplicateQuerys


data_path=sys.argv[1]
EXP_DIR="data/as_is_v_visual/"
AS_IS_QREL="as_is.tsv"
AS_IS_QUERYS="as_is.json"
VISUAL_QREL="visual.tsv"
VISUAL_QUERYS="visual.json"

os.makedirs(EXP_DIR,exist_ok=True)

processor=Processor(data_path)
visual_duplicates,as_is_duplicates=processor.iterate(findDuplicateQuerys)
processor.iterate(makeQrelAndQuerys,EXP_DIR+AS_IS_QREL,EXP_DIR+AS_IS_QUERYS,as_is_duplicates,as_is=True)
processor.iterate(makeQrelAndQuerys,EXP_DIR+VISUAL_QREL,EXP_DIR+VISUAL_QUERYS,visual_duplicates)