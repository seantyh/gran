try:
    get_ipython()
    from tqdm import tqdm_notebook as tqdm    
except NameError:
    from tqdm import tqdm
from pathlib import Path

def install_data_cache(name):
    cache_dir = Path(__file__).parent / f"../data/{name}"
    cache_dir.mkdir(parents=True, exist_ok=True)

def get_cache_path(name, path):
    cache_dir = Path(__file__).parent / f"../data/{name}"
    return cache_dir.joinpath(path).resolve()

def get_resource_path(name, path):
    cache_dir = Path(__file__).parent / f"../resource/{name}"
    return cache_dir.joinpath(path).resolve()

def get_word_boundary_index(ngram):
    tokens = ngram.split('|')
    token_len = [len(x) for x in tokens]
    token_delims = [0]
    for len_x in token_len:
        last_delim = token_delims[-1] + len_x
        token_delims.append(last_delim)
    token_delims = token_delims[1:-1]
    return token_delims