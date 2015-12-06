#!/bin/bash python

import pandas as pd


def main():

    csvPandas = pd.read_csv(
        "C:/Users/Matthew/Documents/cs321/cs321proj3/csvFiles/urlCSVdata.csv")
    topTen = csvPandas[['File Name', 'text']]
    for i in range(len(topTen)):
    	f = open("C:/Users/Matthew/Documents/cs321/cs321proj3/htmlBody/"+topTen['File Name'][i]+".txt", mode="w")
	f.write(topTen['text'][i])


if __name__ == '__main__':

    main()
