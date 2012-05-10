import curses
import copy
import datetime
import os
import sys
import time
import ConfigParser
import random


cwp=sys.path[0]
sys.path.append(cwp)

import tweepy
from EveCentral import *


#######################################
#classes
#######################################

class watchItem:
    
    def __init__(self,typeID,buyorsell,direction,threshhold):
        self.id = random.randint(100,10000)
        self.typeID = typeID
        self.buyorsell = buyorsell
        self.direction = direction
        self.threshhold = threshhold
        self.notified = False
        
class watchListClass:
    
    def __init__(self):
        self.listing=[]
        
    def removeItem(self,index):
        self.listing.pop(index)
        
    def addItem(self,item):
        self.listing.append(item)
        
########################################

########################################
#functions
########################################

def addNewItem(typeName,buyorsell,rawDirection,threshhold):

    typeID = itemnametotypeid(typeName)
    
    if rawDirection == ">":
        direction = 1
    elif rawDirection == "<":
        direction = 0
    
    newItem = watchItem(typeID,buyorsell,direction,threshhold)
    watchList.addItem(newItem)
    
    return
    

def removeItem(index):

    watchList.removeItem(index)
    return

def performItemCheck(item):
    global previousMarketData
    
    now = datetime.date.today()        
    itemName = typeidtoname(item.typeID)
               
    if item.direction == 0:
        operation = 0
    elif item.direction == 1:
        operation = 1
                
    updatePrice(itemName, scope=1, SystemName="Jita")
    if URLError == False:
        marketPrice = priceData(itemName, now,scope=1, RegionName="The Forge", SystemName="Jita")
    elif URLError == True:
        marketPrice = previousMarketData[itemnametotypeid]
    
    if item.buyorsell == "b" or item.buyorsell == "B":
        if operation == 0:
            if float(marketPrice.buyMax) < float(item.threshhold):
                if item.notified == False:
                    api.update_status('@' + twitterName + " #" + str(item.id) + " " + itemName +" - Exceeded Buy Threshhold < " + str(float2comma(float(item.threshhold))) + " at " + str(float2comma(float(marketPrice.buyMax))))
                    item.notified = True
                return True
        elif operation == 1:
            if float(marketPrice.buyMax) > float(item.threshhold):
                if item.notified == False:
                    api.update_status('@' + twitterName + " #" + str(item.id) + " " + itemName +" - Exceeded Buy Threshhold > " + str(float2comma(float(item.threshhold))) + " at " + str(float2comma(float(marketPrice.buyMax))))
                    item.notified = True
                return True
    elif item.buyorsell == "s" or item.buyorsell == "S":
        if operation == 0:
            if float(marketPrice.sellMin) < float(item.threshhold):
                if item.notified == False:
                    api.update_status('@' + twitterName + " #" + str(item.id) + " " + itemName +" - Exceeded Sell Threshhold < " + str(float2comma(float(item.threshhold))) + " at " + str(float2comma(float(marketPrice.sellMin))))
                    item.notified = True
                return True
        elif operation == 1:
            if float(marketPrice.sellMin) > float(item.threshhold):
                if item.notified == False:
                    api.update_status('@' + twitterName + " #" + str(item.id) + " " + itemName +" - Exceeded Sell Threshhold: >" + str(float2comma(float(item.threshhold))) + " at " + str(float2comma(float(marketPrice.sellMin))))
                    item.notified = True
                return True
    return False


def float2comma(f):
    s = str(abs(f)) # Convert to a string
    decimalposition = s.find(".") # Look for decimal point
    if decimalposition == -1:
        decimalposition = len(s) # If no decimal, then just work from the end
    out = "" 
    for i in range(decimalposition+1, len(s)): # do the decimal
        if not (i-decimalposition-1) % 3 and i-decimalposition-1: out = out+","
        out = out+s[i]      
    if len(out):
        out = "."+out # add the decimal point if necessary
    for i in range(decimalposition-1,-1,-1): # working backwards from decimal point
        if not (decimalposition-i-1) % 3 and decimalposition-i-1: out = ","+out
        out = s[i]+out      
    if f < 0:
        out = "-"+out
    return out
