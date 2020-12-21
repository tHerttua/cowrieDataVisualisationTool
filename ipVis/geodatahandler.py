import json 
import os
import csv
import numpy as np
import itertools
from operator import itemgetter


class GeoDataHandler:
    def __init__(self):
        pass

    def getCountryCoordList(self):
        countryCoords = []
        with open('data/meta/countries.csv') as f:
            lines = f.readlines()
        for line in lines:
            countryData = line.split()
            if len(countryData) != 4:
                index = len(countryData) -4
                for i in range(index):
                    countryData[3] += " "+countryData[4+i]
            countryCoords.append(countryData)

        return countryCoords


    def getLocationData(self, filepath):
        geoData = []
        with open(filepath) as r:
            data = json.loads(r.read())
            for entry in data:
                geoData.append(entry)
        return geoData



    def findAllCountries(self, geoList):
        entries = {}
        for entry in geoList:
            entries[entry['ip']] = entry['location']['country']
        countries = []
        for _,val in entries.items():
            countries.append(val)
        return countries


    def getCountryScores(self, countries):
        distinct_countries = set(countries)

        country_scores = {}
        for country in distinct_countries:
            country_scores[country] = 0

        for country in countries:
            if country in distinct_countries:
                country_scores[country] += 1
        return country_scores

    def getTotalByCountry(self, folderPath):
        files = os.listdir(folderPath)
        for scoredCountry in files:
            with open(folderPath+scoredCountry) as f:
                print(f.read())



    def getScoredCoordinates(self, scores):
        countryGeos = self.getCountryCoordList()
        selectedCountryData = []
        for key,val in scores.items():
            for country in countryGeos:
                if key == country[0]:
                    selectedCountryData.append([key, val, country[1], country[2], country[3]])
        return selectedCountryData

    
    def writeData(self, pathToFile):
        geoList = self.getLocationData(pathToFile)
        countries = self.findAllCountries(geoList)
        scores = self.getCountryScores(countries)
        stuff = self.getScoredCoordinates(scores)
        dirFiles = os.listdir('data/scores/')
        with open('data/scores/scoreAms{}.csv'.format(str(len(dirFiles))), 'a+') as f:
            writer = csv.writer(f)
            writer.writerows(stuff)