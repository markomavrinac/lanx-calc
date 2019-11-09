import tkinter as tk
from tkinter import ttk

class simpleapp_tk(tk.Tk):
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
    def makeWeight(self,object,iterations):
        for i in range(iterations):
            object.columnconfigure(i,weight=1)
    def processInput(self,digit):
        if len(digit)==1:
            return int(digit)
        elif digit[0]==0:
            return int(digit[1])
        else:
            return int(digit)
    def processOutput(self,digit):
        digit=str(digit)
        if len(digit)==1:
            return "0"+digit
        else:
            return str(digit)
    def loadUni(self, path): #loads preset for uni settings (uni speed, number of galaxies, donut properties)
        source = open(path, 'r')
        raw = source.readlines()
        source.close()
        for commandLine in raw:
            command, parameter = commandLine.split()
            if command == "speed":
                self.uniSpeedCombo.set(int(parameter))
            elif command == "galaxies":
                self.numberofGalaxiesCombo.set(int(parameter))
            elif command == "donutgalaxy":
                if int(parameter)==1:
                    self.donutGalaxyCheck.select()
                elif int(parameter)==0:
                    self.donutGalaxyCheck.deselect()
            elif command == "donutsystem":
                if int(parameter)==1:
                    self.donutSystemCheck.select()
                elif int(parameter)==0:
                    self.donutSystemCheck.deselect()
    def saveUni(self, instance = 0): #instance is just so method can be called from bind, I don't need it
        uniSpeed = str(self.uniSpeedCombo.get())
        numberofGalaxies = str(self.numberofGalaxiesCombo.get())
        if self.donutGalaxyVar.get():
            donutGalaxy = "1"
        else:
            donutGalaxy = "0"
        if self.donutSystemVar.get():
            donutSystem = "1"
        else:
            donutSystem = "0"
        settings = "speed %s\ngalaxies %s\ndonutgalaxy %s\ndonutsystem %s"%(uniSpeed,numberofGalaxies,donutGalaxy,donutSystem)
        
        output = open("preset.ini","w")
        output.write(settings)
        output.close()

        
    def processRecall(self,digit):
        if len(digit)==0:
            return 0
        else:
            return int(digit)
    def calculate(self):
        self.combo = int(self.combustionEntry.get())
        self.impulse = int(self.impulseEntry.get())
        self.hyper = int(self.hyperEntry.get())
        drives = [self.combo,self.impulse,self.hyper]
        self.uniSpeed = int(self.uniSpeedCombo.get())
        self.donutGalaxy = self.donutGalaxyVar.get()
        self.donutSystem = self.donutSystemVar.get()
        self.numberOfGalaxies = int(self.numberofGalaxiesCombo.get())
        self.travelSpeed = int(self.assumedSpeedCombo.get())
        ships = createShips(drives)
        origin = [int(self.fromGalaxyText.get()),int(self.fromSolarText.get()),int(self.fromSlotText.get())]
        destination = [int(self.toGalaxyText.get()),int(self.toSolarText.get()),int(self.toSlotText.get())]
        distance1 = Distance(origin, destination, self.donutGalaxy,self.donutSystem,self.numberOfGalaxies)
        for i in range(len(ships)):
            if ships[i].name==self.slowestShipCombo.get():
                ship = ships[i]
        travelTime = TravelTime(ship,distance1,self.travelSpeed,self.uniSpeed)
        arrivalTime = [self.processInput(self.hourArrival.get()),self.processInput(self.minuteArrival.get()),self.processInput(self.secondArrival.get())]
        if len(self.scanDelayEntry.get())==0:
            scanDelay = 0
        else:
            scanDelay = int(self.scanDelayEntry.get())
        recallTime = [self.processRecall(self.recallHourEntry.get()),self.processRecall(self.recallMinuteEntry.get()),self.processRecall(self.recallSecondEntry.get())] #SERVER TIME, NOT ETA
        if recallTime == [0,0,0]: #making sure it doesn't make double return times on definite recalls like when fleet reaches planet
            recallTime = False
        returnTime = travelTime.getReturnTime(arrivalTime, scanDelay, recallTime)
        
        #assembling report
        self.speedContent.configure(text=str(ship.getSpeed()))
        self.distanceContent.configure(text =str(distance1.getDistance()))
        self.travelTimeContent.configure(text=self.processOutput(travelTime.getFlightTime()[0])+":"+self.processOutput(travelTime.getFlightTime()[1])+":"+self.processOutput(travelTime.getFlightTime()[2]))
        if len(returnTime)==3: #this is single return time because it's being returned as a list so its len is 3 for hh mm ss
            self.returnTimeContent.configure(text=self.processOutput(returnTime[0])+":"+self.processOutput(returnTime[1])+":"+self.processOutput(returnTime[2]))
        elif len(returnTime)==2: #double return time as it's a tuple of lists
            self.returnTimeContent.configure(text=self.processOutput(returnTime[0][0])+":"+self.processOutput(returnTime[0][1])+":"+self.processOutput(returnTime[0][2])+" - "+self.processOutput(returnTime[1][0])+":"+self.processOutput(returnTime[1][1])+":"+self.processOutput(returnTime[1][2]))
            
    def initialize(self):
        maxColumns = 20
        self.grid()
        self.makeWeight(self,maxColumns)
        #self.entry.bind("<Return>", self.OnPressEnter)
        titleLabel = tk.Label(self, justify=tk.CENTER, text = "LanxCalc by Savage")
        titleLabel.grid(row=0,column=0,columnspan=maxColumns)
        #frame with origin and destination coordinates
        coordinateFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth = 2)
        self.makeWeight(coordinateFrame,maxColumns)
        coordinateLabel = tk.Label(coordinateFrame,justify = tk.CENTER, text ="Destination Coordinates and Arrival Time")
        coordinateLabel.grid(row=0,column=0,columnspan=maxColumns)        
        coordinateFrame.grid(row=2,column=0,columnspan=maxColumns,sticky = 'NSEW')
        arrivalLabel = tk.Label(coordinateFrame, justify = tk.CENTER, text = "Arrival Time:")
        arrivalLabel.grid(row=1,column=0,columnspan=int(maxColumns/4))
        self.hourArrival = tk.Entry(coordinateFrame,justify = tk.CENTER,width=10)
        self.hourArrival.grid(row=1,column=5,columnspan=int(maxColumns/4))
        self.minuteArrival = tk.Entry(coordinateFrame,justify = tk.CENTER,width=10)
        self.minuteArrival.grid(row=1,column=10,columnspan=int(maxColumns/4))
        self.secondArrival = tk.Entry(coordinateFrame,justify = tk.CENTER,width=10)
        self.secondArrival.grid(row=1,column=15,columnspan=int(maxColumns/4)) 
        toLabel = tk.Label(coordinateFrame, justify = tk.CENTER, text = "Coordinates:")
        toLabel.grid(row=2,column=0,columnspan = 5)        
        self.toGalaxyText = tk.Entry(coordinateFrame,justify = tk.CENTER,width=10)
        self.toGalaxyText.grid(row=2,column=5,columnspan=int(maxColumns/4))
        self.toGalaxyText.insert(0,"1")
        self.toSolarText = tk.Entry(coordinateFrame,justify = tk.CENTER,width=10)
        self.toSolarText.grid(row=2,column=10,columnspan=int(maxColumns/4))
        self.toSolarText.insert(0,"1")
        self.toSlotText = tk.Entry(coordinateFrame,justify = tk.CENTER,width=10)
        self.toSlotText.grid(row=2,column=15,columnspan=int(maxColumns/4)) 
        self.toSlotText.insert(0,"1")
        #UNI OPTIONS
        uniOptionFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth = 2)
        uniOptionFrame.grid(row=3,column=0,columnspan=maxColumns,sticky='NSEW')
        self.makeWeight(uniOptionFrame,maxColumns)
        uniLabel = tk.Label(uniOptionFrame,justify = tk.CENTER, text = "Universe Settings")
        uniSpeedLabel = tk.Label(uniOptionFrame,justify = tk.CENTER, text = "Uni Speed:")
        uniLabel.grid(row=0,column=0,columnspan=maxColumns)
        uniSpeedLabel.grid(row=1,column=0,columnspan = int(maxColumns/2),sticky='E')
        self.uniSpeedCombo = ttk.Combobox(uniOptionFrame, values = [1,2,3,4,5,6],width=5,state="readonly",justify = tk.CENTER) #OPTION
        self.uniSpeedCombo.bind("<<ComboboxSelected>>", self.saveUni)
        self.uniSpeedCombo.grid(row=1,column=10,columnspan = int(maxColumns/2),sticky='W')
        self.uniSpeedCombo.set(1)
        numberOfGalaxiesLabel = tk.Label(uniOptionFrame,justify = tk. CENTER, text = "Number of galaxies:")
        numberOfGalaxiesLabel.grid(row=2,column=0,columnspan=int(maxColumns/2),sticky='E')
        self.numberofGalaxiesCombo = ttk.Combobox(uniOptionFrame, values = [1,2,3,4,5,6,7,8,9], width = 5, state = 'readonly', justify = tk.CENTER) #OPTION
        self.numberofGalaxiesCombo.bind("<<ComboboxSelected>>", self.saveUni)
        self.numberofGalaxiesCombo.set(9)
        self.numberofGalaxiesCombo.grid(row=2,column=10,columnspan=int(maxColumns/2),sticky='W')
        donutGalaxyLabel = tk.Label(uniOptionFrame, justify = tk.CENTER, text = "Donut Galaxy")
        donutGalaxyLabel.grid(row=3,column=0,columnspan=int(maxColumns/2),sticky = 'E')
        self.donutGalaxyVar = tk.IntVar()
        self.donutGalaxyCheck = tk.Checkbutton(uniOptionFrame,var = self.donutGalaxyVar,command = self.saveUni) #OPTION
        self.donutGalaxyCheck.select()
        self.donutGalaxyCheck.grid(row=3,column=10,columnspan=int(maxColumns/2),sticky='W')
        donutSystemLabel = tk.Label(uniOptionFrame, justify = tk.CENTER, text = "Donut System")
        donutSystemLabel.grid(row=4,column=0,columnspan=int(maxColumns/2),sticky = 'E')
        self.donutSystemVar = tk.IntVar()
        self.donutSystemCheck = tk.Checkbutton(uniOptionFrame, var = self.donutSystemVar,command = self.saveUni) #OPTION
        self.donutSystemCheck.select()
        self.donutSystemCheck.grid(row=4,column=10,columnspan=int(maxColumns/2),sticky='W')
        #DEFAULTS SET WHEN CREATING OBJECTS, NOW WE TRY TO LOAD FROM THE INI FILE
        self.loadUni("preset.ini")
        
        #PLAYER INFO
        playerInfoFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth = 2)
        playerInfoFrame.grid(row=4,column=0,columnspan=maxColumns,sticky = 'NSEW')
        self.makeWeight(playerInfoFrame,maxColumns)
        playerInfoLabel = tk.Label(playerInfoFrame,justify = tk.CENTER,text = "Player Info")
        playerInfoLabel.grid(row=0,column=0,columnspan = maxColumns)
        combustionLabel = tk.Label(playerInfoFrame,justify = tk.CENTER, text = "Combustion Drive:")
        combustionLabel.grid(row=1,column=0,columnspan = int(maxColumns/2),sticky = 'E')
        self.combustionEntry = tk.Entry(playerInfoFrame,justify = tk.CENTER, width = 10)
        self.combustionEntry.grid(row=1,column=10,columnspan = int(maxColumns/2),sticky = 'W')
        impulseLabel = tk.Label(playerInfoFrame,justify = tk.CENTER, text = "Impulse Drive:")
        impulseLabel.grid(row=2,column=0,columnspan = int(maxColumns/2),sticky = 'E')
        self.impulseEntry = tk.Entry(playerInfoFrame,justify = tk.CENTER, width = 10)
        self.impulseEntry.grid(row=2,column=10,columnspan = int(maxColumns/2),sticky = 'W')
        hyperLabel = tk.Label(playerInfoFrame,justify = tk.CENTER, text = "Hyperspace Drive:")
        hyperLabel.grid(row=3,column=0,columnspan = int(maxColumns/2),sticky = 'E')
        self.hyperEntry = tk.Entry(playerInfoFrame,justify = tk.CENTER, width = 10)
        self.hyperEntry.grid(row=3,column=10,columnspan = int(maxColumns/2),sticky = 'W')
        #FLEET INFO
        fleetFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth = 2)
        fleetFrame.grid(row=5, column=0, columnspan=maxColumns,sticky = 'NSEW')
        self.makeWeight(fleetFrame,maxColumns)
        fleetLabel = tk.Label(fleetFrame,justify=tk.CENTER, text = "Fleet and origin coordinates")
        fleetLabel.grid(row=0,column=0,columnspan=maxColumns)
        toLabel = tk.Label(fleetFrame, justify = tk.CENTER, text = "Coordinates:")
        toLabel.grid(row=1,column=0,columnspan = 5)        
        self.fromGalaxyText = tk.Entry(fleetFrame,justify = tk.CENTER,width=10)
        self.fromGalaxyText.grid(row=1,column=5,columnspan=int(maxColumns/4))
        self.fromGalaxyText.insert(0,"1")
        self.fromSolarText = tk.Entry(fleetFrame,justify = tk.CENTER,width=10)
        self.fromSolarText.grid(row=1,column=10,columnspan=int(maxColumns/4))
        self.fromSolarText.insert(0,"1")
        self.fromSlotText = tk.Entry(fleetFrame,justify = tk.CENTER,width=10)
        self.fromSlotText.grid(row=1,column=15,columnspan=int(maxColumns/4)) 
        self.fromSlotText.insert(0,"1")
        slowestShipLabel = tk.Label(fleetFrame, justify = tk.CENTER, text = "Slowest ship in fleet:")
        slowestShipLabel.grid(row=2,column=0,columnspan = int(maxColumns/2),sticky = 'E')
        self.slowestShipCombo = ttk.Combobox(fleetFrame, values = ["Small Cargo","Large Cargo", "Light Fighter", "Heavy Fighter", "Cruiser", "Battleship", "Colony Ship", "Recycler", "Bomber", "Destroyer","Deathstar", "Battlecruiser"],state = "readonly",width=12,justify = tk.CENTER)
        self.slowestShipCombo.grid(row=2,column = 10,columnspan = int(maxColumns/2),sticky='W')
        assumedSpeedLabel = tk.Label(fleetFrame,justify = tk.CENTER, text = "Assumed speed:")
        assumedSpeedLabel.grid(row=3,column=0,columnspan=int(maxColumns/2),sticky='E')
        self.assumedSpeedCombo = ttk.Combobox(fleetFrame, values = [100,90,80,70,60,50,40,30,20,10],state="readonly",width=12,justify = tk.CENTER)
        self.assumedSpeedCombo.grid(row=3,column=10,columnspan=int(maxColumns/2),sticky='W')
        self.assumedSpeedCombo.set(100)
        recallLabel = tk.Label(fleetFrame,justify=tk.CENTER, text = "Recall server time:")
        recallLabel.grid(row=4,column=0,columnspan=8,sticky='E')
        self.recallHourEntry = tk.Entry(fleetFrame,justify = tk.CENTER,width=6)
        self.recallHourEntry.grid(row=4,column=8,columnspan=4,sticky='W')
        self.recallMinuteEntry = tk.Entry(fleetFrame,justify = tk.CENTER,width=6)
        self.recallMinuteEntry.grid(row=4,column=12,columnspan=4,sticky='W')
        self.recallSecondEntry = tk.Entry(fleetFrame,justify = tk.CENTER,width=6)
        self.recallSecondEntry.grid(row=4,column=16,columnspan=4,sticky='W')
        scanDelayLabel = tk.Label(fleetFrame, justify = tk.CENTER, text = "Time between scans:")
        scanDelayLabel.grid(row=6,column=0,columnspan=int(maxColumns/2),sticky ='E')
        self.scanDelayEntry = tk.Entry(fleetFrame, justify = tk.CENTER,width=10)
        self.scanDelayEntry.grid(row=6,column=10,columnspan=int(maxColumns/2),sticky='W')
        resultFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth = 2)
        resultFrame.grid(row=7,column=0,columnspan=maxColumns,sticky='NSEW')
        self.makeWeight(resultFrame,maxColumns)
        speedCaption = tk.Label(resultFrame, justify = tk.CENTER, text = "Speed:")
        speedCaption.grid(row=0,column=0,columnspan=int(maxColumns/2),sticky='E')
        self.speedContent = tk.Label(resultFrame, justify = tk.CENTER, text = "(not calculated)")
        self.speedContent.grid(row=0,column=10,columnspan=(int(maxColumns/2)),sticky='W')
        distanceCaption = tk.Label(resultFrame, justify = tk.CENTER, text = "Distance:")
        distanceCaption.grid(row=1,column=0,columnspan=int(maxColumns/2),sticky='E')
        self.distanceContent = tk.Label(resultFrame, justify = tk.CENTER, text = "(not calculated)")
        self.distanceContent.grid(row=1,column=10,columnspan=(int(maxColumns/2)),sticky='W')        
        travelTimeCaption = tk.Label(resultFrame, justify =tk.CENTER, text = "Travel time (one way):")
        travelTimeCaption.grid(row=2,column=0,columnspan=int(maxColumns/2), sticky = 'E')
        self.travelTimeContent = tk.Label(resultFrame,justify = tk.CENTER, text = "(not calculated)")
        self.travelTimeContent.grid(row=2,column=10,columnspan=int(maxColumns/2),sticky='W')
        returnTimeCaption = tk.Label(resultFrame, justify = tk.CENTER, text = "Return time:")
        returnTimeCaption.grid(row=3,column=0,columnspan=maxColumns)
        self.returnTimeContent = tk.Label(resultFrame, justify = tk.CENTER, text = "(not calculated)")
        self.returnTimeContent.grid(row=4,column=0,columnspan=maxColumns)
        calculateButton = tk.Button(self,justify=tk.CENTER, text = "Calculate",command=self.calculate)
        calculateButton.grid(row=8,column=0,columnspan=maxColumns)
        
        
        
        
