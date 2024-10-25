from spacy.cli import download
import spacy

def download_spacy():
    # Downloads spacy model if not already downloaded
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("Downloading 'en_core_web_sm' model...")
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    return nlp