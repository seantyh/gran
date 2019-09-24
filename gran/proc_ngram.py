import pickle
from pathlib import Path
from .utils import tqdm
from opencc import OpenCC

def process_google_ngrams(data_path):
    data_path = Path(data_path)
    cc_inst = OpenCC('s2t')
    s2t = cc_inst.convert

    if not data_path.exists():
        raise FileNotFoundError("Cannot find " + data_path)

    
    with open(data_path, 'rb') as fin:
        data = pickle.load(fin)
        if isinstance(data, tuple):
            data = data[0]

    for item, freq in data.items():
        print(s2t(item), freq)
        break


    