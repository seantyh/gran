import argparse
import gran

def main(args):
    gran.process_google_ngrams(args.google_ngram_path)    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("google_ngram_path")

    args = parser.parse_args()
    main(args)