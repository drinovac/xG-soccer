import numpy as np
import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


class xG():

    def __init__(self):
        self.model = RandomForestRegressor(max_depth=6)

    def train(self, file):
        with open(file, mode='r') as f:
            reader = csv.reader(f)
            data = []
            for row in reader:
                data.append(row)
        f.close()

        np_array = np.array(data)

        np_array = np_array.astype(float)

        train_input = np_array[:,:-2]
        train_output = np_array[:, -1]

        self.model.fit(train_input, train_output)
        return

    def test(self, file):
        with open(file, mode='r') as f:
            reader = csv.reader(f)
            data = []
            for row in reader:
                data.append(row)
        f.close()

        np_array = np.array(data)
        np_array = np_array.astype(float)
        
        np.set_printoptions(suppress=True)

        test_input = np_array[:,:-2]
        test_statbombxG = np_array[:, -2]
   
        pred_proba = self.model.predict(test_input)

        print(np.sum(pred_proba))
        print(np.sum(test_statbombxG))
        
        mean_loss = mean_squared_error(pred_proba, test_statbombxG)
        print("MSE: ", mean_loss)
        
        score = self.model.score(test_input, test_statbombxG)
        print("Score: ", score)
        return    

if __name__ == '__main__':
    xg_model = xG()
    xg_model.train("./open-data-master/data/shots/train/data.csv")
    xg_model.test("./open-data-master/data/shots/test/data.csv")
    
