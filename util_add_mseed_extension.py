import os
import argparse
import fnmatch

if __name__ == "__main__":

	#USAGE:
	#python util_datos3_add_mseed_extension.py --stream_path=input/datos3/mseed

    parser = argparse.ArgumentParser()
    parser.add_argument("--stream_path",type=str,default=None,
                        help="path to mseed DIRECTORY to process")
    args = parser.parse_args()

    #dir_name = os.path.dirname(args.stream_path)

    stream_files = [file for file in os.listdir(args.stream_path) if
                    fnmatch.fnmatch(file, "*")]

    for stream_file in stream_files:
        src = os.path.join(args.stream_path, stream_file)
        dst = src + ".mseed"
        print("Renaming "+src+" into "+dst)
        os.rename(src, dst) 
        
