from decomposition_ann.files import read_small_data
import numpy as np
import csv

def make_prediction(last_data, model, files_to_read, steps_num= None):
    
    if steps_num:
        evidence, labels = read_small_data(files_to_read, last_data - steps_num+1, last_data)
        in_data = [ev for ev in evidence]
        data =np.array(in_data)
        data = data.reshape((1, steps_num, 2))          
    else:
        evidence, labels = read_small_data(files_to_read, last_data, last_data)
        data =np.array(evidence)
 
    prediction = model.predict(data)

    return prediction


def print_progress(total, done):
    
    bar_lenght = 20
    progress = done/total
    loading_chars = ['\\', '|', '/', '-']
    char_key = int((done/10)%4)
    print("[" + "#"*int(progress*bar_lenght) + "."*(bar_lenght- int(progress*bar_lenght)) + "] " + loading_chars[char_key], end= "\r")


def write_predictions(first_pred, num_pred, model, files_to_read, file_to_write, steps= None):

    num_done = 0
    print(f"writting {num_pred} predictions to {file_to_write}.csv")
    
    with open(f'{file_to_write}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        for i in range(num_pred):
            data_to_predict = first_pred- 1 + i
            prediction = make_prediction(data_to_predict, model, files_to_read, steps)
            prediction= prediction[0]
            writer.writerow(prediction)
            num_done += 1
            
            if (num_done % 10 == 0):
                print_progress(num_pred, num_done)
    print("\nwriting done")