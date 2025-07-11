import pandas as pd


df = pd.read_csv("data/Oxford-102_Flower_dataset_labels.txt", names= ['Flower'] )

df.reset_index(names = 'id', inplace = True)

df.to_csv("data/labels.csv")