#Bartosz code


import csv
import numpy as np

def read_data(files):
    
    total_data = []
    for file in files:
        
        with open(f"{file}.csv") as f:
            reader = csv.reader(f)
            #next(reader)
            data = []
            for row in reader:
                data.append(float(row[0]) if len(row)==1 else [float(cell) for cell in row])
                
            total_data.append(data)
            
    total_P, total_Q, decomposition = total_data
    evidence = [[total_P[i], total_Q[i]] for i in range(len(total_P))]
    labels = decomposition
    
    return evidence, labels
        
def lstm_data(raw_evidence, raw_labels, seq_lenght):
    new_labels = []
    new_evidence = []
    for i in range(len(raw_evidence)-(seq_lenght-1)):
        new_evidence.append(raw_evidence[i:i+seq_lenght])
        new_labels.append(raw_labels[i+(seq_lenght-1)])
    return np.array(new_evidence), np.array(new_labels)


def read_small_data(files, first, last):
    total_data = []
    for file in files:
        
        with open(f"{file}.csv") as f:
            reader = csv.reader(f)
            for i in range(first-1):
                next(reader)
                
            data_read = 0 
            data = []
            for row in reader:
                data.append(float(row[0]) if len(row)==1 else [float(cell) for cell in row])
                data_read += 1
                if data_read > (last - first):
                    break
                
            total_data.append(data)
            
    total_P, total_Q, decomposition = total_data
    evidence = [[total_P[i], total_Q[i]] for i in range(len(total_P))]
    labels = decomposition
    
    return evidence, labels