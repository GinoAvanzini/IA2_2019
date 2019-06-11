
import csv

if __name__ == "__main__":
    dates = []
    scores = []

    i = 0
    with open('A_Z Handwritten Data.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            dates.append(row)
            break
            # scores.append(row[1])
    

    print(i)
    # print(scores)