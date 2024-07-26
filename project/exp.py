import requests
import pandas as pd


df = pd.read_csv("component\data\Indian Cities Database.csv")


def cities(State):
    df = pd.read_csv("component\data\Indian Cities Database.csv")
   
    cities = df[df['State'] == State]
    return cities["City"].to_list()

result =  cities("Maharashtra")
print(result)