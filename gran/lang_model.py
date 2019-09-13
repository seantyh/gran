import re
import requests
from gzip import GzipFile
from bs4 import BeautifulSoup
import pickle
from .utils import *

class GoogleNgramData:
    def __init__(self, link_list, crit_freq=10):
        self.links = link_list
        self.__ngdata = {}
        self.__freq_vec = []
        self.CRIT_FREQ = crit_freq

    def process(self):
        freq_vec = []
        ngdata = {}
        cjk_pat = re.compile(r'[^\u4e00-\u9fff]')
        prev_words = ""

        for link_x in tqdm(self.links):
            gin = GzipFile(fileobj=requests.get(link_x, stream=True).raw)

            for ln_i, ln in enumerate(gin):
                try:
                    tok, year, tokfreq, volfreq = ln.decode().split("\t")
                    word_list = [x.split('_')[0] for x in tok.split()]
                    words = '|'.join(word_list)
                    # ignore non-cjk entries
                    if any(not x or cjk_pat.match(x) for x in word_list):
                        continue
                    
                    ngdata[words] = ngdata.get(words, 0) + int(tokfreq)
                    
                    if prev_words != words:
                        prev_freq = ngdata.get(prev_words, 0)
                        freq_vec.append(prev_freq)
                        if prev_freq < self.CRIT_FREQ and prev_words:
                            del ngdata[prev_words]
                    
                except Exception as ex:
                    import traceback
                    traceback.print_exc()
                    print("ERROR" + str(ex))
                    import pdb; pdb.set_trace()
                
                prev_words = words
                # if ln_i > 100000: break
            
            prev_freq = ngdata.get(prev_words, 0)
            freq_vec.append(prev_freq)
            if prev_freq < self.CRIT_FREQ and prev_words:
                del ngdata[prev_words]
            gin.close()

        self.__freq_vec = freq_vec
        self.__ngdata = ngdata
    
    @property
    def ngdata(self):
        return self.__ngdata

    @property
    def freq_vec(self):
        return self.__freq_vec
    
    def save(self, fpath):
        with open(fpath, "wb") as fout:
            pickle.dump((self.__ngdata, self.__freq_vec), fout)
    
    def load(self, fpath):
        with open(fpath, "rb") as fin:
            self.__ngdata, self.__freq_vec = pickle.load(fin)