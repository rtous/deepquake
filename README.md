# DeepQuake

## 1 Setup

### 1.1 Setup environment (local machine)

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

### 1.2 Prepare the input data (pre-pre-processing)

*NOTE: The raw data used here (both the files with the waveforms and the metadata) comes from comes from (https://www.geosig.com/files/GS_SEISAN_9_0_1.pdf)[SEISAN], a seismic analysis software suite.

We work with multiple datasets (currently "datos1", "datos2" and "datos3"). Each dataset must be located within the "input" folder (from the root of the repo) and must have the following structure:

```
input
	|-datos1
		|-mseed
		|-sfiles_nordicformat
```

We call "pre-pre-processing" the process of adapting the raw data provided by the experts into this structure and the proper file formats. The datasets that you will find in the repo are already pre-pre-processed. However, if you need to include a new dataset you should consider the requirements described in the following subsections.

NOTE: Currently the input data is part of the repository for convenience. If these data would become too big we would remove them.

### 1.2.1 .mseed files

Requirements of the "mseed" folder of a dataset:

* The "mseed" folder contains seismograms in mseed format. All the files MUST have the .mseed extension (you can use the utility "util_add_mseed_extension.py" if you need to fix a new dataset. 
* All the seismograms should be sampled at 100Hz. 
* The seismograms can be have the three components (like "datos1") or just one (like "datos2" and "datos3). The seismograms can have waves from multiple stations (like "datos1") or for one station (like "datos2" and "datos3"). The code is ready to deal with the different variants automatically. 
* The code will not work if each components of a seismogram is located in a different file. You can use "util_join_components.py" to fix that.

Let's start by plotting different variants of valid input .mseed files:

	python util_plot_mseed.py --stream_path input/datos3/mseed/2018-03-03-1929-00M.BENV__001_HH_1Z.mseed --output_dir output/plots
	python util_plot_mseed.py --stream_path input/datos1/mseed/2015-01-10-0517-00S.mseed --output_dir output/quickstart

### 1.2.2 sfiles metadata

While the .mseed files include some metadata (station code and times basically) the expert-generated metadata (the groundtruth) about the events (origin, magnitude, P-wave arrival at each station) is located in SEISAN's s-files (in Nordic format). If you need to do a pre-pre-processing (dealing with new, raw data) you need to consider the following:

* The sfile filename MUST have the format 01-1259-00M.S201804 (for 01/04/2018 at 12:59). 
* Internally an sfile should have (at least) the kind of structure that you will find in the sfiles in the "datos3" dataset.
* At the end of each line of the stations P-wave arrival section there must be a white space (tricky).  

Pre-pre-processing of raw metadata may be difficult as each new dataset comes in a different variant. We created many utilities to deal with that (e.g. "util_datos3_bigsfile2sfiles.py" and "util_mseed_name2sfile_name.py"). Hope you don't need them.

You can inspect the content of an S-File metadata with the utility "util_inspect_sfile.py" this way: 
	
	python util_inspect_sfile.py --stream_path input/datos3/sfiles_nordicformat/01-0000-00M.S200601 --output_path output/quickstart/metadata.xml

*NOTE: Don't worry about the sfiles complexity, during the preprocessing we will convert all the messy sfiles of each dataset into a single and simple .json file with our own metadata format.

*NOTE: SEISAN programs produce output files with the extension .out preceded by the name of the program. The original groundtruth metadata used here were obtained with the SEISAN's SELECT tool, which generates a file named select.out. From this file, we extracted the desired Nordic format fragments with:

	grep -e "2019 \|2019-\|BAUV HZ\|BENV HZ\|MAPV HZ\|TACV HZ\|^[[:space:]]*$" select.out > arrival_times_v2.txt

## 2 A full execution cycle (preprocessing -> training -> evaluation)

### Note about the tools parametrization (you may skip this if doing a quick start)

* By default tools read parameters from the config_default.ini file. 
* Some parameters can be (some times need to be) overriden with command line arguments. This is the recommended way of overriding the defaults.
* You can also override a subset of parameters specifying your own config file with the --config_file_path argument. This may be convenient when many parameters need to be overriden the same way for a set of experiments (e.g. the configuration of a new model with different layers, kernel size, etc.) 

WARNING: When specifying boolean command line arguments we will use 0 or 1 because of a limitation of the argparse module. When specifying boolean parameters in the .ini config files we will use "true" and "false", with all letters in lower-case.


### 2.0 Step 0. Preprocessing 0. Gather all the metadata of a dataset and put it within a .json file.

Run the following command (ignore the warnings):

	python step0_preprocess0_metadata.py \
	--input_path input/datos1/sfiles_nordicformat \
	--output_path output/data_prep_quickstart/catalog.json

Check the content of the output/data_prep_quickstart/catalog.json file. 

### 2.1 Step 1. Preprocessing 1. Splitting the seismograms into small windows.

Now we will split all the .mseed files into small windows of "window_size" seconds (e.g. 10 seconds) and just one station. If the input seismograms include the three components we will obtain three-component windows (even if we plan to just use one, we will specify that later).

Run the following command:

	python step1_preprocess1_get_windows.py \
	--debug 1 \
	--window_size 10 \
	--window_stride 10 \
	--raw_data_dir input/datos1/mseed \
	--catalog_path output/data_prep_quickstart/catalog.json \
	--prep_data_dir output/data_prep_quickstart/10 \
	--station CRUV

We have included a special argument (--station CRUV) that limits the processing only to the CRUV station to make things faster. You will not use this argument in real experiments.

Check the contents of the "output/data_prep_quickstart/10 directory". You will find:

```
output
    |-data_prep_quickstart
        |-10
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
	--debug 1 \
	--window_size 10 \
	--window_stride 10 \
	--raw_data_dir input/datos1/mseed \
	--catalog_path output/data_prep_quickstart/catalog.json \
	--prep_data_dir output/data_prep_quickstart/10 \
	--station CRUV \
	--plot 1
```

### 2.2 Step 2. Preprocessing 2. Generating tfrecords for positives

Run the following:

	python step2_preprocess2_create_tfrecords_positives.py \
	--window_size 10 \
	--component_N 0 \
	--component_E 0 \
	--prep_data_dir output/data_prep_quickstart/10 \
	--tfrecords_dir output/data_prep_quickstart/10/CL2/CO1/tfrecords

It did read the "output/data_prep_quickstart/10/mseed_event_windows" folder and did generate the "positives" part of a training and test datasets this way:

```
output
    |-data_prep_quickstart
        |-10
            |-CL2
                |-CO1
                    |-tfrecords
                        |-test
                            |-positive
                                |-positives.tfrecords
                        |-train
                            |-positive
                                |-positives.tfrecords
```
Ths "CL2" and "CO1" subfolders mean "two classes" (event and no event) and "1 component" (only Z) respectively. You can generate different training/test datasets (e.g. with all the components and more classes if you need location detection) with this tool without the need to do the costly step 1 again. 

### 2.3 Step 3. Preprocessing 3. Generating tfrecords for negatives

Run the following:

	python step3_preprocess3_create_tfrecords_negatives.py \
	--window_size 10 \
	--component_N 0 \
	--component_E 0 \
	--prep_data_dir output/data_prep_quickstart/10 \
	--tfrecords_dir output/data_prep_quickstart/10/CL2/CO1/tfrecords


### 2.4 Step 4. Train

Let's do a short training with the ConvNetQuake original model (model 1). We will use a special configuration in file "experiments/config_test.ini" to limit the number of training steps. Let's run:

	python step4_train.py \
    --config_file_path experiments/config_test_model1.ini \
	--component_N 0 \
	--component_E 0 \
	--n_clusters 2 \
	--window_size 10 \
	--tfrecords_dir output/data_prep_quickstart/10/CL2/CO1/tfrecords \
	--checkpoint_dir output/data_prep_quickstart/10/CL2/CO1/model1/checkpoints

### 2.5 Step 5. Eval

Let's eval the generated model against the test dataset (20% of the data):

	python step5_eval_over_tfrecords.py \
	--config_file_path experiments/config_test_model1.ini \
	--component_N 0 \
	--component_E 0 \
	--n_clusters 2 \
	--window_size 10 \
	--checkpoint_dir output/data_prep_quickstart/10/CL2/CO1/model1/checkpoints \
	--output_dir output/data_prep_quickstart/10/CL2/CO1/model1/eval \
	--tfrecords_dir output/data_prep_quickstart/10/CL2/CO1/tfrecords/test

The evaluation will show the results but will also generate a file like this at the root of the output folder:
```
output
    |-eval_20181123111049_1_data_prep_quickstart_10_2_1_ConvNetQuake.json
```
This file contains the results in .json format. When running over a cluster, retrieving these files and processing them with some of the automation utilities provided by the report is critical in order to generate reports, plots and papers.  


### 2.6 Step 6. Detect over raw data (OPTIONAL)

While the evaluation step is enough to assess the performance of a model, you may be curious to apply the model to real data.  

	python step6_eval_over_mseed.py \
	--config_file_path experiments/config_test_model1.ini \
	--component_N 0 \
	--component_E 0 \
	--n_clusters 2 \
	--window_size 10 \
	--checkpoint_dir output/data_prep_quickstart/10/CL2/CO1/model1/checkpoints \
	--output_dir output/data_prep_quickstart/10/CL2/CO1/model1/eval \
	--catalog_path output/data_prep_quickstart/catalog.json \
	--stream_path output/data_prep_quickstart/10/mseed

It will try detecting P-waves over all the files within "output/data_prep_quickstart/10/mseed". The tool will generate some nice plots within the "output/data_prep_quickstart/10/CL2/CO1/model1/eval" folder. 


## 3 Tools for running experiments in a cluster and processing the results automatically 

Real experiments are usually submitted to a computing cluster. The following sections explain some utilities to facilitate this task.  

### 3.1 Scripts

The "scripts" folder includes some bash scripts to make things easier. For instance, if you would like to perform the training and evaluation with the improved model (model 2) you could do it with simple running:

	./scripts/step4_and_5_train_and_eval_over_tfrecords.sh quickstart 10 2 1 model2 experiments/config_test_model2.ini


### 3.2 The "experiments" folder

Within the "experiments" folders you will find the configuration files (and some special configuration files such as the ones used for location detection) used in the experiments that we have already done. In this folder you will also find .txt files with the qsub commands that we submitted to the Arvei cluster. In order to launch experiments on Arvei read this:

* [Launching experiments on Arvei](arvei/arvei_user_guide.md)

* [Some comments about using Arvei](arvei/arvei_notes.md)


### 3.3 Processing the results

The repo includes some utilities to automate the processing of results. The script:

	bring_results_from_server.sh

Performs an scp of all result .json files into the local experiments/results folder. 

The tool "results.py" includes utilities to gather all results and generate plots, etc. You can use it as a module or run it (it has a main that generate some plots, but you may need to change that).


## 4 Troubleshooting

	"tensorflow.python.framework.errors_impl.InternalError: Unable to get element from the feed as bytes." -> cannot find the checkpoint file

	"ValueError: string_input_producer requires a non-null input tensor" -> the training directories should be "positive" and "negative" without "s" at the end.

	"InvalidArgumentError (see above for traceback): Name: <unknown>, Feature: end_time is required but could not be found." -> Using old positives/negatives (downloaded), generate new ones

	"_tkinter.TclError: no display name and no $DISPLAY environment variable" -> Add this code to the start of your script (before importing pyplot) and try again:
			import matplotlib
			matplotlib.use('Agg')

	"tf.errors.OutOfRangeError" -> a parameter from config .ini is not being passed correctly. Harcode it in config.py instead.


