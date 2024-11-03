# a file for housing all the mutation functions

import json
from VisualContextualClassifier import VisualContextualClassifier
from .utils import download_spacy



def splitMetaData(metadata):
    nlp=download_spacy()
    for entry in metadata.values():
        if entry['description']:
            desc = nlp(entry['description'])
            temp_dict = {}
            for idx, sentence in enumerate(desc.sents):
                temp_dict[idx] = str(sentence)
            entry['sentences'] = temp_dict
        else:
            entry['sentences'] = None

def visualContextualBins(metadata):
    nlp=download_spacy()
    prediction_file = "predictions.json"
    classifier=VisualContextualClassifier()
    prediction_data = {}
    for idx1, entry in metadata.items():
        if entry['description']:
            temp_vdict = {} # visual sentences
            temp_cdict = {} # contextual sentences
            temp_sent_dict = {} # {sentence#: {"v/c":probability}}
            for idx2, sentence in enumerate(nlp(entry["description"]).sents):
                sentence=str(sentence)
                temp_pred_dict = {} # {"v/c":probability}
                vis_con = classifier.predict(sentence)
                if vis_con['visual'] >= vis_con['contextual']:
                    temp_vdict[idx2] = sentence
                    temp_pred_dict["v"] = vis_con['visual']
                    temp_pred_dict["c"] = vis_con['contextual']
                else:
                    temp_cdict[idx2] = sentence
                    temp_pred_dict["v"] = vis_con['visual']
                    temp_pred_dict["c"] = vis_con['contextual']
                temp_sent_dict[idx2] = temp_pred_dict
            entry['visual'] = temp_vdict
            entry['contextual'] = temp_cdict
            prediction_data[idx1] = temp_sent_dict
        # if no description/sentences
        else:
            entry['visual'] = None
            entry['contextual'] = None
    with open(prediction_file,'w',encoding='utf-8') as outputfile:
      outputfile.write(json.dumps(prediction_data,indent=4))


FUNCTION_DICT={
    "splitMetaData":splitMetaData,
    "visualContextualBins":visualContextualBins,
}