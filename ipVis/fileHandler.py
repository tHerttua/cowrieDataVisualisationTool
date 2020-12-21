import os
import csv
import json
from collections import Counter
from operator import itemgetter


class Filehandler:
    def __init__(self):
        self.scoreFiles = "data/scores/"


    def getLocationData(self, filepath):
        """
        Reads the geo data, returns a list with all data
        """
        geoData = []
        files = os.listdir(filepath)
        for afile in files:
            with open(filepath+afile) as r:
                data = json.loads(r.read())
                for entry in data:
                    geoData.append(entry)
        return geoData

    def findAllCountries(self, geoList):
        """
        Returns the list of countries that appear in the list
        """
        entries = {}
        for entry in geoList:
            entries[entry['ip']] = entry['location']['country']
        countries = []
        for _,val in entries.items():
            countries.append(val)
        return countries

    def getCountryCoordList(self):
        """
        Returns the list of country coordinates from a reference list
        """
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

    def getCountryScores(self, countries):
        """
        Counts the number of times a country appears in the list
        (Should be replaced with built-in count method)
        """
        distinct_countries = set(countries)

        country_scores = {}
        for country in distinct_countries:
            country_scores[country] = 0

        for country in countries:
            if country in distinct_countries:
                country_scores[country] += 1
        return country_scores

    def getScoredCoordinates(self, scores):
        """
        Returns list with country code, score, latitude, longitude and full name
        based on the scored list
        """
        countryGeos = self.getCountryCoordList()
        selectedCountryData = []
        for key,val in scores.items():
            for country in countryGeos:
                if key == country[0]:
                    selectedCountryData.append([key, val, country[1], country[2], country[3]])
        return selectedCountryData

    def getOne(self, folderPath):
        """
        Uses one list to find the values
        """
        geoData = []
        with open(folderPath) as r:
            data = json.loads(r.read())
            for entry in data:
                geoData.append(entry)
        countries = self.findAllCountries(geoData)
        scores = self.getCountryScores(countries)
        stuff = self.getScoredCoordinates(scores)
        return stuff


    def getScoredData(self, folderpath):
        """
        Uses all lists to find the values
        """
        geoList = self.getLocationData(folderpath)
        countries = self.findAllCountries(geoList)
        scores = self.getCountryScores(countries)
        stuff = self.getScoredCoordinates(scores)
        return stuff


    def findEvents(self, eventid, folderPath):
        """
        Finds all the events as a list
        """
        events = []
        listOfFiles = os.listdir(folderPath)
        for log in listOfFiles:
            with open(folderPath+log) as r:
                data = json.loads(r.read())
                for entry in data:
                    if eventid in str(entry['eventid']):
                        events.append(entry)
        return events


    def countAllEvents(self, folderPath):
        """
        Finds the number of all events
        """
        eventids = ['cowrie.session.connect', 
                    'cowrie.direct-tcpip.request', 
                    'cowrie.log.closed', 
                    'cowrie.client.version', 
                    'cowrie.session.file_upload',
                    'cowrie.session.file_download',
                    'cowrie.direct-tcpip.redirect', 
                    'cowrie.login.success', 
                    'cowrie.client.fingerprint', 
                    'cowrie.session.params', 
                    'cowrie.login.failed', 
                    'cowrie.command.success', 
                    'cowrie.client.kex', 
                    'cowrie.command.failed', 
                    'cowrie.client.size', 
                    'cowrie.tunnelproxy-tcpip.data', 
                    'cowrie.command.input', 
                    'cowrie.session.closed', 
                    'cowrie.direct-tcpip.tunnel', 
                    'cowrie.direct-tcpip.data']
        eventCount = []
        for event in eventids:
            events = self.findEvents(event, folderPath)
            x = (event, len(events))
            eventCount.append(x)
        for a,s in eventCount:
            print(a,s)


    def findAllCredentials(self, events):
        nms = []
        pws = []
        for event in events:
            nms.append(event['username'])
            pws.append(event['password'])

        creds = zip(nms,pws)
        return creds

    def findAllCommandInputs(self, events):
        inputs = []
        messages = []
        for event in events:
            inputs.append(event['input'])
            messages.append(event['message'])

        commands = zip(inputs,messages)
        return commands

    def getCredentialsAsWord(self, eventList):
        """
        Joins all the combinations and returns a string
        (mainly used for wordcloud)
        """
        creds = []
        for u,p in eventList:
            credString = u+" "+p
            creds.append(credString)
        credString = (" ").join(creds)
        return credString

    def getCommandsAsWord(self, eventList):
        """
        Forms a string of the commands for wordcloud
        """
        commands = []
        for cinput, _ in eventList:
            commands.append(cinput)
        commandsString = (" ").join(commands)
        return commandsString


    def countUniques(self, eventList):
        listedEvents = list(eventList)
        amounts = []
        uniques = set(listedEvents)

        for entry in uniques:
            amount = listedEvents.count(entry)
            data = (amount, entry[0], entry[1])
            amounts.append(data)
        sortedAmounts = sorted(amounts, key=itemgetter(0))
        sortedAmounts.reverse()
        
        return sortedAmounts

    def getScoreFile(self):
        attacksScoresList = []
        scoreFiles = os.listdir(self.scoreFiles)
        for scoreFile in scoreFiles:
            day = []
            with open(self.scoreFiles+scoreFile) as r:
                reader = csv.reader(r, delimiter=',')
                for row in reader:
                    day.append(row)
            for country in day:
                country[1] = int(country[1])
            sortedDay = sorted(day, key=itemgetter(1))
            sortedDay.reverse()
            attacksScoresList.append(sortedDay)
        return attacksScoresList

    def countAll(self, attacksScoresList):
        countries=[]
        attacks=[]
        for entry in attacksScoresList:
            if entry[4] in countries:
                index = countries.index(entry[4])
                attacks[index] += int(entry[1])
            else:
                countries.append(entry[4])
                attacks.append(int(entry[1]))
        total= zip(countries, attacks)
        sortedTotal = sorted(total, key=lambda x: x[1])
        sortedTotal.reverse()
        return sortedTotal      