####################################
#Curses Functions
####################################

def initMainWindow():
    ##Creates Main Window
    screen = curses.initscr()
    
    ##Resizes the Terminal
    

    ##Disables key Echos
    curses.noecho()

    ##Enable cbreak Mode
    curses.cbreak()

    ##Enable keypad mode
    screen.keypad(1)
    

    return screen
    
def mainMenu(screen):
    curses.start_color()
    curses.init_pair(1,curses.COLOR_RED, curses.COLOR_WHITE)
    pos=1
    x=None
    h=curses.color_pair(1)
    n=curses.A_NORMAL
    rows,cols = screen.getmaxyx()
    screen.nodelay(1)
    
    informationWin = screen.subwin(3,cols-2,rows-4,1)
    refresh = 0
    while x != ord('\n'):
        screen.clear()
        screen.border(0)
        
        informationWin.border(0)
        
        screen.addstr(1,2, "Eve Online Aura Terminal - v0.2a", curses.A_STANDOUT)
        screen.addstr(2,2, "Created by Deamos: If you find this useful, please donate ISK.", curses.A_NORMAL)
        screen.addstr(4,2, "Please select an option...", curses.A_BOLD)
        
        if pos == 1:
            screen.addstr(5,4, "1 - Add/Remove Watch Data",h)
        else:
            screen.addstr(5,4, "1 - Add/Remove Watch Data",n)
        if pos == 2:
            screen.addstr(6,4, "2 - Begin Market Scan",h)
        else:
            screen.addstr(6,4, "2 - Begin Market Scan",n)

        if pos == 3:
            screen.addstr(8,4, "3 - Exit", h)
        else:
            screen.addstr(8,4, "3 - Exit", n)
        
        screen.addstr(15,2, "Eve Online Market Notifier is only as accurate as Eve-Central. Reported data may be delayed.", curses.A_NORMAL)
        screen.addstr(16,2, "It is recommended to run a tool like Contribtastic to help keep the market data accurate!", curses.A_NORMAL)
        screen.addstr(18,2, "***Note***", curses.A_NORMAL)
        screen.addstr(19,2, "This Version only covers the Jita Market (Sell:Sell Minimum / Buy:Buy Max)", curses.A_NORMAL)
            
        localtime = time.asctime(time.localtime(time.time()))
        informationWin.addstr(1,1,localtime,n)
        
        if refresh == 1:
        
            screen.noutrefresh()
        
        localtime = time.asctime(time.localtime(time.time()))
        informationWin.addstr(1,1,localtime,n)
        informationWin.noutrefresh()
        
        curses.doupdate()
            
        x=screen.getch()
        time.sleep(.22)
            
        if x == ord('1'):
            pos = 1
            refresh = 1
            
        elif x == ord("2"):
            pos = 2
            refresh = 1
        elif x == ord("3"):
            pos = 3
            refresh = 1

        
        elif x == 258:
            if pos < 3:
                pos += 1
                refresh = 1
            else:
                pos = 1
                refresh = 1
        elif x == 259:
            if pos > 1:
                pos += -1
                refresh = 1
            else:
                pos = 3
                refresh = 1
        elif x == -1:
            refresh = 0
            
        elif x != ord('\n'):
            curses.flash()
            screen.addstr(11,1,"Invalid Key",curses.A_BOLD)
            screen.refresh()
            time.sleep(.75)

    return str(pos)

