import pandas as pd


def finder(myList, target):
    diff = pow(10, 30)
    index = None
    for i, num in enumerate(myList):
        if abs(target - num) < diff:
            diff = abs(target - num)
            index = i
    return index

def interAndMapping():


    EM_data = pd.read_csv("D:/01-DOCUMENT/01-zone/02-LANE/input/EM.csv")
    EM_data_time = EM_data["field.header.stamp"]

    EQ_data = pd.read_csv("D:/01-DOCUMENT/01-zone/02-LANE/input/EyeQ4VideoLane.csv")
    EQ_data_time = EQ_data["field.header.stamp"]
    # print(EM_data_time[0],EQ_data_time[0])
    EQ_start_index = finder(EQ_data_time, EM_data_time[0])
    EQ_end_index = finder(EQ_data_time, EM_data_time.values[-1])
    print(EQ_start_index,EQ_end_index)
    EQ_data = EQ_data[EQ_start_index:EQ_end_index]

    EM_start_index = finder(EM_data_time, EQ_data_time[0])
    EM_end_index = finder(EM_data_time, EQ_data_time.values[-1])
    print(EM_start_index,EM_end_index)
    EM_data = EM_data[EM_start_index:EM_end_index]
