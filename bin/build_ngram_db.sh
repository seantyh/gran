#! /bin/bash
python3 bin/proc_ngram.py data/lang_model/uni_grams.pkl --purge
python3 bin/proc_ngram.py data/lang_model/bi_grams.pkl
python3 bin/proc_ngram.py data/lang_model/tri_grams.pkl
python3 bin/proc_ngram.py data/lang_model/quad_grams.pkl
python3 bin/proc_ngram.py data/lang_model/penta_grams.pkl