def monitorDataMenu(screen):
    
    global previousMarketData
    rows,cols = screen.getmaxyx()
    
    #Creates New Window    
    itemSubWin = curses.newwin(rows-2,cols-2,1,1) 
    
    #Enables Keypad Input and prepares the Window
    itemSubWin.keypad(1)
    itemSubWin.clear()
    itemSubWin.border(0)
    itemSubWin.nodelay(1)
    
    h=curses.color_pair(1)
    
    y = None
    
    #Establishes Size of Input Display Values
    displayLineLimit = rows-9    
    beginNum = 0
    endNum = beginNum + displayLineLimit
    pos = beginNum
    
    cursor = 0
    
    while y != ord('q'):

        currentX = 1
        currentY = 4
        
        itemSubWin.addstr(2,currentX,"Item Name")
        itemSubWin.addstr(2,currentX+30,"Buy/Sell")
        itemSubWin.addstr(2,currentX+50,"Operator")
        itemSubWin.addstr(2,currentX+70,"Threshhold")
        itemSubWin.addstr(2,currentX+90,"Current Market")
        itemSubWin.addstr(2,currentX+110,"Threshhold Met")
        
        #Begin Data Display.  Increments pos within the Array and displays from beginNum to endNum 
        while endNum != pos:
            
            try:
                row = watchList.listing[pos]
            except:
                endNum = pos
            else:
                #Used to Highlight the Selected Item
                if cursor == pos:
                    textHighlight = h
                else:
                    textHighlight = curses.A_NORMAL
                
                if row.direction == 1:
                    stringDirection = ">"
                elif row.direction == 0:
                    stringDirection = "<"
                    
                now = datetime.date.today()
                typeName = typeidtoname(row.typeID)   
                updatePrice(typeName,scope=1,SystemName="Jita")
                requesteddata = priceData(typeName,now, scope=1)
                    
                if row.buyorsell == "b" or row.buyorsell == "B":
                    stringBorS = "Buy"
                    eveCPrice = requesteddata.buyMax
                elif row.buyorsell == "s" or row.buyorsell == "S":
                    stringBorS = "Sell"
                    eveCPrice = requesteddata.sellMin
                
                metThreshhold=performItemCheck(row)
                
                itemSubWin.addnstr(currentY,currentX,str(typeidtoname(row.typeID)),25,curses.A_NORMAL)
                itemSubWin.addstr(currentY,currentX+30,stringBorS)
                itemSubWin.addstr(currentY,currentX+50,stringDirection)
                itemSubWin.addstr(currentY,currentX+70,str(float2comma(float(row.threshhold))))
                itemSubWin.addstr(currentY,currentX+90,str(float2comma(float(eveCPrice))))
                if metThreshhold == True:
                    itemSubWin.addstr(currentY,currentX+115,"****")

                currentY = currentY+1
            
                pos = pos + 1
        
        
        itemSubWin.refresh()
        y=itemSubWin.getch()
        pos = beginNum
        
        ############################################################
        #Handles program ability to be responsive without flooding Eve-Central with requests
        
        for x in range(1,600):
            time.sleep(.5)
            itemSubWin.addstr(rows-5,2,"Next Refresh in:" + str((600-x)/2) +" secs")
            if URLError == True:
                itemSubWin.addstr(rows-5,30,"**Error**")
            else:
                itemSubWin.addstr(rows-5,30,"**Live**")
            itemSubWin.addstr(rows-5,115,"(q)uit")
            y=itemSubWin.getch()
            #itemSubWin.deleteln()
            if y == ord('q'):
                return
        
        previousMarketData = []
        
        if URLError == False or URLError == True:
            for item in mainItemHandler.data:
                previousMarketData = copy.deepcopy(mainItemHandler.data[item].priceData)
                mainItemHandler.data[item].priceData = []

        #Window Input Lines---- To Be added back in at a later date
        ########################################################
        #    if y == 258:
        #        cursor = cursor + 1
        #        if cursor >= endNum:
        #            cursor = beginNum
        #            pos = beginNum
        #            itemSubWin.clear()
        #            itemSubWin.border(0) 
        #            x=10               
        #    elif y == 259:
        #        cursor = cursor - 1
        #        if cursor < beginNum:
        #            cursor = endNum-1
        #            pos = beginNum
        #        itemSubWin.clear()
        #        itemSubWin.border(0)
        #        x=10
            
        #    elif y == ord("\n"):
            
        #        pos = beginNum
        #        itemSubWin.clear()
        #        itemSubWin.border(0)
        #        x=10
 
