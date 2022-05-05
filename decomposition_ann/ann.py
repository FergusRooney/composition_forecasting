import tensorflow as tf
import numpy as np

from decomposition_ann.files import read_data, read_small_data, lstm_data
from decomposition_ann.models_funcs2 import make_prediction, write_predictions

from sklearn.model_selection import train_test_split


class ANN():
    
    #creator function:
    #   ann_type ->       string
    #   layers ->         array of ints, number of nodes in each layer
    #   files_to_train -> array of strings
    #   files_to_test ->  array of strings 
    def __init__(self, ann_type, layers, files_to_train, files_to_test, file_to_write, steps = None):
        
        self.model_functions = {"FFN" : tf.keras.layers.Dense,
                                "LSTM": tf.keras.layers.LSTM}
        self.type = ann_type
        self.layers = layers
        self.files_to_train = files_to_train
        self.files_to_test = files_to_test
        self.steps = steps
        self.file_to_write = file_to_write
        
        evidence, labels = self.get_data()
            
        if ann_type == "FFN":
            self.input_type = (2,)
            self.steps = None
            self.x_training, self.x_testing, self.y_training, self.y_testing = train_test_split(
                evidence, labels, test_size=0.2   
                )
            
        elif ann_type == "LSTM":
            self.input_type = (steps, 2)
            evidence, labels = lstm_data(raw_evidence = evidence, raw_labels = labels, seq_lenght = steps)
            
            self.x_training, self.x_testing, self.y_training, self.y_testing = train_test_split(
                evidence, labels, test_size=0.2   
                )
            
            self.x_testing = self.x_testing.reshape((self.x_testing.shape[0], self.x_testing.shape[1], 2))
            self.x_training = self.x_training.reshape((self.x_training.shape[0], self.x_training.shape[1], 2))
            
        self.model = None
        #self.model = self.create_ann()
        
            
        
    #gets data for FFN
    def get_data(self):
        print("read in progress")
        evidence, labels = read_data(self.files_to_train)
        print("data read done")
        return evidence, labels
       
    #creates, trains, evaluates and saves an ann
    def create_ann(self):
           	
        # Create a neural network
        model = tf.keras.models.Sequential()

        #first/input layer
        if self.type == "FFN":
            model.add(self.model_functions[self.type](self.layers[0], input_shape= self.input_type, activation="relu"))
            model.add(tf.keras.layers.Dropout(0.4))
            #adding hidden layers
            for layer in self.layers[1:]:
                model.add(self.model_functions[self.type](layer, activation="elu"))
                model.add(tf.keras.layers.Dropout(0.4))
        
        else:
            model.add(self.model_functions[self.type](self.layers[0], input_shape= self.input_type, activation="relu", return_sequences= True))
            model.add(tf.keras.layers.Dropout(0.4))
            #adding hidden layers
            for layer in self.layers[1:-1]:
                model.add(self.model_functions[self.type](layer, activation="elu", return_sequences= True))
                model.add(tf.keras.layers.Dropout(0.4))
            model.add(self.model_functions[self.type](self.layers[-1], activation="elu"))
            model.add(tf.keras.layers.Dropout(0.4))
        #last/output layer    
        model.add(tf.keras.layers.Dense(6, activation="sigmoid"))
        
        # Train neural network
        model.compile(
            optimizer="adam",
            loss= "mse",
            metrics= ["mse"]
        )
        
        model.fit(self.x_training, self.y_training, epochs=20)
        # Evaluate how well model performs
        model.evaluate(self.x_testing,  self.y_testing, verbose=2)

        model.save(f"decomposition_ann/test_model{self.type}")
        print("model saved")
        model.summary()
        self.model = model
        #return model
        
        
    def load_model(self, model_to_load):
        self.model = tf.keras.models.load_model(model_to_load)
      
    #makes one prediction:
    #   element_to_predict -> int
    def make_one_prediction(self, element_to_predict):
        prediction = make_prediction(last_data= element_to_predict, model = self.model, files_to_read = self.files_to_test, steps_num = self.steps)      

    #makes n predictions and writes them to csv file (n= number_of_predictions):
    #   first_prediction ->      int
    #   number_of_predictions -> int
    #   file_to_write ->         string
    def write_predictions_to_csv(self, first_prediction, number_of_predictions):
        write_predictions(first_pred = first_prediction, num_pred = number_of_predictions, model= self.model, files_to_read = self.files_to_test, file_to_write= self.file_to_write, steps= self.steps)