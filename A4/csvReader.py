import csv
from constants import *

def read_csv_to_dict(csv_file):
    data_dict = {}
    with open(csv_file, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for index,row in enumerate(csv_reader):
            # print("row = ", row)
            data_dict[index+1] = row
    
    # print(data_dict)
    student_details = data_dict
    return data_dict

# csv_file = 'assets/studentData.csv'
# data_dict = read_csv_to_dict(csv_file)
# print(data_dict)