def watchDataMenu(screen):
    
    rows,cols = screen.getmaxyx()
    
    #Creates New Window    
    itemSubWin = curses.newwin(rows-2,cols-2,1,1) 
    
    #Enables Keypad Input and prepares the Window
    itemSubWin.keypad(1)
    itemSubWin.clear()
    itemSubWin.border(0)
    
    h=curses.color_pair(1)
    
    y = None
    
    #Establishes Size of Input Display Values
    displayLineLimit = rows-9    
    beginNum = 0
    endNum = beginNum + displayLineLimit
    pos = beginNum
    
    cursor = 0
    
    while y != ord('q'):

        currentX = 1
        currentY = 4
        
        itemSubWin.addstr(2,currentX,"Item Name")
        itemSubWin.addstr(2,currentX+30,"Buy/Sell")
        itemSubWin.addstr(2,currentX+50,"Operator")
        itemSubWin.addstr(2,currentX+70,"Threshhold")

        #Begin Data Display.  Increments pos within the Array and displays from beginNum to endNum 
        while endNum != pos:
            
            try:
                row = watchList.listing[pos]
            except:
                endNum = pos
            else:
                #Used to Highlight the Selected Item
                if cursor == pos:
                    textHighlight = h
                else:
                    textHighlight = curses.A_NORMAL
                
                if row.direction == 1:
                    stringDirection = ">"
                elif row.direction == 0:
                    stringDirection = "<"
                    
                if row.buyorsell == "b" or row.buyorsell == "B":
                    stringBorS = "Buy"
                elif row.buyorsell == "s" or row.buyorsell == "S":
                    stringBorS = "Sell"
                
                itemSubWin.addnstr(currentY,currentX,str(typeidtoname(row.typeID)),25,textHighlight)
                itemSubWin.addstr(currentY,currentX+30,stringBorS)
                itemSubWin.addstr(currentY,currentX+50,stringDirection)
                itemSubWin.addstr(currentY,currentX+70,str(float2comma(float(row.threshhold))))

                currentY = currentY+1
            
                pos = pos + 1
        
        itemSubWin.addstr(rows-4,75,"(a)dd a New Item / (d)elete Selected Item / (q)uit")
            
        itemSubWin.refresh()
        y=itemSubWin.getch()
        
        #Window Input Lines
        ########################################################
        
        ################################
        #Handles Input from Up Key / Down Key to move Cursor
        if y == 258:
            cursor = cursor + 1
            if cursor >= endNum:
                cursor = beginNum
            pos = beginNum
            itemSubWin.clear()
            itemSubWin.border(0)                
        elif y == 259:
            cursor = cursor - 1
            if cursor < beginNum:
                cursor = endNum-1
            pos = beginNum
            itemSubWin.clear()
            itemSubWin.border(0)
        
        ################################
        #Adds new Watch Item
        elif y == ord('a'):
            cursor = cursor - 1
            iteminput = ""
            buyorsellinput = ""                        
            directionInput = ""
            threshholdInput = 0 
            
            ###########################################
            #Handling of Input for new Watch Item
            curses.echo()
            
            validInput = False
            while validInput == False:
                
                itemSubWin.addstr(rows-3,1,"Item Name:",curses.A_STANDOUT)
                iteminput = itemSubWin.getstr(rows-3,12,50)
                typeID=itemnametotypeid(iteminput)
                try:
                    if iteminput == typeIDs[typeID]:
                        validInput = True
                except:
                    validInput = False
                itemSubWin.deleteln()
            
            validInput = False
            while validInput == False:
                
                itemSubWin.addstr(rows-3,1,"Buy(b) or Sell(s):",curses.A_STANDOUT)
                buyorsellinput = itemSubWin.getstr(rows-3,19,1)
                if buyorsellinput == "b" or buyorsellinput == "B" or buyorsellinput == "s" or buyorsellinput == "S":
                    validInput = True
                else:
                    validInput = False
                itemSubWin.deleteln()
            
            validInput = False
            while validInput == False:
                
                itemSubWin.addstr(rows-3,1,"Greater Than(>) or Less Than(<):",curses.A_STANDOUT)
                directionInput = itemSubWin.getstr(rows-3,34,1)
                if directionInput == ">" or directionInput == "<":
                    validInput = True
                else:
                    validInput = False
                itemSubWin.deleteln()
            
            validInput = False
            while validInput == False:
                
                itemSubWin.addstr(rows-3,1,"Threshhold:",curses.A_STANDOUT)
                threshholdInput = itemSubWin.getstr(rows-3,13,15)
                try:
                    threshholdInput = float(threshholdInput)
                except:
                    validInput = False
                    
                if isinstance(threshholdInput,float) == True or isinstance(threshholdInput,int) == True:
                    validInput = True
                else:
                    validInput = False
                itemSubWin.deleteln()
            
            addNewItem(iteminput,buyorsellinput,directionInput,threshholdInput)
            
            curses.noecho()
            
            pos = beginNum
            cursor = 0
            
            endNum = beginNum + displayLineLimit
            
            itemSubWin.clear()
            itemSubWin.border(0)
        
        ###################################
        #Deletes Watch Item at Cursor
        elif y == ord('d'):
            removeItem(cursor)
            pos = beginNum
            cursor = 0
            
            endNum = beginNum + displayLineLimit
            
            itemSubWin.clear()
            itemSubWin.border(0)
            
        elif y == ord("\n"):
            
            pos = beginNum
            itemSubWin.clear()
            itemSubWin.border(0)
  
