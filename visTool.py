import os
import argparse
from ipVis import visualizationkit, iplookup, logparser, fileHandler

APIKEY = ""
with open('data/meta/APIKEY.txt') as r:
    APIKEY = r.read() 

parser = argparse.ArgumentParser()
parser.add_argument('Input', type=str)
parser.add_argument('-c','--cleanLog', action="store_true", help="Cleans up a cowrie json log (in: unprocessed_log.json out: processed_log.json)")
parser.add_argument('-ip','--createIPlist', action="store_true", help="Creates list of IPs using cleaned log (in: processed_log.json out: iplist.txt)")
parser.add_argument('-l','--iplookup', action="store_true", help='Checks the geo data of IPs (in: iplist.txt out: x.json)')
#parser.add_argument('-pm', '--plotMarkers', action="store_true", help="Plots a map using one JSON geo data (in: x.json out: image.png)")
parser.add_argument('-pic', '--plotOneChoro', action="store_true", help="Plots a choropleth map using one JSON geo data (in: x.json out: image.png)")
parser.add_argument('-pac', '--plotTotalChoro', action="store_true", help="Plots a choropleth map using all JSON geo data found in path (in: folder out: image.png)")
#parser.add_argument('-crc', '--credCloud', action="store_true", help="Draw a word cloud of credentials using all cowrie logs in a folder (in: folder out: image.png)")
#parser.add_argument('-coc', '--commandCloud', action="store_true", help="Draw a word cloud of commands using all cowrie logs in a folder (in: folder out: image.png)")


args = parser.parse_args()
plotting = visualizationkit.VisKit()


if args.cleanLog:
    logparser = logparser.LogParser(args.Input)
    logparser.cleanAndWriteCowrieLog()
    print("\ncleaned log into data/cleaned/\n")

if args.createIPlist:
    logparser = logparser.LogParser(args.Input)
    logparser.writeIPlist()
    print( "\ncreated ip list into data/iplists/\n")

if args.iplookup:
    lookup = iplookup.IpLookup(args.Input, APIKEY=APIKEY)
    lookup.createDatafromIPlist()
    print("\ncreated file into data/geoData/\n")

"""if args.plotMarkers:
    plotting.drawMarkerMap(args.Input)
    print("\ndrew map\n")"""

if args.plotOneChoro:
    plotting.drawMapFromOneFile(args.Input)
    print("\ndrew map\n")

if args.plotTotalChoro:
    plotting.drawChoroMapTotal(args.Input)
    print("\ndrew map\n")

"""if args.credCloud:
    plotting.drawChoroMapTotal(args.Input)
    print("\ndrew word cloud\n")

if args.commandCloud:
    plotting.drawChoroMapTotal(args.Input)
    print("\ndrew word cloud\n")"""


    #plotting.drawMap()
    #plotting.writeData()
    #plotting.drawPieChart("total")
    #plotting.drawBarChart(20)
    #plotting.drawChoroMapTotal()
    
    #plotting.drawWordCloud(args.Input, 'command')
    #plotting.drawCredsBarChart(args.Input)
    #import ipVis.processcowrielog as lp
    #lp1 = lp.LogProcessor(args.Input)
    #lp1.countAllEvents()
    #plotting.printAll()
    
    


