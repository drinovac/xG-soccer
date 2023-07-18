import numpy as np
import csv
from sklearn.linear_model import LogisticRegression


class xG():

    def __init__(self):
        self.model = LogisticRegression(max_iter=1000, solver='saga')
        

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
        test_goal = np_array[:, -1]
        test_statbombxG = np_array[:, -2]

        pred_proba = self.model.predict_proba(test_input)
        
        print(np.sum(pred_proba[:, 1]))
        print(np.sum(test_statbombxG))
        
        mse = np.mean(np.square(pred_proba[:, 1] - test_statbombxG))
        print("MSE: ", mse)

        score = self.model.score(test_input, test_goal)
        print("Score: ", score)
        return


        

        


if __name__ == '__main__':
    xg_model = xG()
    xg_model.train("./open-data-master/data/shots/train/data.csv")
    xg_model.test("./open-data-master/data/shots/test/data.csv")
    
