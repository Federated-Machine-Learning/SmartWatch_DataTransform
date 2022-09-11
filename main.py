"""
Started Creating on Sun Sept 11 23:48:01 2022

@author: Devansh Sehgal and Aaditya Kumra
"""

import os
import pickle
import numpy as np

class DataManager:
  # Path to the WESAD dataset
  ROOT_PATH = '' # TODO
  #ROOT_PATH = r'C:\WESAD'
  
  # pickle file extension for importing
  FILE_EXT = '.pkl'

  # Directory in project structure where model files are stored
  MODELS_DIR = '' # TODO
  
  # IDs of the subjects
  SUBJECTS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    
  # Label values defined in the WESAD readme
  BASELINE = 1
  STRESS = 2
    
  FEATURE_KEYS =     ['max',  'min', 'mean', 'range', 'std']
  FEATURE_ACC_KEYS = ['maxx', 'maxy', 'maxz', 'mean', 'std']

  # Keys for measurements collected by the RespiBAN on the chest
  # minus the ones we don't want
  RAW_SENSOR_VALUES = ['ACC', 'ECG','BVP']
  FEATURES = {'a_mean': [], 'a_std': [], 'a_maxx': [], 'a_maxy': [], 'a_maxz': [],\
              'e_max': [],  'e_min': [], 'e_mean': [], 'e_range': [], 'e_std': [],\
              'b_max': [],  'b_min': [], 'b_mean': [], 'b_range': [], 'b_std': [] }
  STRESS_FEATURES = {'a_mean': [], 'a_std': [], 'a_maxx': [], 'a_maxy': [], 'a_maxz': [],\
              'e_max': [],  'e_min': [], 'e_mean': [], 'e_range': [], 'e_std': [],\
              'b_max': [],  'b_min': [], 'b_mean': [], 'b_range': [], 'b_std': [] }

  # Dictionaries to store the two sets of data
  BASELINE_DATA = []
  STRESS_DATA = []

  # the file name for the last created model
  last_saved=''

  def __init__(self, ignore_additional_signals=True):
    pass

  def get_subject_path(self, subject):
    """ 
    Parameters:
    subject (int): id of the subject
    
    Returns:
    str: path to the pickle file for the given subject number
         iff the path exists 
    """
    
    # subjects path looks like data_set + '<subject>/<subject>.pkl'
    path = os.path.join(DataManager.ROOT_PATH, 'S'+ str(subject), 'S' + str(subject) + DataManager.FILE_EXT)
    print('Loading data for S'+ str(subject))
    #print('Path=' + path)
    if os.path.isfile(path):
        return path
    else:
        print(path)
        raise Exception('Invalid subject: ' + str(subject))

  def load(self, subject):
    """ 
    Loads and saves the data from the pkl file for the provided subject
    
    Parameters:
    subject (int): id of the subject
    
    Returns: Baseline and stress data
    dict: {{'EDA': [###, ..], ..}, 
           {'EDA': [###, ..], ..} }
    """
   
    # change the encoding because the data appears to have been
    # pickled with py2 and we are in py3
    with open(self.get_subject_path(subject), 'rb') as file:
        data = pickle.load(file, encoding='latin1')
        return self.extract_and_reform(data, subject)

  def load_all(self, subjects=SUBJECTS):
    """ 
    Parameters:
    subjects (list): subject ids to be loaded
    
    Returns:
    """
    for subject in subjects:
        self.load(subject)

  def extract_and_reform(self, data, subject):
    """ 
    Extracts and shapes the data from the pkl file
    for the provided subject.
    
    Parameters:
    data (dict): as loaded from the pickle file
    
    Returns: Baseline and stress data
    dict: {{'EDA': [###, ..], ..}, 
           {'EDA': [###, ..], ..} }
    """