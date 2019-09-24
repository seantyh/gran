import argparse
import gran

def main(args):
    gran.process_google_ngrams(args.google_ngram_path, 
        purge_db=args.purge_db, debug=args.debug)    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("google_ngram_path")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--purge-db", action="store_true")
    args = parser.parse_args()
    main(args)