"""
combo = 14
impulse = 13
hyper = 12
donutGalaxy = True
donutSystem = True
numberOfGalaxies = 4
travelSpeed = 100
uniSpeed = 6   ->this is just for reference and was used for testing
"""
class Ship(object):
    def __init__(self, name, baseSpeed, drive, drives):
        self.name = name
        self.baseSpeed = baseSpeed
        self.drive = drive
        self.combo = drives[0]
        self.impulse = drives[1]
        self.hyper = drives[2]
        if self.name == "Small Cargo" and self.impulse>=5:
            self.drive = "Impulse"
            self.baseSpeed = 10000
        if self.name == "Recycler" and self.impulse>=17:
            self.drive == "Impulse"
            self.baseSpeed = 4000
        
        if self.name == "Bomber" and self.hyper>=8:
            self.drive = "Hyper"
            self.baseSpeed = 5000
        if self.name == "Recycler" and self.hyper>=15:
            self.drive = "Hyper"
            self.baseSpeed = 6000
        
        if self.drive == "Combustion":
            self.multiplier = 0.1
        elif self.drive == "Impulse":
            self.multiplier = 0.2
        elif self.drive == "Hyper":
            self.multiplier = 0.3
        
        self.speed = round(self.baseSpeed*(1+self.multiplier*self.getDriveLevel(self.drive)))
    def getDriveLevel(self,drive):
        if drive == "Combustion":
            return self.combo
        elif drive == "Impulse":
            return self.impulse
        elif drive == "Hyper":
            return self.hyper

    def getSpeed(self):
        return int(self.speed)
    
