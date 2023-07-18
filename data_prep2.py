import numpy as np
import os
import json
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import xlwt
from xlwt import Workbook

SPAIN_ID = 11

spain_league_matches = {}

class xG():
    def __init__(self):
        #self.brain = NeuralNetwork(8,5,1)
        self.treshold = 0.5

    def cross_entropy_loss(self, yHat, y):
        if(y == 1):
            return -np.log(yHat)
        else:
            return -np.log(1- yHat)

    def train(self, dir):

        files = os.listdir(dir)
        wb = Workbook()
        for file in files:
            f = open(dir + str(file), "r", encoding="utf8")

            data = json.load(f)
            
            losses = []
            pogotci = 0
            sum_xg = 0
            sum_predicted = 0

            index = 0

            for i in data:
                input = []

                input.append(i["position"])
                input.append(i["under_pressure"])
                input.append(i["play_pattern"])
                input.append(i["body_part"])
                input.append(i["technique"])
                input.append(i["type"])
                input.append(i["shot_angle"])
                input.append(i["distance"])

                inputs = np.array(input)
                inputs = np.reshape(input,(8,1))
                output = self.brain.feedforward(inputs)

                if(i["outcome"]["id"] == 97):
                    goal = 1
                else:
                    goal = 0
                
                sum_xg += abs(i["statsbomb_xg"] - output[0][0])

                if((output[0][0] > self.treshold and goal == 1) or (output[0][0] <= self.treshold and goal == 0)):
                    pogotci += 1

                loss = self.cross_entropy_loss(output[0][0], goal)
                #loss = nn.functional.binary_cross_entropy(torch.tensor([output[0][0]]), torch.tensor([goal]).float(), pos_weight=torch.tensor([7.25]))

                losses.append(loss)

                self.brain.backward(i["statsbomb_xg"], output)

                if(index % 500 == 0):
                    #print(sum(losses) / len(losses))
                    model.test("./open-data-master/data/shots/test/", wb, index)
                    print("Prosjecna razlika: ", sum_xg / len(losses))
                    print("Broj pogodaka: ", pogotci / len(losses))
                index += 1
            f.close()
        wb.save("Test.xls")
        with open("nn_config.npy", "wb") as f:
            np.save(f, self.brain.in_hidden_weights)
            np.save(f, self.brain.hidden_output_weights)
            np.save(f, self.brain.in_hidden_biases)
            np.save(f, self.brain.hidden_out_biases)

        return

    def test(self, dir, wb, name):

        files = os.listdir(dir)

        
        sheet = wb.add_sheet(str(name))

        sheet.write(0,0,"Calculated")
        sheet.write(0,1,"Actual")
        sheet.write(0,2,"Difference")

        index = 1

        for file in files:

            f = open(dir + file, "r", encoding="utf-8")

            data = json.load(f)

            for i in data:

                input = []
                input.append(i["position"])
                input.append(i["under_pressure"])
                input.append(i["play_pattern"])
                input.append(i["body_part"])
                input.append(i["technique"])
                input.append(i["type"])
                input.append(i["shot_angle"])
                input.append(i["distance"])
                
                inputs = np.array(input)
                inputs = np.reshape(input,(8,1))
                output = self.brain.feedforward(inputs)

                pogodak = 0
                if((output[0][0] > self.treshold and i["outcome"]["id"] == 97) or (output[0][0] < self.treshold and i["outcome"]["id"] != 97)):
                    pogodak = 1

                sheet.write(index, 0, output[0][0])
                sheet.write(index, 1, i["statsbomb_xg"])
                sheet.write(index, 2, abs(output[0][0] - i["statsbomb_xg"]))
                sheet.write(index, 3, pogodak)

                index += 1
                #print("Predicted:", output[0][0], "Actual:", i["statsbomb_xg"], "Difference:", abs(output[0][0] - i["statsbomb_xg"]))

        

        return
    


if __name__ == '__main__':
    model = xG()
    model.train("./open-data-master/data/shots/train/")
    
    
    