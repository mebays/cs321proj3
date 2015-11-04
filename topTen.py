import pandas as pd


def main():

    csvPanda = pd.read_csv(
        "/home/mebays/Documents/cs321/proj3/csvFiles/csvData2.csv")
    result = csvPanda.sort(['Number of times'], ascending=[False])
    topTen = result[['Number of times', 'URL']][0:10]
    topTen.to_csv(
        "/home/mebays/Documents/cs321/proj3/csvFiles/topTen.csv", sep=',')

main()
