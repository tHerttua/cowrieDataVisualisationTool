import os
import json


class LogParser:
    def __init__(self, inputArg, outputArg=None, IPlist=None):
        self.cowrieLog = inputArg
        self.IPlistFile = IPlist


    def addColons(self):
        worklog = self.outFileName(self.cowrieLog, ".json")
        with open(self.cowrieLog, 'r') as r:
            with open(worklog, 'a+') as f:
                lines = r.readlines()
                for line in lines:
                    if len(line) > 5:
                        f.write(line)


    def addBracket(self):
        lines = []
        worklog = self.outFileName(self.cowrieLog, ".json")
        with open(worklog, 'r') as r:
            lines = r.readlines()
            last = lines[-1]
            if last[-1] == ",": 
                last = last[:-1]+"]"
                lines = lines[:-1]
                lines.append(last)
            elif last[-1] != "]":
                last = last+"]"
                lines = lines[:-1]
                lines.append(last)
        with open(worklog, 'w+') as f:
            first = lines[0]
            if first[0] != "[":
                lines[0] = "["+first
            for line in lines:
                f.write(line)

    def outFileName(self, filepath, ext):
        withoutExtension = os.path.splitext(filepath)
        fileName = withoutExtension[0].split("/")
        if ext == ".json":
            output = "data/cleaned/"+fileName[-1]+ext
        elif ext == ".txt":
            output = "data/iplists/"+fileName[-1]+ext
        return output
                

    def findIPs(self):
        IPlist = []
        with open(self.cowrieLog) as r:
            data = json.loads(r.read())
            for entry in data:
                sourceIP = entry['src_ip']
                IPlist.append(sourceIP)
        cleanList = list(set(IPlist))
        return cleanList


    def writeIPlist(self):  
        workfile = self.outFileName(self.cowrieLog, ".txt")
        ipList = self.findIPs()      
        with open(workfile, 'w+') as f:
            for IP in ipList:
                f.write(IP+"\n")


    def cleanAndWriteCowrieLog(self):
        self.addColons()
        self.addBracket()

