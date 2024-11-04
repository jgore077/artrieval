# A file used for writing functions that iterate over the data
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

def countBinFields(predictions:dict, result_path:str):
    # get counts on desired aspects of metadata
    results = {}
    visual_sentences_length = 0
    contextual_sentences_length = 0
    for sample in predictions.values():
        if sample["visual"] and sample["contextual"]:
            results["visual_sent_count"] = results.get("visual_sent_count", 0) + len(sample["visual"])
            results["contextual_sent_count"] = results.get("contextual_sent_count", 0) + len(sample["contextual"])
            results["visual_samples"] = results.get("visual_samples", 0) + 1
            results["visual+contextual_samples"] = results.get("visual+contextual_samples", 0) + 1
            for vSentence in sample["visual"].values():
                visual_sentences_length += len(vSentence.split())
            for cSentence in sample["contextual"].values():
                contextual_sentences_length += len(cSentence.split())
        elif sample["visual"]:
            results["visual_sent_count"] = results.get("visual_sent_count", 0) + len(sample["visual"])
            results["visual_samples"] = results.get("visual_samples", 0) + 1 
            for vSentence in sample["visual"].values():
                visual_sentences_length += len(vSentence.split())
    results["average_len_visual"] = visual_sentences_length / results["visual_sent_count"]
    results["average_len_contextual"] = contextual_sentences_length / results["contextual_sent_count"]
    results["average_len_all"] = (visual_sentences_length + contextual_sentences_length) / (results["visual_sent_count"] + results["contextual_sent_count"])

    with open(result_path, "w") as f:
        json.dump(results, f, indent=4)
    

def makeQrelAndQuerys(bins:dict,qrels_path,querys_path,as_is=False):
    # as-is querys of the entire description and are prefixed with 1
    # visual querys are prefixed with 0
    prefix=1 if as_is else 0
    qrels=[]
    querys={}
    for key in bins:
        query_id=prefix+key
        qrels.append([query_id,0,key,1])
        querys[query_id]=bins[key]["description"] if as_is else ' '.join(bins[key]["visual"].values())

    with open(qrels_path,'w',encoding="utf-8") as qrel_file:
        writer=csv.writer(qrel_file, delimiter='\t',quoting=csv.QUOTE_MINIMAL)
        for row in qrels:
            writer.writerow(row)
            
    with open(querys,'w',encoding='utf-8') as query_file:
        query_file.write(json.dumps(querys,indent=4,ensure_ascii=False))
    
ITERATION_DICT={
    "predictionsUncertaintyCheck":predictionsUncertaintyCheck
}

        