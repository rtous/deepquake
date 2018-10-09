import argparse
import os
import catalog

if __name__ == "__main__":
    print ("\033[92m******************** STEP 0/5. PREPROCESSING STEP 0/4. IMPORT METADATA AND SAVE INTO OUR OWN FORMAT (JSON) *******************\033[0m ")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str)
    parser.add_argument("--output_path", type=str)
    args = parser.parse_args()
    if not os.path.exists(os.path.dirname(args.output_path)):
        os.makedirs(os.path.dirname(args.output_path))
    c = catalog.Catalog()
    c.import_sfiles(args.input_path)
    c.export_json(args.output_path)


    

        