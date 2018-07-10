class Config(object):
  def __init__(self, data_dir):
    self.WINDOW_SIZE = 50
    self.WINDOW_STEP_NEGATIVES = 10 #The step between the start times of two successive windows in seconds.
    self.WINDOW_AVOID_NEGATIVES = 200
    self.INPUT_STREAM_DIR = data_dir+"/"+"input/funvisis/mseed"
    self.INPUT_METADATA_DIR = data_dir+"/"+"input/funvisis/sfiles_nordicformat"
    self.OUTPUT_MSEED_DIR = data_dir+"/"+"output/funvisis2oklahoma/mseed"
    self.OUTPUT_MSEED_EVENT_DIR = data_dir+"/"+"output/funvisis2oklahoma/mseed_10s"
    self.OUTPUT_MSEED_NOISE_DIR = data_dir+"/"+"output/funvisis2oklahoma/mseed_noise"
    self.OUTPUT_PNG_DIR = data_dir+"/"+"output/funvisis2oklahoma/png"
    self.OUTPUT_PNG_EVENT_DIR = data_dir+"/"+"output/funvisis2oklahoma/png_10s"
    self.OUTPUT_PNG_NOISE_DIR = data_dir+"/"+"output/funvisis2oklahoma/png_noise"
    self.OUTPUT_TFRECORDS_DIR_POSITIVES = data_dir+"/"+"output/positive"
    self.OUTPUT_TFRECORDS_DIR_NEGATIVES = data_dir+"/"+"output/negative"
    self.CHECKPOINT_DIR = data_dir+"/"+"output/checkpoints"
    self.DATASET = data_dir+"/"+"output"

    #train
    self.learning_rate = 0.001
    self.batch_size = 128
    #self.win_size = 1001
    self.win_size = (self.WINDOW_SIZE * 100) + 1
    self.n_traces = 3
    self.display_step = 50
    self.n_threads = 2
    self.n_epochs = None
    self.regularization = 1e-3
    self.n_clusters = None
    # Number of epochs, None is infinite
    n_epochs = None

    #eval
    self.WINDOW_STEP_PREDICT = 51 #The step between the start times of two successive windows in seconds.
    self.OUTPUT_EVAL_BASE_DIR = data_dir+"/"+"output/eval"

    #predict
    self.WINDOW_STEP_PREDICT = 51
    self.OUTPUT_PREDICT_BASE_DIR = data_dir+"/"+"output/predict"