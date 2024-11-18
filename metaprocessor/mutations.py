# a file for housing all the mutation functions

import json
import random
from VisualContextualClassifier import VisualContextualClassifier
from .utils import download_spacy



def splitMetaData(metadata:dict):
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

def visualContextualBins(metadata:dict):
    """
    Updates metadata by splitting descriptions into visual/contextual sentences, and
    adds "visual" and "contextual" fields to metadata to contain the sorted sentences.
    Also creates "predictions.json", which contains prediction data on each sentence.
    """
    nlp=download_spacy()
    prediction_file = "predictions.json"
    classifier=VisualContextualClassifier()
    prediction_data = {}
    for idx1, entry in metadata.items():
        if entry['description']:
            processed_description = [] # process any issues missed during scraping
            temp_vdict = {} # visual sentences
            temp_cdict = {} # contextual sentences
            temp_sent_dict = {} # {sentence#: {"v/c":probability}}
            for idx2, sentence in enumerate(nlp(entry["description"]).sents):
                sentence=str(sentence)
                processed_description.append(sentence.strip())
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
            entry['description'] = " ".join(processed_description)
            entry['visual'] = temp_vdict
            entry['contextual'] = temp_cdict
            prediction_data[idx1] = temp_sent_dict
        # if no description/sentences
        else:
            entry['visual'] = None
            entry['contextual'] = None
    with open(prediction_file,'w',encoding='utf-8') as outputfile:
      outputfile.write(json.dumps(prediction_data,indent=4))

def removeEmptyObjects(metadata:dict):
    """
    Remove any samples from metadata that do not contain descriptions, or only contain contextual descriptions.
    """
    for key in list(metadata.keys()):
        if metadata[key]['description'] == "" or metadata[key]['visual'] is None or metadata[key]['visual'] == {}:
            del metadata[key]

def removeDuplicates(metadata:dict, visual_duplicates:dict):
    """
    Remove samples that share exact match descriptions with other samples.
    """
    # every as_is dupe is a visual_dupe (after removal of contextual-only samples), so just delete visual_dupes
    for v_dupe_keys in visual_duplicates.values():
        for v_key in v_dupe_keys[1:]: # only keep first instance of dupes
            if v_key in metadata:
                del metadata[v_key]

FUNCTION_DICT={
    "splitMetaData":splitMetaData,
    "visualContextualBins":visualContextualBins,
}