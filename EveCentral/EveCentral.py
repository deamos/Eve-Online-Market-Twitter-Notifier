#!/usr/bin/env python

import urllib2
import httplib
import csv
import time
import sys
import glob
from xml.etree import ElementTree as ET
from xml.dom.minidom import parse
import time
import datetime


from StringIO import StringIO
import gzip

cwp=sys.path[0]
sys.path.append(cwp)

#########################################################################
#Classes
#########################################################################

class itemPriceData:

	def __init__(self):
		
		now = datetime.date.today()
		updatetime=datetime.datetime.now()		
		self.updateDate = now

		self.scope = 0
		self.regionNum = 0
		self.systemNum = 0
		self.sellVolume = 0
		self.sellMin = 0
		self.sellMax = 0
		self.sellAvg = 0
		self.sellMed = 0
		self.sellPerc = 0

		self.buyVolume = 0
		self.buyMin = 0
		self.buyMax = 0
		self.buyAvg = 0
		self.buyMed = 0
		self.buyPerc = 0
	
	def updateData(self, date, updateSellVolume, updateSellMin, updateSellMax, updateSellAvg, updateSellMed, updateSellPerc, updateBuyVolume, updateBuyMin, updateBuyMax, updateBuyAvg, updateBuyMed, updateBuyPerc, scope = 0, regionNum=0, systemNum = 0):
		
		self.updateDate = date
		self.scope = scope
		self.regionNum = regionNum
		self.systemNum = systemNum
		self.sellVolume = updateSellVolume
		self.sellMin = updateSellMin
		self.sellMax = updateSellMax
		self.sellAvg = updateSellAvg
		self.sellMed = updateSellMed
		self.sellPerc = updateSellPerc
		self.buyVolume = updateBuyVolume
		self.buyMin = updateBuyMin
		self.buyMax = updateBuyMax
		self.buyAvg = updateBuyAvg
		self.buyMed = updateBuyMed
		self.buyPerc = updateBuyPerc
		
class itemPrices:
	
	def __init__(self, typeID):
		self.priceData = []
		
		self.typeID = typeID
		self.typeName = typeidtoname(typeID)
		
		self.importData()
		
	def addPrice(self, scope=1, regionName="The Forge", systemName="Jita"):
		
		scopeSubdata={}
		localSubdata={}		
		
		regionID = regionNametoRegionID(regionName)
		systemID = systemNametoSystemID(systemName)
		
		## Tests for if Daily Data Exists for Scope
		now = datetime.date.today()
		#for items in self.priceData:
		#	if items.scope == scope:
		#		if items.systemNum == systemID and items.scope == 1:
		#			if now == items.updateDate:
		#				return
		#		if items.regionNum == regionID and items.scope == 0:
		#			if now == items.updateDate:
		#				return
										
		rawXMLData = loadMarketStat(self.typeID, scope, regionID, systemID)
		
		loadedBuyVolume = volume(1)
		loadedBuyMin = minprice(1)
		loadedBuyMax = maxprice(1)
		loadedBuyAvg = avgprice(1)
		loadedBuyMed = medprice(1)
		loadedBuyPer = perprice(1)
		
		loadedSellVolume = volume(2)
		loadedSellMin = minprice(2)
		loadedSellMax = maxprice(2)
		loadedSellAvg = avgprice(2)
		loadedSellMed = medprice(2)
		loadedSellPer = perprice(2)
		
		newPriceData = itemPriceData()
		
		
		now = datetime.date.today()
		newPriceData.updateData(now, loadedSellVolume, loadedSellMin, loadedSellMax, loadedSellAvg, loadedSellMed, loadedSellPer, loadedBuyVolume, loadedBuyMin, loadedBuyMax, loadedBuyAvg, loadedBuyMed, loadedBuyPer, scope = scope, regionNum = regionID, systemNum = systemID)
		
		
		self.priceData.append(newPriceData)
		
		#if scope == 0:
			
		#	fileHandler=open("MarketData/" + str(self.typeID) + ".dat", 'a')
		#	fileHandler.write(str(now) + "," + str(scope) + "," + str(regionID) + "," + str(loadedSellVolume) + "," + str(loadedSellMin) + "," + str(loadedSellMax) + "," + str(loadedSellAvg) + "," + str(loadedSellMed) + "," + str(loadedSellPer) + "," + str(loadedBuyVolume) + "," + str(loadedBuyMin) + "," + str(loadedBuyMax) + "," + str(loadedBuyAvg) + "," + str(loadedBuyMed) + "," + str(loadedBuyPer))
		#	fileHandler.write("\n")
			
		#	fileHandler.close()
		
		#if scope == 1:
		#	fileHandler=open("MarketData/" + str(self.typeID) + ".dat", 'a')
		#	fileHandler.write(str(now) + "," + str(scope) + "," + str(systemID) + "," + str(loadedSellVolume) + "," + str(loadedSellMin) + "," + str(loadedSellMax) + "," + str(loadedSellAvg) + "," + str(loadedSellMed) + "," + str(loadedSellPer) + "," + str(loadedBuyVolume) + "," + str(loadedBuyMin) + "," + str(loadedBuyMax) + "," + str(loadedBuyAvg) + "," + str(loadedBuyMed) + "," + str(loadedBuyPer))
		#	fileHandler.write("\n")
						
		#	fileHandler.close()		
	
	def importData(self):
		
		rawList=[]
		
		try:
			return
		except IOError:
			return		
		else:
			for row in readFile:
				
												
				dataDate = datetime.datetime.strptime(row[0], "%Y-%m-%d").date()
				dataScope = int(row[1])
				dataLocation = int(row[2])
				dataSellVolume = float(row[3])
				dataSellMin = float(row[4])
				dataSellMax = float(row[5])
				dataSellAvg = float(row[6])
				dataSellMed = float(row[7])
				dataSellPer = float(row[8])
				dataBuyVolume = float(row[9])
				dataBuyMin = float(row[10])
				dataBuyMax = float(row[11])
				dataBuyAvg = float(row[12])
				dataBuyMed = float(row[13])
				dataBuyPer = float(row[14])
					
				newPriceData = itemPriceData()
				newPriceData.updateData(dataDate,dataSellVolume, dataSellMin, dataSellMax, dataSellAvg, dataSellMed, dataSellPer, dataBuyVolume, dataBuyMin, dataBuyMax, dataBuyAvg, dataBuyMed, dataBuyPer, scope = dataScope, regionNum = dataLocation, systemNum = dataLocation)
				self.priceData.append(newPriceData)
				#print newPriceData