class Distance(object):
    def __init__(self, origin, destination,donutGalaxy,donutSystem,numberOfGalaxies): #[3 244 15], [2 424 12]
        self.rawCoords1 = origin
        self.rawCoords2 = destination
        self.galaxy1 = origin[0]
        self.solar1 = origin[1]
        self.slot1 = origin[2]
        self.galaxy2 = destination[0]
        self.solar2 =  destination[1]
        self.slot2 = destination[2]
        self.donutGalaxy = donutGalaxy
        self.donutSystem = donutSystem
        self.numberOfGalaxies = numberOfGalaxies
    def __moonToPlanet(self):
        return 5
    def __inSystem(self, slot1, slot2):
        
        return 1000+5*abs(slot2-slot1)
    def __inGalaxy(self,solar1,solar2):
        if not self.donutSystem:
            return 2700+(95*(abs(solar2-solar1)))
        else:
            route1 = abs(solar2-solar1)
            route2 = 499 - route1
            difference = min(route1,route2)
            return 2700+(95*difference)
    def __crossGalaxy(self,galaxy1,galaxy2):
        if not self.donutGalaxy:
            return 20000*abs(galaxy2-galaxy1)
        else:
            route1 = abs(galaxy2-galaxy1)
            route2 = self.numberOfGalaxies - route1
            difference = min(route1,route2)
            return 20000*abs(difference)
    def getDistance(self):
        if self.rawCoords1==self.rawCoords2:
            return self.__moonToPlanet()
        elif (self.galaxy1 == self.galaxy2) and (self.solar1==self.solar2):
            return self.__inSystem(self.slot1,self.slot2)
        elif self.galaxy1 == self.galaxy2:
            return self.__inGalaxy(self.solar1,self.solar2)
        else:
            return self.__crossGalaxy(self.galaxy1,self.galaxy2)
        
