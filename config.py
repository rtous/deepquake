import configparser
import argparse

class Config(object):
  def __init__(self, config_file_path):
    config = configparser.ConfigParser()
    config.read(config_file_path)
    
    self.debug = config.getboolean('main', 'debug')
    self.sampling_rate = config.getfloat('main', 'sampling_rate')
    self.window_size = config.getint('main', 'window_size')
    self.pwave_window = config.getint('main', 'pwave_window')
    self.window_step_negatives = config.getint('main', 'window_step_negatives') #the step between the start times of two successive windows in seconds.
    self.window_avoid_negatives = config.getint('main', 'window_avoid_negatives')
    #self.input_stream_dir = config.get('main', 'input_stream_dir')
    #self.input_metadata_dir = config.get('main', 'input_metadata_dir')
    #self.dataset_base_dir = config.get('main', 'dataset_base_dir')
    

    self.n_traces = 0
    self.component_Z = config.getboolean('main', 'component_Z')
    if self.component_Z:
        self.n_traces = self.n_traces + 1    
    self.component_N = config.getboolean('main', 'component_N')
    if self.component_N:
        self.n_traces = self.n_traces + 1
    self.component_E = config.getboolean('main', 'component_E')
    if self.component_E:
        self.n_traces = self.n_traces + 1
    #self.n_traces = config.getint('main', 'n_traces')
    if self.n_traces == 0:
        print ("[config] \033[91m ERROR!!\033[0m 0 number of components selected. You need to specify at least component_Z = true, component_N = true or component_E = true")
        sys.exit(0)

    self.mseed_dir = config.get('main', 'mseed_dir')
    self.mseed_event_dir = config.get('main', 'mseed_event_dir')
    self.mseed_noise_dir = config.get('main', 'mseed_noise_dir')
    self.png_dir = config.get('main', 'png_dir')
    self.png_event_dir = config.get('main', 'png_event_dir')
    self.png_noise_dir = config.get('main', 'png_noise_dir')
    self.output_tfrecords_dir_positives = config.get('main', 'output_tfrecords_dir_positives')
    self.output_tfrecords_dir_negatives = config.get('main', 'output_tfrecords_dir_negatives')
    #self.checkpoint_dir = config.get('main', 'checkpoint_dir')

    #train
    self.learning_rate = config.getfloat('main', 'learning_rate')
    self.batch_size = config.getint('main', 'batch_size')
    self.win_size = int((self.window_size * self.sampling_rate) + 1)
    
    self.display_step = config.getint('main', 'display_step')
    self.n_threads = config.getint('main', 'n_threads')
    self.n_epochs = None
    self.regularization = 1e-3
    self.n_clusters = config.getint('main', 'n_clusters')
    self.model = config.get('main', 'model')
    self.resume = config.getboolean('main', 'resume')
    self.profiling = config.getboolean('main', 'profiling')
    self.add = config.getint('main', 'add')
    self.checkpoint_step = config.getint('main', 'checkpoint_step')
    self.max_checkpoint_step = config.getint('main', 'max_checkpoint_step')
    
    #eval
    self.window_step_predict = config.getint('main', 'window_step_predict')
    #self.output_predict_base_dir = config.get('main', 'output_predict_base_dir')
    self.save_sac = config.getboolean('main', 'save_sac')