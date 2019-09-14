import re
import argparse
import requests
from bs4 import BeautifulSoup
from pathlib import Path

import sys
gran_path = (Path(__file__).parent/"../").resolve()
sys.path.append(str(gran_path))
import gran

import logging
logging.basicConfig()

def main(win, crit_freq, freq_only=True, debug=False):
    ngrams_index_url = "http://storage.googleapis.com/books/ngrams/books/datasetsv2.html"
    ngrams_index = requests.get(ngrams_index_url)
    ngrams_dom = BeautifulSoup(ngrams_index.text, 'lxml')
    logging.info("Google NGram index retrieved")

    ng_links = find_links(ngrams_dom, f'{win}gram')
    if debug:
        m = int(len(ng_links)/2)
        ng_links = ng_links[m:m+3]

    gram_data = gran.GoogleNgramData(ng_links, crit_freq)
    gram_data.process()
    ng_prefix = ["", "uni", "bi", "tri", "quad", "penta"]
    freq_suffix = ["freq", "ngdata"][int(freq_only)]
    if debug:
        ng_path = gran.get_cache_path("lang_model", f"{ng_prefix[win]}_grams_f{freq_suffix}_debug.pkl")
    else:
        ng_path = gran.get_cache_path("lang_model", f"{ng_prefix[win]}_f{freq_suffix}_grams.pkl")
    gram_data.save(ng_path)

def find_links(ngram_index, category):
    atags = ngram_index.find_all("a", {
        'href': re.compile(f'googlebooks-chi-sim-all-{category}-2012')})
    links = [x.get('href') for x in atags]
    links = [x for x in links if x]
    return links

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("window", type=int)
    parser.add_argument("crit_freq", type=int)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--freq-only", action="store_true")
    args = parser.parse_args()

    main(args.window, args.crit_freq, args.freq_only, args.debug)

