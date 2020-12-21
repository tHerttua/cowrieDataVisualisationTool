import os
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.colors import Normalize
import matplotlib.patches as mpatches
from mpl_toolkits.basemap import Basemap
from ipVis.fileHandler import Filehandler
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs

ZOOM_SCALE = 8

EARTHCOLOR = np.array([143,188,143])/255.

COLORS1 = np.array([
                    (128, 0, 0),
                    (255, 0, 0),
                    (255, 69, 0),
                    (255, 160, 122),
                    (248, 222, 126),
                    ]) / 255.

COLORS2 = np.array([
                    (0, 63, 92),
                    (45, 135, 187),
                    (100, 194, 166),
                    (170, 222, 167),
                    (230, 246, 157),
                    ]) / 255.


class VisKit:
    def __init__(self):
        self.fh = Filehandler()
    

    def get_coords(self, jsonData):
        lats = []
        lngs = []
        if jsonData:
            with open(jsonData) as r:
                data = json.loads(r.read())
                for entry in data:
                    locData = entry['location']
                    lats .append(locData['lat']) 
                    lngs.append(locData['lng']) 
        return [lats, lngs]
        

    def create_bbox(self, coords):
        lats = coords[0]
        lngs = coords[1]
        bbox = [
            np.min(lats)-ZOOM_SCALE,
            np.max(lats)+ZOOM_SCALE,
            np.min(lngs)-ZOOM_SCALE,
            np.max(lngs)+ZOOM_SCALE,
        ]
        return bbox


    def createBaseMap(self, bbox):
        m = Basemap(projection='merc',
                    llcrnrlat=bbox[0],
                    urcrnrlat=bbox[1],
                    llcrnrlon=bbox[2],
                    urcrnrlon=bbox[3],
                    lat_ts=10,
                    resolution='i')
        return m 

    def outFileName(self, inputArg, thing):
        withoutExtension = os.path.splitext(inputArg)
        fileName = withoutExtension[0].split("/")
        output = "data/pics/"+thing+fileName[-1]+".png"
        return output

 
    def drawPieChart(self, mode, folderPath):
        files = os.listdir(folderPath)
        scoreFiles = [txt for txt in files if "Lon" in str(txt)]
        scoreFiles.sort()
        scoredList = self.fh.getScoreFile()
        top5 = []
        dayIndex = 1

        if mode == "indv":
            thing = "pieChart_"
            for day in scoredList:
                top5 = day[:5]
                countries=[]
                attacks=[]

                for entry in top5:
                    countries.append(entry[4]+" : "+str(entry[1]))
                    attacks.append(entry[1])

                plt.pie(attacks, labels=countries, colors=COLORS2, autopct='%1.1f%%',
                    wedgeprops={"edgecolor": 'black'})
                plt.title("Day {}".format(dayIndex))
                plt.tight_layout()
                plt.savefig(self.outFileName(folderPath, thing), format='png', dpi=300)
                dayIndex += 1
                plt.show()

        elif mode == "total":
            thing = "pieChartTotal_"
            sortedTopList = self.fh.countAll(scoredList)
            sources = []
            amounts = []

            for s,a in sortedTopList[:5]:
                sources.append(s+" : "+str(a))
                amounts.append(a)
            plt.pie(amounts, labels=sources, colors=COLORS2, autopct='%1.1f%%',
                    wedgeprops={"edgecolor": 'black'})
            plt.title("Top5 total")
            plt.tight_layout()
            plt.savefig(self.outFileName(folderPath,thing), format='png', dpi=300)
            plt.show()

    def drawAttacksourcesBarChart(self,cutoff,folderPath):
        thing = "barChart_"
        #files = os.listdir(folderPath)
        #scoreFiles = [txt for txt in files if "Ams" in str(txt)]
        #scoreFiles = files#.sort()
        scoredList = self.fh.getScoreFile()
        countries = []
        attacks = []

        sortedTopList = self.fh.countAll(scoredList)
        sortedTopList.reverse()
        for s,a in sortedTopList:
            if a > cutoff:
                countries.append(s)
                attacks.append(a)

        plt.barh(countries, attacks)

        plt.legend()

        plt.title("Unique attacks by country name")
        plt.xlabel("No. Attacks")
        plt.ylabel("Country")

        plt.tight_layout()
        plt.savefig(self.outFileName(str(cutoff),thing), format='png', dpi=300)

        plt.show()

    def getWords(self, folderPath, wordType):
        if wordType == 'command':
            events = self.fh.findEvents('command', folderPath)
            stuff = self.fh.findAllCommandInputs(events)
            word = self.fh.getCommandsAsWord(stuff)

        elif wordType == 'login':
            events = self.fh.findEvents('login', folderPath)
            stuff = self.fh.findAllCredentials(events)
            word = self.fh.getCredentialsAsWord(stuff)
      
        return word

    def getRankedWords(self, folderPath, wordType):
        if wordType == 'command':
            events = self.fh.findEvents('command', folderPath)
            stuff = self.fh.findAllCommandInputs(events)

        elif wordType == 'login':
            events = self.fh.findEvents('login', folderPath)
            stuff = self.fh.findAllCredentials(events)
        
        words = self.fh.countUniques(stuff)
      
        return words


    def drawWordCloud(self, folderPath, wordType):
        if wordType == 'command':
            thing = "commandsWordCloud_"
        elif wordType == 'login':
            thing = "credentialsWordCloud_"

        mask = np.array(Image.open("data/meta/circlemask.png"))
        words = self.getWords(folderPath, wordType)
        plt.figure()
        
        plt.axis('off')
        wordcloud = WordCloud(  width=4000,
                                height=3000,
                                relative_scaling=0,
                                random_state=1,
                                mask=mask,
                                background_color="white",
                                colormap='autumn',
                                collocations='True').generate(words)

        plt.imshow(wordcloud)
        plt.savefig(self.outFileName("ams",thing), bbox_inches="tight", dpi=300)

    def drawCredsBarChart(self, folderPath):
        words = self.getRankedWords(folderPath, 'login')
        
        creds = []
        amounts = []
        for word in words:
            if word[0] >= 5:
                credPair = word[1]+" : "+word[2]
                creds.append(credPair)
                amounts.append(word[0])

        self.drawCredsTop5(creds, amounts, folderPath)
        self.drawCredsWithoutTop(creds, amounts, folderPath)
        
        
    def drawCredsTop5(self, creds, amounts, folderPath):
        thing = "credsBarchart_top5"
        top5c = creds[:5]
        top5a = amounts[:5]
        plt.barh(top5c, top5a)
        plt.legend()
        plt.title("Top5 Username password combination")
        plt.xlabel("No. attempts")
        plt.tight_layout()
        plt.savefig(self.outFileName(folderPath, thing), format='png', dpi=300)
        plt.show()

    def drawCredsWithoutTop(self, creds, amounts, folderPath):
        thing = "credsBarchart_top"
        c = creds[5:25]
        a = amounts[5:25]
        plt.barh(c, a)
        plt.legend()
        plt.title("Top5 Username password combination")
        plt.xlabel("No. attempts")
        plt.tight_layout()
        plt.savefig(self.outFileName(folderPath, thing), format='png', dpi=300)
        plt.show()


    def drawMarkerMap(self, folderPath):
        coords = self.get_coords(folderPath)
        lats = coords[0]
        lngs = coords[1]
        bbox = self.create_bbox(coords)
        m = self.createBaseMap(bbox)
        plt.figure()
        m.drawcoastlines()
        m.fillcontinents(color='#76c666')
        m.drawcountries()
        thing = "markerMap_"

        x,y = m(lngs, lats)
        m.plot(x,y,marker='X',color='maroon', LineStyle='none')
        plt.savefig(self.outFileName(folderPath, thing), format='png', dpi=300)
        plt.show()

    def getPatches(self, colors, maxScore):
        handles = []
        i = len(colors)
        ratios = [(ratio/i) for ratio in range(i+1)]
        colorTuple = zip(colors, reversed(ratios))
        for color, ratio in colorTuple:
            attacks = ratio * maxScore
            if ratio <= 0.2:
                label = "At least 1 attack"
            else:
                label="More than {} attacks".format(round(attacks))
            colorPatch = mpatches.Patch(color=color, label=label)
            handles.append(colorPatch)
        return handles

    def get_color(self, score, maxScore, colors):
        ratio = score/maxScore
        if ratio > 0.8:
            return colors[0]
        elif ratio > 0.6 and ratio < 0.8:
            return colors[1]
        elif ratio > 0.4 and ratio < 0.6:
            return colors[2]
        elif ratio > 0.2 and ratio < 0.4:
            return colors[3]
        else:
            return colors[4]

    def getMaxScore(self, selectedCountryData):
        maxScore = 0
        for country in selectedCountryData:
            if country[1] > maxScore:
                maxScore = country[1]
        return maxScore


    def drawChoroMapTotal(self, folderPath):
        thing = "choroMap_"
        SHAPENAME = 'admin_0_countries'
        SHP = shpreader.natural_earth(resolution='110m', category='cultural', name=SHAPENAME)
        scoredList = self.fh.getScoredData(folderPath)
        for entry in scoredList:
            print(entry)
        countries = []
        attacks = []

        sortedTopList = self.fh.countAll(scoredList)
        for s,a in sortedTopList:
            countries.append(s)
            attacks.append(a)

        
        maxScore = attacks[0]
        color_patch = self.getPatches(COLORS1, maxScore)
        ax = plt.axes(projection=ccrs.PlateCarree(),)
        ax.figure.set_size_inches(11,12)

        for country in shpreader.Reader(SHP).records():
            ax.add_geometries([country.geometry], ccrs.PlateCarree(),
                                    facecolor=EARTHCOLOR,
                                    edgecolor='black')  
            for acountry in countries:
                if country.attributes['NAME_LONG'] == acountry:       
                    index = countries.index(acountry)    
                    ax.add_geometries([country.geometry], ccrs.PlateCarree(),
                                    facecolor=self.get_color(attacks[index],maxScore,COLORS1),
                                    edgecolor='black',
                                    label=country.attributes['NAME_LONG']) 

        
        plt.legend(handles=color_patch, loc='lower left', bbox_to_anchor=(0,0))
        plt.savefig(self.outFileName("total",thing), format='png', dpi=300)
        plt.show()

    def drawMapFromOneFile(self, folderPath):
        thing = "choroMap_"
        SHAPENAME = 'admin_0_countries'
        SHP = shpreader.natural_earth(resolution='110m', category='cultural', name=SHAPENAME)
        ax = plt.axes(projection=ccrs.PlateCarree(),)
        ax.figure.set_size_inches(11,12)
        selectedCountryData = self.fh.getOne(folderPath)
        maxScore = self.getMaxScore(selectedCountryData)
        color_patch = self.getPatches(COLORS1, maxScore)

        for country in shpreader.Reader(SHP).records():
            ax.add_geometries([country.geometry], ccrs.PlateCarree(),
                                    facecolor=EARTHCOLOR,
                                    edgecolor='black')  
            for scoredCountry in selectedCountryData:
                if country.attributes['NAME_LONG'] == scoredCountry[4]:           
                    ax.add_geometries([country.geometry], ccrs.PlateCarree(),
                                    facecolor=self.get_color(int(scoredCountry[1]),maxScore,COLORS1),
                                    edgecolor='black',
                                    label=country.attributes['NAME_LONG']) 

        
        plt.legend(handles=color_patch, loc='lower left', bbox_to_anchor=(0,0))
        plt.savefig(self.outFileName(folderPath, thing), format='png', bbox_inches='tight', dpi=300)
        plt.show()