def writeWatchList(watchList):
    fileHandler=open("WatchList.dat", 'w')
    for item in watchList:
        fileHandler.write(str(item.typeID) + "," + str(item.buyorsell) + "," + str(item.direction) + "," + str(item.threshhold) + "," + str(item.notified))
        fileHandler.write("\n")                
    fileHandler.close()
    return   

def readWatchList():
    #Loads the Descriptor for Each TypeID
    try:
        fileHandler = csv.reader(open("WatchList.dat", "rb"))
    except:
        print("No Previous Data..")
    else:
        for row in fileHandler:
            if row[2] == "0":
                direction = "<"
            elif row[2] == "1":
                direction = ">"
            addNewItem(typeidtoname(int(row[0])),str(row[1]),direction,float(row[3]))
    return
##############################
#Initial Setup
##############################
print("Reading Configuration...")
config = ConfigParser.RawConfigParser()
try:
    config.read('config.ini')
except:
    print("Error Reading config.ini.")
    sys.exit()

consumer_key = config.get('Twitter','consumer_key')
consumer_secret = config.get('Twitter','consumer_secret')
access_token = config.get('Twitter','access_token')
access_token_secret = config.get('Twitter','access_token_secret')
twitterName = config.get('Twitter','twitterName')

if consumer_key == "CHANGE_ME" or consumer_secret == "CHANGE_ME" or access_token == "CHANGE_ME" or access_token_secret == "CHANGE_ME" or twitterName == "CHANGE_ME":
    print("Twitter API not setup. Please check the config.ini file!")
    sys.exit()


##########################
#Sets up OAuth for Twitter/Tweepy
##########################
print("Performing Twitter OAuth Setup...")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)     
              
#############################       
#Begin Alert Program Setup
#############################
watchList = watchListClass()
typeIDs = loadtypeids()
readWatchList()

previousMarketData = []

#############################
#Load Initial Screen
#############################
screen = initMainWindow()


#############################
#Handle Main Menu Choices
#############################
choice = 99
while choice != str(3):
    
    choice = mainMenu(screen)
    
    if choice == str(1):
        watchDataMenu(screen)
        writeWatchList(watchList.listing)
        choice = 99
        
    if choice == str(2):
        monitorDataMenu(screen)
        choice = 99
        
    if choice == str(3):
        print 
        #Load 3

#############################
#Ending Program Cleanup
#############################
curses.nocbreak() 
screen.keypad(0)
curses.echo()
curses.endwin()
