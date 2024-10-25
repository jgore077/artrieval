# A file used for writing functions that iterate over the data

def predictionsUncertaintyCheck(predictions:dict):
    THRESHOLD=.10
    num_unsure_predictions=0
    for id in predictions:
        for i,prediction in enumerate(predictions[id]):
            if abs(predictions[id][prediction]["v"]-predictions[id][prediction]["c"])<THRESHOLD:
                print(f"model had an unsure prediction for sentence {i} in object {id}")
                num_unsure_predictions+=1
    print(f"{num_unsure_predictions} predictions were detected with a threshold of {THRESHOLD}")
ITERATION_DICT={
    "predictionsUncertaintyCheck":predictionsUncertaintyCheck
}