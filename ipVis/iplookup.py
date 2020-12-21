import os
import json
from simple_geoip import GeoIP


class IpLookup:
    def __init__(self, inputArg, APIKEY):
        self.input = inputArg
        self.geoip = GeoIP(APIKEY)

    def getIPlist(self):
        IPlist = []
        with open(self.input, 'r') as r:
            for line in r.read().split():
                IPlist.append(line)
        return IPlist

    def outPutFile(self):
        withoutExtension = os.path.splitext(self.input)
        fileName = withoutExtension[0].split("/")
        output = "data/geoData/"+fileName[-1]+".json"
        return output

    def createJsonGeoData(self, IPlist):
        data = []

        outfile = self.outPutFile()
        for IP in IPlist:
            data.append(self.geoip.lookup(IP))

        with open(outfile, "a+") as f:
            json.dump(data, f) 

    def createDatafromIPlist(self):
        ips = self.getIPlist()
        self.createJsonGeoData(ips) 