class TravelTime(object):
    def __init__(self, ship, distance, flightSpeed, uniSpeed):
        self.ship = ship
        self.distance = distance
        self.flightSpeed = flightSpeed
        self.uniSpeed = uniSpeed
    def getFlightTime(self):
        timeInSeconds = round(((35000/self.flightSpeed)*(self.distance.getDistance()*1000/self.ship.getSpeed())**(0.5)+10)/self.uniSpeed)
        hours = int(str(timeInSeconds/3600).split(".")[0])
        remainder = timeInSeconds-hours*3600
        minutes = int(str(remainder/60).split(".")[0])
        seconds = remainder - minutes*60
        return hours, minutes, seconds
    def getReturnTime(self,arrivalTime, delay, recallTime):
        flightTime = self.getFlightTime()
        returnTimeSeconds = arrivalTime[2]+flightTime[2]
        returnTimeMinutes = arrivalTime[1]+flightTime[1]
        returnTimeHours = arrivalTime[0]+flightTime[0]
        if returnTimeSeconds>=60:
            returnTimeMinutes+=1
            returnTimeSeconds-=60
        if returnTimeMinutes>=60:
            returnTimeHours+=1
            returnTimeMinutes -= 60
        while returnTimeHours>=24:
            returnTimeHours -= 24
        if recallTime==False:
            return [returnTimeHours,returnTimeMinutes,returnTimeSeconds]
        else:
            recallIntervalHours = arrivalTime[0]-recallTime[0]
            recallIntervalMinutes = arrivalTime[1]-recallTime[1]
            recallIntervalSeconds = arrivalTime[2]-recallTime[2]
            
            if recallIntervalSeconds<0:
                recallIntervalSeconds+=60
                recallIntervalMinutes-=1
            if recallIntervalMinutes<0:
                recallIntervalHours-=1
                recallIntervalMinutes+=60
            #latest possible return time
            returnTimeSeconds -= recallIntervalSeconds*2
            returnTimeMinutes -= recallIntervalMinutes*2
            returnTimeHours -= recallIntervalHours*2
            
            while returnTimeSeconds<0:
                returnTimeMinutes-=1
                returnTimeSeconds+=60
            while returnTimeMinutes<0:
                returnTimeHours-=1
                returnTimeMinutes+=60
            while returnTimeHours<0:
                returnTimeHours+=24
            lateRecallTime = [returnTimeHours,returnTimeMinutes,returnTimeSeconds]
            
            earlyRecallTimeSeconds = lateRecallTime[2] - 2*delay
            earlyRecallTimeMinutes = lateRecallTime[1]
            earlyRecallTimeHours = lateRecallTime[0]
            
            while earlyRecallTimeSeconds<0:
                earlyRecallTimeMinutes-=1
                earlyRecallTimeSeconds+=60
            while earlyRecallTimeMinutes<0:
                earlyRecallTimeHours-=1
                earlyRecallTimeMinutes+=60
            while earlyRecallTimeHours<0:
                earlyRecallTimeHours+=24
            earlyRecallTime = [earlyRecallTimeHours,earlyRecallTimeMinutes,earlyRecallTimeSeconds]
            
            return (earlyRecallTime,lateRecallTime)
    
                
        
        
