# DeepQuake

## 1 Introduction

This repository contains code for applying a deep convolutional neural network, called UPC-UCV, over single-station three-channel
signal windows for P-wave earthquake detection and source region estimation in north central Venezuela. The model is optimized and trained for the [CARABOBO2019](https://github.com/rtous/CARABOBO2019) dataset but it can be trained over other datasets as well. 

## 2 Acknowledgements

If you find this repository useful for your research, please cite the original publication:


	@article{Tous2020,
	    author = {R. Tous and L. Alvarado and B. Otero and L. Cruz and O. Rojas},
	    title = {Deep Neural Networks for Earthquake Detection and Source Region Estimation in North Central Venezuela},
	    journal = {Bulletin of the Seismological Society of America},
	    number = {?},
	    pages = {?--?},
	    volume = {?},
	    year = {2020}
	}

## 3 Setup

### 3.1 Setup environment (local machine)

WARNING: This repository only works with Python 2.7. 

NOTE: We tried the setup both on Mac and Linux. As the project involves many old libraries (including tensorflow 0.12) the setup may become troublesome (each time we do it we found new problems). Good luck.

In case you don't have pip installed let's install it:

	sudo curl https://bootstrap.pypa.io/get-pip.py | sudo python

In case you don't have virtualenv installed let's install it:

	sudo pip install virtualenv

Let's first create and activate a Python's virtualenv (let's assume you save your Python virtualenvs within MY_VIRTUALENVS folder, e.g. $HOME/virtualenvs):
 
	virtualenv MY_VIRTUALENVS/deepquake
	source MY_VIRTUALENVS/deepquake/bin/activate

Now download the repository from GiHub into your home directory or wherever you prefer: 

	cd
	git clone https://github.com/rtous/deepquake.git
	cd deepquake

INFO: An "ouput" directory will be created after running some of the programs. This directory will not be part of the repository (is listed within .gitignore).

Install all the dependencies listed within requirements.txt:

	xargs -L 1 pip install < requirements.txt

*NOTE: According to the ConvNetQuake repo they used tensorflow 0.11. We tried with 0.12 and it works. However, this version is very old (currently 1.12) and we plan updating at some point.


## 4. Quick start: running the UPC-UCV model 

You can directly test the UPC-UCV model over a couple of example streams (at input/CARABOBO_lite/mseed) running:

	./scripts/step6_eval_over_mseed.sh CARABOBO_lite 50 2 3 models/model14b models/model14b/config_model14b.ini input/CARABOBO_lite/mseed input/CARABOBO_lite/catalog.json output/test

## 5 A full execution cycle (preprocessing -> training -> evaluation)

The following subsections describe the necessary steps to train the model. They operate over an small demo dataset (CARABOBO_lite) to make things faster. At the end it is described how to train the model over the CARABOBO2019 dataset. 

### 5.0 Step 0. Preprocessing 0. Gather all the metadata of a dataset and put it within a .json file.

In this step you will generate the catalog.json file from a source catalog in Nordic format (see [ANNEX 1](#ANNEX 1)). In fact you may skip this as we already provide the catalog.json (both for CARABOBO_lite and CARABOBO2019) but this may be necessary if you are working with a different dataset.

Run the following command (ignore the warnings):

	python step0_preprocess0_metadata.py \
	--input_path input/CARABOBO_lite /sfiles_nordicformat \
	--output_path output/data_prep_CARABOBO_lite/catalog.json

Check the content of the output/data_prep_CARABOBO_lite/catalog.json file. 

Alternatively, you can use the following script:

	./scripts/step0_metadata.sh CARABOBO_lite

### 5.1 Step 1. Preprocessing 1. Splitting the seismograms into small windows.

Now we will split all the .mseed files into small windows of "window_size" seconds (e.g. 50 seconds) and just one station. If the input seismograms include the three components we will obtain three-component windows (even if we plan to just use one, we will specify that later).

Run the following command:

	python step1_preprocess1_get_windows.py \
	--window_size 50 \
	--window_stride 10 \
	--raw_data_dir input/CARABOBO_lite/mseed \
	--catalog_path output/data_prep_CARABOBO_lite/catalog.json \
	--prep_data_dir output/data_prep_CARABOBO_lite/50

Alternatively, you can use the following script:

	./scripts/step1_preprocess1_get_windows.sh CARABOBO_lite 50 10

Check the contents of the "output/data_prep_quickstart/10 directory". You will find:

```
output
    |-data_prep_CARABOBO_lite
        |-50
            |-mseed
            |-mseed_event_windows
            |-mseed_noise
            |-png
            |-png_event_windows
            |-png_noise
```

The only folders that we really need to proceed are "mseed_event_windows" and "mseed_noise". They contain the windows that (according to "data_prep_quickstart/catalog.json") include a P-wave and the windows that not respectivelly. 

The "mseed" folder contains a replica of the input .mseed files but as one-file-per-station. We will use them to perform some optional detection experiments at the end. 

The "png*" folders contain plots but they are now empty because we did not specify the "--plot 1" argument. It is recommended that you generate plots at the beginning, but not later as it takes a lot of time. Retype the command and wait:
```
	python step1_preprocess1_get_windows.py \
	--window_size 50 \
	--window_stride 10 \
	--raw_data_dir input/CARABOBO_lite/mseed \
	--catalog_path output/data_prep_CARABOBO_lite/catalog.json \
	--prep_data_dir output/data_prep_CARABOBO_lite/50
	--plot 1
```

### 5.2 Step 2. Preprocessing 2. Generating tfrecords for positives

Run the following:

	python step2_preprocess2_create_tfrecords_positives.py \
	--window_size 50 \
	--prep_data_dir output/data_prep_CARABOBO_lite/50 \
	--tfrecords_dir output/data_prep_CARABOBO_lite/50/CL2/CO3/tfrecords

It did read the "output/data_prep_CARABOBO_lite/50/mseed_event_windows" folder and did generate the "positives" part of a training and test datasets this way:

```
output
    |-data_prep_quickstart
        |-50
            |-CL2
                |-CO3
                    |-tfrecords
                        |-test
                            |-positive
                                |-positives.tfrecords
                        |-train
                            |-positive
                                |-positives.tfrecords
```
Ths "CL2" and "CO3" subfolders mean "two classes" (event and no event) and "3 components" respectively. You can generate different training/test datasets (e.g. with all the components and more classes if you need location detection) with this tool without the need to do the costly step 1 again. 

### 5.3 Step 3. Preprocessing 3. Generating tfrecords for negatives

Run the following:

	python step3_preprocess3_create_tfrecords_negatives.py \
	--window_size 50 \
	--prep_data_dir output/data_prep_CARABOBO_lite/50 \
	--tfrecords_dir output/data_prep_CARABOBO_lite/50/CL2/CO3/tfrecords

Alternatively, you can use the following script to generate the tfrecords for both, the positives and the negatives:

	./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh CARABOBO_lite 50 2 3

### 5.4 Step 4. Train

Let's do a short training with the UPC-UCV model. We will use a special configuration in file "models/model14b/config_model14b_lite.ini" to limit the number of training steps. Let's run:

	python step4_train.py \
    --config_file_path models/model14b/config_model14b_lite.ini \
	--n_clusters 2 \
	--window_size 50 \
	--tfrecords_dir output/data_prep_CARABOBO_lite/50/CL2/CO3/tfrecords \
	--checkpoint_dir output/data_prep_CARABOBO_lite/50/CL2/CO3/model14b/checkpoints

### 5.5 Step 5. Eval

Let's eval the generated model against the test dataset (20% of the data):

	python step5_eval_over_tfrecords.py \
	--config_file_path models/model14b/config_model14b_lite.ini \
	--n_clusters 2 \
	--window_size 50 \
	--checkpoint_dir output/data_prep_CARABOBO_lite/50/CL2/CO3/model14b/checkpoints \
	--output_dir output/data_prep_CARABOBO_lite/50/CL2/CO3/model14b/eval \
	--tfrecords_dir output/data_prep_CARABOBO_lite/50/CL2/CO3/tfrecords/test

The evaluation will show the results but will also generate a file like this at the root of the output folder:
```
output
    |-eval_20181123111049_1_data_prep_CARABOBO_lite_50_2_3_model14b.json
```
This file contains the results in .json format. When running over a cluster, retrieving these files and processing them with some of the automation utilities provided by the report is critical in order to generate reports, plots and papers.  

Alternatively, you can use the following script to perform both, the training and the evaluation:

	./scripts/step4_and_5_train_and_eval_over_tfrecords.sh CARABOBO_lite 50 2 3 model14b models/model14b/config_model14b_lite.ini

### 5.6 Step 6. Detect over raw data 

While the evaluation step is enough to assess the performance of a model, you may be curious to apply the model to real data.  

	python step6_eval_over_mseed.py \
	--config_file_path models/model14b/config_model14b_lite.ini \
	--n_clusters 2 \
	--window_size 50 \
	--checkpoint_dir output/data_prep_CARABOBO_lite/50/CL2/CO3/model14b/checkpoints \
	--output_dir output/data_prep_CARABOBO_lite/10/CL2/CO3/model14b/eval \
	--catalog_path output/data_prep_CARABOBO_lite/catalog.json \
	--stream_path output/data_prep_CARABOBO_lite/50/mseed

It will try detecting P-waves over all the files within "output/data_prep_CARABOBO_lite/50/mseed". The tool will generate some nice plots within the "output/data_prep_CARABOBO_lite/50/CL2/CO3/model14b/eval" folder. 

Alternatively, you can use the following script:

	./scripts/step6_eval_over_mseed.sh CARABOBO_lite 50 2 3 output/data_prep_CARABOBO_lite/50/CL2/CO3/model14b models/model14b/config_model14b.ini input/CARABOBO_lite/mseed input/CARABOBO_lite/catalog.json output/test 


## 6. Training the model over the CARABOBO2019 dataset

First download the CARABOBO2019 dataset and place it within the "input" directory:

	cd input

	git clone https://github.com/rtous/CARABOBO2019.git

Then perform the steps from the previous section replacing "CARABOBO_lite" with "CARABOBO2019".


## ANNEX 1. Working over your own dataset 

The different tools work over a given DATASET. The input files of a DATASET must be located within the "input" folder (from the root of the repo) and must have the following structure:

```
input
	|-DATASET
		|-mseed
		|-sfiles_nordicformat
```

The different tools have been desgned to work over data (both the files with the waveforms and the metadata) coming from (https://www.geosig.com/files/GS_SEISAN_9_0_1.pdf)[SEISAN], a seismic analysis software suite. 

### .mseed files

Requirements of the "mseed" folder of a dataset:

* The "mseed" folder contains seismograms in mseed format. All the files MUST have the .mseed extension (you can use the utility "util_add_mseed_extension.py" if you need to fix a new dataset. 
* All the seismograms should be sampled at 100Hz. 
* The seismograms can have the three components or just one. The seismograms can have waves from multiple stations or for one station. The code is ready to deal with the different variants automatically. 
* The code will not work if each components of a seismogram is located in a different file. You can use "util_join_components.py" to fix that.

Let's start by plotting different variants of valid input .mseed files:

	python util_plot_mseed.py --stream_path input/CARABOBO_lite/mseed/2018-04-24-0355-00M.BENV__001_HH.mseed --output_dir output/plots

### sfiles metadata

While the .mseed files include some metadata (station code and times basically) the expert-generated metadata (the groundtruth) about the events (origin, magnitude, P-wave arrival at each station) is located in SEISAN's s-files (in Nordic format). If you need to do a pre-pre-processing (dealing with new, raw data) you need to consider the following:

* The sfile filename MUST have the format 01-1259-00M.S201804 (for 01/04/2018 at 12:59). 
* Internally an sfile should have (at least) the kind of structure that you will find in the sfiles in the CARABOBO_lite dataset.
* At the end of each line of the stations P-wave arrival section there must be a white space (tricky).  

You can inspect the content of an S-File metadata with the utility "util_inspect_sfile.py" this way: 
	
	python util_inspect_sfile.py --stream_path input/CARABOBO_lite/sfiles_nordicformat/01-0000-00M.S190001 --output_path output/CARABOBO_lite/metadata.xml

*NOTE: Don't worry about the sfiles complexity, during the preprocessing we will convert all the messy sfiles of each dataset into a single and simple .json file with our own metadata format.

*NOTE: SEISAN programs produce output files with the extension .out preceded by the name of the program. The original groundtruth metadata used here were obtained with the SEISAN's SELECT tool, which generates a file named select.out. From this file, we extracted the desired Nordic format fragments with:

	grep -e "2019 \|2019-\|BAUV HZ\|BENV HZ\|MAPV HZ\|TACV HZ\|^[[:space:]]*$" select.out > arrival_times_v2.txt

However, in order to have a single file for each earthquake we need to split the file this way:

	python util_bigsfile2sfiles.py --bigsfile_path input/CARABOBO_lite --output_path input/CARABOBO_lite/sfiles_nordicformat


## ANNEX 2. Tools for running experiments in a cluster and processing the results automatically 

Real experiments are usually submitted to a computing cluster. The following sections explain some utilities to facilitate this task.  

### Scripts

The "scripts" folder includes some bash scripts to make things easier. For instance, if you would like to perform the training and evaluation with the improved model (model 2) you could do it with simple running:

	./scripts/step4_and_5_train_and_eval_over_tfrecords.sh quickstart 10 2 1 model2 experiments/config_test_model2.ini


### The "experiments" folder

Within the "experiments" folders you will find the configuration files (and some special configuration files such as the ones used for location detection) used in the experiments that we have already done. In this folder you will also find .txt files with the qsub commands that we submitted to the Arvei cluster. In order to launch experiments on Arvei read this:

* [Launching experiments on Arvei](arvei/arvei_user_guide.md)

* [Some comments about using Arvei](arvei/arvei_notes.md)


### Processing the results

The repo includes some utilities to automate the processing of results. The script:

	bring_results_from_server.sh

Performs an scp of all result .json files into the local experiments/results folder. 

The tool "results.py" includes utilities to gather all results and generate plots, etc. You can use it as a module or run it (it has a main that generate some plots, but you may need to change that).


## ANNEX 3. Tools parametrization

* By default tools read parameters from the config_default.ini file. 
* Some parameters can be (some times need to be) overriden with command line arguments. This is the recommended way of overriding the defaults.
* You can also override a subset of parameters specifying your own config file with the --config_file_path argument. This may be convenient when many parameters need to be overriden the same way for a set of experiments (e.g. the configuration of a new model with different layers, kernel size, etc.) 

WARNING: When specifying boolean command line arguments we will use 0 or 1 because of a limitation of the argparse module. When specifying boolean parameters in the .ini config files we will use "true" and "false", with all letters in lower-case.


## ANNEX 4. Troubleshooting

	"tensorflow.python.framework.errors_impl.InternalError: Unable to get element from the feed as bytes." -> cannot find the checkpoint file

	"ValueError: string_input_producer requires a non-null input tensor" -> the training directories should be "positive" and "negative" without "s" at the end.

	"InvalidArgumentError (see above for traceback): Name: <unknown>, Feature: end_time is required but could not be found." -> Using old positives/negatives (downloaded), generate new ones

	"_tkinter.TclError: no display name and no $DISPLAY environment variable" -> Add this code to the start of your script (before importing pyplot) and try again:
			import matplotlib
			matplotlib.use('Agg')

	"tf.errors.OutOfRangeError" -> a parameter from config .ini is not being passed correctly. Harcode it in config.py instead.


