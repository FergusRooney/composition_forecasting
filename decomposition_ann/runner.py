from decomposition_ann import ann

def train_save(model, model_to_load = None):
    model.create_ann()

def train_save_pred(model, model_to_load = None):
    model.create_ann()
    model.write_predictions_to_csv(first_prediction = 5876, number_of_predictions = 3200)

def load_pred(model, model_to_load):
    model.load_model(model_to_load)
    model.write_predictions_to_csv(first_prediction = 5876, number_of_predictions = 3200)

def main(train_or_predict):
    
    #setting up a model
    ann_type = "LSTM"               #type of ANN
    layers = [8]                    #array of numbers of units in each layer 
    house_train = 20                
    house_test = 20
    files_to_train = [f"decomposition_ann/total_P_new{house_train}", f"decomposition_ann/total_Q_new{house_train}", f"decomposition_ann/decomposition_new{house_train}"]  #files that are used to train ANN
    files_to_test =  [f"decomposition_ann/total_P_new{house_test}", f"decomposition_ann/total_Q_new{house_test}", f"decomposition_ann/decomposition_new{house_test}"]     #files that are used to make predictions

    file_to_write = "decomposition_ann/predictions"           #file to save predictions
    model_to_load = f"test_model{ann_type}" #file to load a model (only relevant if you want to load), make sure you load the same type (e.g. FFN)
    steps = 25                              #number of steps (only relevant for LSTM)
    
    model = ann.ANN(ann_type = ann_type, layers = layers, files_to_train= files_to_train, files_to_test= files_to_test, file_to_write = file_to_write, steps = steps)

    actions = [train_save, train_save_pred, load_pred]      #array of function pointers
    
    print("what do you want?")
    print("1. make, train and save a model")
    print("2. make, train, save and make predictions")
    print("3. load a model and make predictions")
    #action = int(input("enter a number: "))

    action = train_or_predict

    try:
        #calling a desired function
        #the solution mimics c-like swith-case
        #time to get to desired function is O(1)
        #elif-s would make developing code more difficult and time would be O(n)
        actions[action-1](model, model_to_load)
    
    except IndexError:
        print("PROGRAM TERMINATED")
        print("Enter one of the allowed numbers next time")
        
    #model = ann.ANN(ann_type = ann_type, layers = layers, files_to_train= files_to_train, files_to_test= files_to_test, steps = steps)
    #model.write_predictions_to_csv(first_prediction = 5876, number_of_predictions = 5000, file_to_write = file_to_write_predictions)


if __name__ == "__main__":
    main()