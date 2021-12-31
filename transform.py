import pandas as pd

# construct id function
def construct_id(df, column1, column2):
    edited_column1 = df[column1].apply(lambda title: title[-5:].replace(' ','_'))
    return edited_column1+ "_"+ df[column2] 