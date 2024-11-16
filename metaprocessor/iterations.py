# A file used for writing functions that iterate over the data
from .utils import assemble_visual_description
import json
import csv


def predictionsUncertaintyCheck(predictions:dict):
    THRESHOLD=.10
    num_unsure_predictions=0
    for id in predictions:
        for i,prediction in enumerate(predictions[id]):
            if abs(predictions[id][prediction]["v"]-predictions[id][prediction]["c"])<THRESHOLD:
                print(f"model had an unsure prediction for sentence {i} in object {id}")
                num_unsure_predictions+=1
    print(f"{num_unsure_predictions} predictions were detected with a threshold of {THRESHOLD}")

def countBinFields(metadata:dict, result_path:str):
    # get counts on desired aspects of metadata
    results = {}
    as_is_description_lengths = []
    visual_description_lengths = []
    visual_sentences_length = 0
    contextual_sentences_length = 0
    for sample in metadata.values():
        if sample["visual"] and sample["contextual"]: # if sample has visual and contextual sentences
            visual_description_lengths.append(len(assemble_visual_description(sample["visual"])))
            results["visual_sent_count"] = results.get("visual_sent_count", 0) + len(sample["visual"])
            results["contextual_sent_count"] = results.get("contextual_sent_count", 0) + len(sample["contextual"])
            results["visual_samples"] = results.get("visual_samples", 0) + 1
            results["visual+contextual_samples"] = results.get("visual+contextual_samples", 0) + 1
            for vSentence in sample["visual"].values():
                visual_sentences_length += len(vSentence.split())
            for cSentence in sample["contextual"].values():
                contextual_sentences_length += len(cSentence.split())
        elif sample["visual"]: # if sample only has visual sentences
            visual_description_lengths.append(len(sample["description"]))
            results["visual_sent_count"] = results.get("visual_sent_count", 0) + len(sample["visual"])
            results["visual_samples"] = results.get("visual_samples", 0) + 1 
            for vSentence in sample["visual"].values():
                visual_sentences_length += len(vSentence.split())
        as_is_description_lengths.append(len(sample["description"]))
    results["avg_len_as_is_description"] = sum(as_is_description_lengths) / len(as_is_description_lengths)
    results["avg_len_visual_description"] = sum(visual_description_lengths) / len(visual_description_lengths)
    results["max_len_as_is_description"] = max(as_is_description_lengths)
    results["max_len_visual_description"] = max(visual_description_lengths)
    results["min_len_as_is_description"] = min(as_is_description_lengths)
    results["min_len_visual_description"] = min(visual_description_lengths)
    results["average_len_visual"] = visual_sentences_length / results["visual_sent_count"]
    results["average_len_contextual"] = contextual_sentences_length / results["contextual_sent_count"]
    results["average_len_sentence"] = (visual_sentences_length + contextual_sentences_length) / (results["visual_sent_count"] + results["contextual_sent_count"])

    with open(result_path, "w") as f:
        json.dump(results, f, indent=4)
    
def makeQrelAndQuerys(bins:dict,qrels_path,querys_path,duplicates,as_is=False):
    # as-is querys of the entire description and are prefixed with 1
    # visual querys are prefixed with 0
    prefix="1" if as_is else "0"
    qrels=[]
    querys={}
    query=None
    for key in bins:
        query_id=prefix+key
    
        if as_is:
            query=bins[key]["description"]
        else:
            query=assemble_visual_description(bins[key]["visual"])
        
        skip=False
        # If the query has duplicates we enter this loop
        if query in duplicates:
            duplicate_querys=duplicates[query]
            for id in duplicate_querys:
                # if it has already been saved we set query_id to the previous entry
                # We also set a boolean variable that determines if it gets added to the .json file
                if prefix+id in querys:
                    query_id=prefix+id
                    skip=True
        
        qrels.append([query_id,0,key,1])
        if not skip:
            querys[query_id]=query

    with open(qrels_path,'w',encoding="utf-8",newline="") as qrel_file:
        writer=csv.writer(qrel_file, delimiter='\t',quoting=csv.QUOTE_MINIMAL)
        for row in qrels:
            writer.writerow(row)
            
    with open(querys_path,'w',encoding='utf-8') as query_file:
        query_file.write(json.dumps(querys,indent=4,ensure_ascii=False))

def findDuplicateQuerys(metadata:dict)->tuple[dict[str,list],dict[str,list]]:
    visual={}
    as_is={}
    for key in metadata:
        vsent=assemble_visual_description(metadata[key]["visual"])
        description=metadata[key]["description"]
        if vsent not in visual:
            visual[vsent]=[key]
        else:
            visual[vsent].append(key)
        if description not in as_is:
            as_is[description]=[key]
        else:
             as_is[description].append(key)
             
    # We filter out single occurences with these comprehensions, only returning querys with 2 or more duplicates
    return {k: v for k, v in visual.items() if len(v) > 1},{k: v for k, v in as_is.items() if len(v) > 1}

ITERATION_DICT={
    "predictionsUncertaintyCheck":predictionsUncertaintyCheck
}