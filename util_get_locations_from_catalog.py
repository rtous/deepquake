import argparse
import os
import catalog

if __name__ == "__main__":
    print ("\033[92m******************** UTIL *******************\033[0m ")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str)
    parser.add_argument("--output_path", type=str)
    args = parser.parse_args()

    catalogs = {"output/data_prep_datos1/catalog.json", "output/data_prep_datos2/catalog.json"};

    locations = []
    for c in catalogs: 
        print("Extracting locations from "+c)
        cat = catalog.Catalog()
        cat.import_json(c)
        locations = locations+cat.getLocations()
   


    

        