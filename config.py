import configparser

class Config(object):
  def __init__(self, config_file_path):
    config = configparser.ConfigParser()
    config.read(config_file_path)
    
    self.DEBUG = config.getboolean('main', 'DEBUG')
    self.SAMPLING_RATE = config.getfloat('main', 'SAMPLING_RATE')
    self.WINDOW_SIZE = config.getint('main', 'WINDOW_SIZE')
    self.PWAVE_WINDOW = config.getint('main', 'PWAVE_WINDOW')
    self.WINDOW_STEP_NEGATIVES = config.getint('main', 'WINDOW_STEP_NEGATIVES') #The step between the start times of two successive windows in seconds.
    self.WINDOW_AVOID_NEGATIVES = config.getint('main', 'WINDOW_AVOID_NEGATIVES')
    self.INPUT_STREAM_DIR = config.get('main', 'INPUT_STREAM_DIR')
    self.INPUT_METADATA_DIR = config.get('main', 'INPUT_METADATA_DIR')

    self.DATASET_BASE_DIR = config.get('main', 'DATASET_BASE_DIR')
    self.MSEED_DIR = config.get('main', 'MSEED_DIR')
    #self.OUTPUT_MSEED_DIR = os.path.join(self.DATASET_BASE_DIR, self.MSEED_DIR)
    self.MSEED_EVENT_DIR = config.get('main', 'MSEED_EVENT_DIR')
    #self.OUTPUT_MSEED_EVENT_DIR = os.path.join(self.DATASET_BASE_DIR, self.MSEED_EVENT_DIR)
    self.MSEED_NOISE_DIR = config.get('main', 'MSEED_NOISE_DIR')
    #self.OUTPUT_MSEED_NOISE_DIR = os.path.join(self.DATASET_BASE_DIR, self.MSEED_NOISE_DIR)
    self.PNG_DIR = config.get('main', 'PNG_DIR')
    #self.OUTPUT_PNG_DIR = os.path.join(self.DATASET_BASE_DIR, self.PNG_DIR)
    self.PNG_EVENT_DIR = config.get('main', 'PNG_EVENT_DIR')
    #self.OUTPUT_PNG_EVENT_DIR = os.path.join(self.DATASET_BASE_DIR, self.PNG_EVENT_DIR)
    self.PNG_NOISE_DIR = config.get('main', 'PNG_NOISE_DIR')
    #self.OUTPUT_PNG_NOISE_DIR = os.path.join(self.DATASET_BASE_DIR, self.PNG_NOISE_DIR)
    
    self.OUTPUT_TFRECORDS_DIR_POSITIVES = config.get('main', 'OUTPUT_TFRECORDS_DIR_POSITIVES')
    self.OUTPUT_TFRECORDS_DIR_NEGATIVES = config.get('main', 'OUTPUT_TFRECORDS_DIR_NEGATIVES')
    self.CHECKPOINT_DIR = config.get('main', 'CHECKPOINT_DIR')
    #self.DATASET = config.get('main', 'DATASET')

    #train
    self.learning_rate = config.getfloat('main', 'learning_rate')
    self.batch_size = config.getint('main', 'batch_size')
    self.win_size = int((self.WINDOW_SIZE * self.SAMPLING_RATE) + 1)
    self.n_traces = config.getint('main', 'n_traces')
    self.display_step = config.getint('main', 'display_step')
    self.n_threads = config.getint('main', 'n_threads')
    #self.n_epochs = config.getint('main', 'n_epochs')
    self.n_epochs = None
    #self.regularization = config.getfloat('main', 'regularization')s
    self.regularization = 1e-3
    self.n_clusters = config.getint('main', 'n_clusters')
    self.model = config.get('main', 'model')
    self.resume = config.getboolean('main', 'resume')
    self.profiling = config.getboolean('main', 'profiling')
    self.add = config.getint('main', 'add')
    self.checkpoint_step = config.getint('main', 'checkpoint_step')
    self.max_checkpoint_step = config.getint('main', 'max_checkpoint_step')
    
    #eval
    self.OUTPUT_EVAL_BASE_DIR = config.get('main', 'OUTPUT_EVAL_BASE_DIR')

    #predict
    self.WINDOW_STEP_PREDICT = config.getint('main', 'WINDOW_STEP_PREDICT')
    self.OUTPUT_PREDICT_BASE_DIR = config.get('main', 'OUTPUT_PREDICT_BASE_DIR')
    self.save_sac = config.getboolean('main', 'save_sac')