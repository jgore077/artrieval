
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from metaprocessor import Processor,makeQrelAndQuerys,findDuplicateQuerys,write_qrel,write_querys


data_path=sys.argv[1]
VISUAL_PREFIX="0"
AS_IS_PREFIX="1"
EXP_DIR="data/as_is_v_visual/"
AS_IS_QREL_PATH="as_is.tsv"
AS_IS_QUERYS_PATH="as_is.json"
VISUAL_QREL_PATH="visual.tsv"
VISUAL_QUERYS_PATH="visual.json"

os.makedirs(EXP_DIR,exist_ok=True)

processor=Processor(data_path)
visual_duplicates,as_is_duplicates=processor.iterate(findDuplicateQuerys)
as_is_querys,as_is_qrels=processor.iterate(makeQrelAndQuerys,EXP_DIR+AS_IS_QREL_PATH,EXP_DIR+AS_IS_QUERYS_PATH,as_is_duplicates,as_is=True,write=False)
visual_querys,visual_qrels=processor.iterate(makeQrelAndQuerys,EXP_DIR+VISUAL_QREL_PATH,EXP_DIR+VISUAL_QUERYS_PATH,visual_duplicates,write=False)


# After some discussion we realized that the mis-aligment (differing sizes in the query files) will effect the as-is vs. visual experiment
# We need to remove the visual duplicates in as_is_querys (querys that appear in as_is_querys but not visual_querys)
# A complete redesign of makeQrelsAndQuerys was not considered because the way we didn't want to rewrite the way we identify duplicate querys
# This code block below could be removed if a better way to identify duplicates is found.


for key in processor.metadata.keys():
    as_is_key=AS_IS_PREFIX+key
    visual_key=VISUAL_PREFIX+key
    if as_is_key in as_is_querys and not visual_key in visual_querys:
        del as_is_querys[as_is_key]

        
# assert that the querys are the same size
assert len(visual_querys)==len(as_is_querys)
assert len(as_is_qrels)==len(visual_qrels)


write_querys(EXP_DIR+AS_IS_QUERYS_PATH,as_is_querys)
write_querys(EXP_DIR+VISUAL_QUERYS_PATH,visual_querys)
write_qrel(EXP_DIR+AS_IS_QREL_PATH,as_is_qrels)
write_qrel(EXP_DIR+VISUAL_QREL_PATH,visual_qrels)