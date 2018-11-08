import argparse
import os
import catalog

if __name__ == "__main__":
    print ("\033[92m******************** IMPORT SIMPLIFIED METADATA AND SAVE INTO OUR OWN FORMAT (JSON) *******************\033[0m ")
    print ("\033[92m******************** WARNING: NO PWAVE ARRIVAL AT STATIONS IN THIS FORMAT *******************\033[0m ")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str)
    parser.add_argument("--output_path", type=str)
    args = parser.parse_args()
    if not os.path.exists(os.path.dirname(args.output_path)):
        os.makedirs(os.path.dirname(args.output_path))
    c = catalog.Catalog()
    c.import_txt(args.input_path)
    c.export_json(args.output_path)