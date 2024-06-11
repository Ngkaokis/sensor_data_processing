import csv

with open("data/data1.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(", ".join(row))