class itemPriceHandler():

	def __init__(self):
		self.data={}
		
		#typeIDs = loadtypeids()
		
		for line in typeIDs:
			
			newItem=itemPrices(line)
			self.data[line]=newItem

#class historicPriceHandler():
#	def __init__(self):
#		self.orders=[]
#	
#	def newHistoric(self,region,system,typeid,bid,price,volremain):
#		newOrder = historicPriceItem(region,system,typeid,bid,price,volremain)
#		self.orders.append(newOrder)
#	 
#	def getMin(self,typeid,bid,scope,system=0,region=0):
#		Min = 999999999999999999999999
#		for line in self.orders:
#			if scope == 0:
#				if line.bid == bid and line.typeID == typeid and line.regionID == region:
#					if line.price < Min:
#						Min = line.price
#					 
#			if scope == 1:
#				if line.bid == bid and line.typeID == typeid and line.systemID == system:
#					if line.price < Min:
#						Min = line.price	
#		if Min == 999999999999999999999999:
#			Min = 0			
#		return Min
		
#	def getMax(self,typeid,bid,scope,system=0,region=0):
#		Max = 0
#		for line in self.orders:
#			if scope == 0:
#				if line.bid == bid and line.typeID == typeid and line.regionID == region:
#					if line.price > Max:
#						Max = line.price
#					 
#			if scope == 1:
#				if line.bid == bid and line.typeID == typeid and line.systemID == system:
#					if line.price > Max:
#						Max = line.price		
#		return Max
#		
#	def getAvg(self,typeid,bid,scope,system=0,region=0):
#		Total = 0
#		Itteration = 0
#		for line in self.orders:
#			if scope == 0:
#				if line.bid == bid and line.typeID == typeid and line.regionID == region:
#					Total = Total + line.price
#					Itteration = Itteration + 1
#							 
#			if scope == 1:
#				if line.bid == bid and line.typeID == typeid and line.systemID == system:
#					Total = Total + line.price
#					Itteration = Itteration + 1
#		if Itteration == 0:
#			Itteration = 1
#		Avg = Total / Itteration
#		return Avg
			
#class historicPriceItem:
#	def __init__(self,region,system,typeid,bid,price,volremain):
#		self.regionID = region
#		self.systemID = system
#		self.typeID = typeid
#		self.bid = bid
#		self.price = price
#		self.volremain = volremain
	
	
	
	

#####################################################################################################################################################
#Functions
#####################################################################################################################################################
def loadMarketStat(typeID, scope, regionID, systemID):
	typeidstr=str(typeID)
	regionID = str(regionID)
	systemID = str(systemID)
	global URLError 

	URLError = True
	
	while URLError == True:
		if scope == 0:
			url="http://api.eve-central.com/api/marketstat?typeid=" + typeidstr + "&regionlimit=" + regionID
			try:
				marketDataXML=urllib2.urlopen(url).read()
			except:
				URLError = True
				time.sleep(1)
			else:
				URLError = False

		elif scope == 1:
			url="http://api.eve-central.com/api/marketstat?typeid=" + typeidstr + "&usesystem=" + systemID
			try:
				marketDataXML=urllib2.urlopen(url).read()
			except:
				URLError = True
				time.sleep(1)
			else:
				URLError = False


	if URLError == False:
		File=open('MarketDataCache.dat', 'w')
		File.write(marketDataXML)

     	File.close()
    
	return 