def createShips(drives):
    sc = Ship("Small Cargo", 5000, "Combustion",drives)
    lc = Ship("Large Cargo", 7500, "Combustion",drives)
    lf = Ship("Light Fighter", 12500, "Combustion",drives)
    hf = Ship("Heavy Fighter", 10000, "Impulse",drives)
    cru = Ship("Cruiser", 15000, "Impulse",drives)
    bs = Ship("Battleship", 10000, "Hyper",drives)
    colo = Ship("Colony Ship", 2500, "Impulse",drives)
    rec = Ship("Recycler", 2000, "Combustion",drives)
    bomb = Ship("Bomber", 4000, "Impulse",drives)
    des = Ship("Destroyer", 5000, "Hyper",drives)
    rip = Ship("Deathstar", 100, "Hyper",drives)
    bc = Ship("Battlecruiser", 10000, "Hyper",drives)
    return [sc,lc,lf,hf,cru,bs,colo,rec,bomb,des,rip,bc]

"""
coord1 = [3,105,8]
coord2 = [3,62,8]
distance1 = Distance(coord1,coord2,donutGalaxy,donutSystem,numberOfGalaxies)
trtime1=TravelTime(sc,distance1, travelSpeed, uniSpeed)
print(trtime1.getFlightTime())
arrivalTime = [18,3,56]
print(trtime1.getReturnTime(arrivalTime,3,[17,58,56])) -> also just for reference
"""

#LOGIC#########

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('LanxCalc')
    app.mainloop()
