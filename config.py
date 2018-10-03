import configparser
import argparse

class Config(object):
    def __init__(self, config_file_path):
        self.setValues("config_default.ini", True)
        self.setValues(config_file_path, False)

    def setValues(self, config_file_path, required):
        config = configparser.ConfigParser()
        config.read(config_file_path)   
        self.getboolean('debug', required, config)
        self.getint('sampling_rate', required, config)
        self.getint('window_size', required, config)
        self.getint('pwave_window', required, config)
        self.getint('window_step_negatives', required, config)
        self.getint('window_avoid_negatives', required, config)
        self.n_traces = 0
        self.getboolean('component_Z', required, config)
        if self.component_Z:
            self.n_traces = self.n_traces + 1 
        self.getboolean('component_N', required, config)
        if self.component_N:
            self.n_traces = self.n_traces + 1
        self.getboolean('component_E', required, config)
        if self.component_E:
            self.n_traces = self.n_traces + 1
        if self.n_traces == 0:
            print ("[config] \033[91m ERROR!!\033[0m 0 number of components selected. You need to specify at least component_Z = true, component_N = true or component_E = true")
            sys.exit(0)
        self.getfloat('mean_velocity', required, config)
        self.get('mseed_dir', required, config)
        self.get('mseed_event_dir', required, config)
        self.get('mseed_noise_dir', required, config)
        self.get('png_dir', required, config)
        self.get('png_event_dir', required, config)
        self.get('png_noise_dir', required, config)
        self.get('output_tfrecords_dir_positives', required, config)
        self.get('output_tfrecords_dir_negatives', required, config)
        self.getfloat('learning_rate', required, config)
        self.getint('batch_size', required, config)
        self.win_size = int((self.window_size * self.sampling_rate) + 1)
        self.getint('display_step', required, config)
        self.getint('n_threads', required, config)
        self.n_epochs = None
        self.regularization = 1e-3
        self.getint('n_clusters', required, config)
        self.get('model', required, config)
        self.getboolean('resume', required, config)
        self.getboolean('profiling', required, config)
        self.getint('add', required, config)
        self.getint('checkpoint_step', required, config)
        self.getint('max_checkpoint_step', required, config)
        self.getint('window_step_predict', required, config)
        self.getboolean('save_sac', required, config)

    def getboolean(self, attribute, required, config):
        if config.has_option('main', attribute):
            setattr(self, attribute, config.getboolean('main', attribute))
        elif required:
            print("ERROR: Attribute "+attribute+" not found in default config file.")
            sys.exit(0)

    def getint(self, attribute, required, config):
        if config.has_option('main', attribute):
            setattr(self, attribute, config.getint('main', attribute))
        elif required:
            print("ERROR: Attribute "+attribute+" not found in default config file.")
            sys.exit(0)

    def getfloat(self, attribute, required, config):
        if config.has_option('main', attribute):
            setattr(self, attribute, config.getfloat('main', attribute))
        elif required:
            print("ERROR: Attribute "+attribute+" not found in default config file.")
            sys.exit(0)

    def get(self, attribute, required, config):
        if config.has_option('main', attribute):
            setattr(self, attribute, config.get('main', attribute))
        elif required:
            print("ERROR: Attribute "+attribute+" not found in default config file.")
            sys.exit(0)