def volume(type): 
   
    dom = parse('MarketDataCache.dat')
    my_node_list = dom.getElementsByTagName("volume")
    my_n_node = my_node_list[type]
    my_child = my_n_node.firstChild
    my_text = my_child.data
    return my_text

# Eve Central
def avgprice(type): 
   
    dom = parse('MarketDataCache.dat')
    my_node_list = dom.getElementsByTagName("avg")
    my_n_node = my_node_list[type]
    my_child = my_n_node.firstChild
    my_text = my_child.data
    return my_text

# Eve Central
def maxprice(type): 
   
    dom = parse('MarketDataCache.dat')
    my_node_list = dom.getElementsByTagName("max")
    my_n_node = my_node_list[type]
    my_child = my_n_node.firstChild
    my_text = my_child.data
    return my_text

# Eve Central
def minprice(type): 
   
    dom = parse('MarketDataCache.dat')
    my_node_list = dom.getElementsByTagName("min")
    my_n_node = my_node_list[type]
    my_child = my_n_node.firstChild
    my_text = my_child.data
    return my_text

# Eve Central
def medprice(type): 
   
    dom = parse('MarketDataCache.dat')
    my_node_list = dom.getElementsByTagName("median")
    my_n_node = my_node_list[type]
    my_child = my_n_node.firstChild
    my_text = my_child.data
    return my_text

# Eve Central
def perprice(type): 
   
    dom = parse('MarketDataCache.dat')
    my_node_list = dom.getElementsByTagName("percentile")
    my_n_node = my_node_list[type]
    my_child = my_n_node.firstChild
    my_text = my_child.data
    return my_text

###############################################################
def loadtypeids():
    #Loads the Descriptor for Each TypeID
    typeidcsv = csv.reader(open("EveDB/invTypes.csv", "rb"))
    typeids =  {}
    for row in typeidcsv:
        typeids[int(row[0])]=(row[2])
    return typeids

def itemnametotypeid(name):
    
    for row in typeIDs:
        #If the TypeID exists for Name, Display typeID and Read Requirements    
        if (typeIDs[row] == name):
            return row
        

#Converts a TypeID directly to a Name
def typeidtoname(tid):
    return typeIDs[tid]
    
def loadRegionIDs():
    #Loads the Descriptor for Each RegionID
    regionidcsv = csv.reader(open("EveDB/mapRegions.csv", "rb"))
    regionids =  {}
    for row in regionidcsv:
        regionids[int(row[0])]=(row[1])
    return regionids

def regionNametoRegionID(name):
    
    for row in regionIDs:
        #If the RegionID exists for Name, Display RegionID and Read Requirements    
        if (regionIDs[row] == name):
            return row 

def loadSystemIDs():
    #Loads the Descriptor for Each SystemID
    systemidcsv = csv.reader(open("EveDB/mapSolarSystems.csv", "rb"))
    systemids =  {}
    for row in systemidcsv:
        systemids[int(row[2])]=(row[3])
    return systemids  

def systemNametoSystemID(name):
    
    for row in systemIDs:
        #If the SystemID exists for Name, Display SystemID and Read Requirements    
        if (systemIDs[row] == name):
            return row 

################################################

def updatePrice(itemName, scope=1, RegionName="The Forge", SystemName="Jita"):
	mainItemHandler.data[itemnametotypeid(itemName)].addPrice(scope,RegionName,SystemName)
	
	return

def priceData(itemName, date,scope=1, RegionName="The Forge", SystemName="Jita"):
	systemID=systemNametoSystemID(SystemName)
	regionID=regionNametoRegionID(RegionName)
	
	#Check for Required Info
	for items in mainItemHandler.data[itemnametotypeid(itemName)].priceData:
		if items.updateDate == date:
			if items.scope == scope:
				if items.systemNum == systemID  and scope == 1:
					return items
				if items.regionNum == regionID and scope == 0:
					return items
						
	#If info does not exist, return a zero
	return 0 

def updateAll():
	for typeID in typeIDs:
		updatePrice(typeidtoname(typeID))
		requestedData = priceData(typeidtoname(typeID),now)


#########################################################################################################
#Main
########################################################################################################
print("Importing Eve Central Data.....")
#Required Loading
typeIDs = loadtypeids()
regionIDs=loadRegionIDs()
systemIDs=loadSystemIDs()
URLError = False

now = datetime.date.today()

mainItemHandler=itemPriceHandler()
