import pickle
import os
from pathlib import Path
from .utils import *
from opencc import OpenCC
from .ngram_orm import NGram, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def process_google_ngrams(data_path, purge_db=False, debug=False):
    data_path = Path(data_path)
    cc_inst = OpenCC('s2t')
    s2t = cc_inst.convert

    dbpath = get_cache_path("lang_model", "ngram_db.sqlite3")

    if dbpath.exists() and purge_db:
        os.remove(dbpath)
    
    if not dbpath.exists():
        to_initialize = True
    else:
        to_initialize = False
    
    print("dbpath: ", str(dbpath.resolve().absolute()))
    engine = create_engine("sqlite:///" + str(dbpath.resolve().absolute()))
    Session = sessionmaker(bind=engine)
    sess = Session()

    if to_initialize:
        print("initializing")
        Base.metadata.create_all(engine)
    
    if debug:
        data = {"測試|字串":123, "另|一|個": 3}
    else:
        print("loading ngram data")
        with open(data_path, 'rb') as fin:
            data = pickle.load(fin)
            if isinstance(data, tuple):
                data = data[0]

    counter = 0
    for item, freq in tqdm(data.items()):
        ng_text = s2t(item.replace("|", ""))
        ngram_x = NGram(ngram=ng_text, ncharac=len(ng_text), freq=freq)
        delims = get_word_boundary_index(item)
        ngram_x.delim = ",".join(str(x) for x in delims)
        sess.add(ngram_x)
        counter += 1
        if counter > 1000:
            sess.commit()
            counter = 0

    sess.commit()
    
    