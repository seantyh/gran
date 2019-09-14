import re
from gzip import GzipFile
from multiprocessing import Pool
from functools import partial
import pickle
import redis
import requests
from bs4 import BeautifulSoup
from .utils import *
from . import config

class GoogleNgramData:
    def __init__(self, link_list, crit_freq=10):
        self.links = link_list
        self.__ngdata = {}
        self.__freq_vec = []
        print(f"CRIT_FREQ:{crit_freq}")
        self.CRIT_FREQ = crit_freq

    def process(self):
        freq_vec = []
        ngdata = {}

        proc_func = partial(self.process_single, crit_freq=self.CRIT_FREQ)
        pool = Pool(processes=config.N_PROC)
        for _ in tqdm(pool.imap_unordered(
            proc_func, self.links), total=len(self.links)):
            pass

        self.__freq_vec = freq_vec
        self.__ngdata = ngdata

    def process_single(self, link_x, crit_freq):
        prev_words = ""
        freq_buf = 0
        cjk_pat = re.compile(r'[^\u4e00-\u9fff]')
        gin = GzipFile(fileobj=requests.get(link_x, stream=True).raw)
        r = redis.Redis(config.REDIS_HOST, port=config.REDIS_PORT, db=3)

        for ln_i, ln in enumerate(gin):
            try:
                tok, year, tokfreq, volfreq = ln.decode().split("\t")
                word_list = [x.split('_')[0] for x in tok.split()]
                words = '|'.join(word_list)
                # ignore non-cjk entries
                if any(not x or cjk_pat.match(x) for x in word_list):
                    continue
                
                freq_buf += int(tokfreq)
                
                if prev_words != words and freq_buf > crit_freq:
                    r.set(words, freq_buf)
                    freq_buf = 0

            except Exception as ex:
                import traceback
                traceback.print_exc()
                print("ERROR" + str(ex))
                # import pdb; pdb.set_trace()

            prev_words = words
            # if ln_i > 100000: break

        if freq_buf > crit_freq:
            r.set(words, freq_buf)
            freq_buf = 0
        gin.close()

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