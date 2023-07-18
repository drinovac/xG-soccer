import csv
import os
import json
from math import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

SPAIN_ID = 11

training_seasons = [1,2,4,21,22,23,24,25,26,27,37,38,39,40]
test_season = [41, 42, 90]  

spain_league_matches = {}


def shot_angle(location):

    x = location[0]
    y = location[1]

    if(x > 60):
        if(y >= 36 and y <= 44):
            alfa = atan2((y-36), (120-x))
            beta = atan2((44-y), (120-x))
            return (beta + alfa)
        else:
            alfa = atan2((36-y), (120-x))
            beta = atan2((44-y), (120-x))
            return (beta - alfa)
    else:
        if(y >= 36 and y <= 44):
            alfa = atan2((y-36), x)
            beta = atan2((44-y), x)
            return (beta + alfa)
        else:
            alfa = atan2((36-y), x)
            beta = atan2((44-y), x)
            return (beta - alfa)

def distance_to_goal(location):

    x = location[0]
    y = location[1]

    if(x>60):
        return sqrt((120-x)**2 + (40-y)**2)
    else:
        return sqrt(x**2 + (40-y)**2)


class DataPrep:

    def __init__(self):
        self.number_of_goals = 0
        self.number_of_failure = 0
        self.shots = []
        self.limes = 1500

    def filter_leagues(self, dir):
        spain_dir = os.listdir(dir+"matches/"+str(SPAIN_ID))
        for file in spain_dir:
            f = open(dir + "matches/" + str(SPAIN_ID) + "/" + file, "r", encoding="utf8")
            data = json.load(f)
            temp_list = []
            for i in data:
                temp_list.append(i["match_id"])
            spain_league_matches[int(file.split(".")[0])] = temp_list
        return

    def extractShots(self, dir, key):
        for match in spain_league_matches[key]:
            f = open(dir + str(match) + ".json", "r", encoding="utf8")
            data = json.load(f)
            
            for i in data:
                type = i["type"]
                if(type['name'] == "Shot"):

                    useful_shot_info = []
                    shot_info = i["shot"]

                    if("under_pressure" in i):
                        useful_shot_info.append(-1)
                    else :
                        useful_shot_info.append(1)
                    useful_shot_info.append(i["position"]["id"])
                    useful_shot_info.append(i["play_pattern"]["id"])
                    useful_shot_info.append(shot_info["body_part"]["id"])
                    useful_shot_info.append(shot_info["technique"]["id"])
                    useful_shot_info.append(shot_info["type"]["id"])
                    useful_shot_info.append(shot_angle(i["location"]))
                    useful_shot_info.append(distance_to_goal(i["location"]))
                    useful_shot_info.append(shot_info["statsbomb_xg"])
                    if(shot_info["outcome"]["id"] == 97):
                        useful_shot_info.append(1)
                    else:
                        useful_shot_info.append(0)
                    
                    self.shots.append(useful_shot_info)
            f.close()
        return


    def writeData(self, file):

        with open(file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.shots)
        f.close()

        self.shots = []
        self.number_of_failure = 0
        self.number_of_goals = 0
        return

    def readData(self, dir):

        for key in training_seasons:
            self.extractShots(dir, key)

        self.writeData("./open-data-master/data/shots/train/data.csv")

        for key in test_season:
            self.extractShots(dir, key) 

        self.writeData("./open-data-master/data/shots/test/data.csv") 

        return


if __name__ == '__main__':

    prep = DataPrep()
    prep.filter_leagues("./open-data-master/data/")
    prep.readData("./open-data-master/data/events/")
