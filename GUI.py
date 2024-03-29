
"""

               
datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

    The year, month and day arguments are required. tzinfo may be None, or an
    instance of a tzinfo subclass. The remaining arguments may be ints.
    """   
version = "1.0.1"
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime as dt
import pyperclip
class LanxCalc(tk.Tk):
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
    def getBoostRange(self, maxValue, increment): #just so I don't have to dig manually through the code if limits turn out to be different
        output = []
        assert(maxValue>increment)
        currentValue = increment
        while currentValue<=maxValue:
            if int(currentValue)!=currentValue:
                output.append(currentValue)
            else:
                output.append(int(currentValue)) #avoiding 1.0 etc
            currentValue+=increment
        return output
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
            elif command == "collectorboost":
                parameter = float(parameter) #can't directly translate float string to int :(
                if int(parameter) == parameter:
                    self.collectorBoostCombo.set(int(parameter))
                else:
                    self.collectorBoostCombo.set(float(parameter))
            elif command == "generalboost":
                parameter = float(parameter)
                if int(parameter) == parameter:
                    self.generalBoostCombo.set(int(parameter))
                else:
                    self.generalBoostCombo.set(float(parameter))
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
        collectorBoost = str(self.collectorBoostCombo.get())
        generalBoost = str(self.generalBoostCombo.get())
        settings = "speed %s\ngalaxies %s\ndonutgalaxy %s\ndonutsystem %s\ncollectorboost %s\ngeneralboost %s"%(uniSpeed,numberofGalaxies,donutGalaxy,donutSystem,collectorBoost,generalBoost)
        
        output = open("preset.ini","w")
        output.write(settings)
        output.close()

        
    def processRecall(self,digit):
        if len(digit)==0:
            return 0
        else:
            return int(digit)
    def getReport(self):
        self.calculate(report=True)
    def calculate(self,report = False):
        try:
            self.combo = int(self.combustionEntry.get())
            self.impulse = int(self.impulseEntry.get())
            self.hyper = int(self.hyperEntry.get())
        except:
            messagebox.showinfo("Bad input", "Drive levels invalid!")
            return
        if self.classCombo.get() == "":
            messagebox.showinfo("Bad input", "Player class not selected!")
            return #don't want multiple pesky messageboxes at once, do we?
        drives = [self.combo,self.impulse,self.hyper]
        self.uniSpeed = int(self.uniSpeedCombo.get())
        self.donutGalaxy = self.donutGalaxyVar.get()
        self.donutSystem = self.donutSystemVar.get()
        self.numberOfGalaxies = int(self.numberofGalaxiesCombo.get())
        self.travelSpeed = int(self.assumedSpeedCombo.get())
        ships = createShips(drives)
        try:
            origin = [int(self.fromGalaxyText.get()),int(self.fromSolarText.get()),int(self.fromSlotText.get())]
        except:
            messagebox.showinfo("Bad input", "Origin coordinates invalid!")
            return
        try:
            destination = [int(self.toGalaxyText.get()),int(self.toSolarText.get()),int(self.toSlotText.get())]
        except:
            messagebox.showinfo("Bad input", "Destination coordinates invalid!")
            return
        distance1 = Distance(origin, destination, self.donutGalaxy,self.donutSystem,self.numberOfGalaxies)
        ship = False #kinda crappy patch for recognizing if ship wasn't selected, gonna try format it better in the future
        for i in range(len(ships)):
            if ships[i].name==self.slowestShipCombo.get():
                ship = ships[i]
        if not ship:
            messagebox.showinfo("Bad input", "Slowest ship not selected!")
            return
        travelTime = TravelTime(ship,distance1,self.travelSpeed,self.uniSpeed)
        try:
            arrivalTime = [self.processInput(self.yearArrival.get()),self.processInput(self.monthArrival.get()),self.processInput(self.dayArrival.get()),self.processInput(self.hourArrival.get()),self.processInput(self.minuteArrival.get()),self.processInput(self.secondArrival.get())]
        except:
            messagebox.showinfo("Bad input", "Arrival time invalid!")
            return
        if len(self.scanDelayEntry.get())==0:
            scanDelay = 0
        else:
            try:
                scanDelay = int(self.scanDelayEntry.get())
            except:
                messagebox.showinfo("Bad input", "Scan delay invalid!")
                return
        try:
            recallTime = [self.processRecall(self.recallYearEntry.get()),self.processRecall(self.recallMonthEntry.get()),self.processRecall(self.recallDayEntry.get()),self.processRecall(self.recallHourEntry.get()),self.processRecall(self.recallMinuteEntry.get()),self.processRecall(self.recallSecondEntry.get())] #SERVER TIME, NOT ETA
        except:
            messagebox.showinfo("Bad input", "Recall time invalid!")
            return
        if recallTime[3:6] == [0,0,0]: #making sure it doesn't make double return times on definite recalls like when fleet reaches planet
            recallTime = False
        returnTime = travelTime.getReturnTime(arrivalTime, scanDelay, recallTime)
        
        #assembling  GUI report
        if report == False:
            self.speedContent.configure(text=str(ship.getSpeed(self.classCombo.get())))
            self.distanceContent.configure(text =str(distance1.getDistance()))
            self.travelTimeContent.configure(text=self.processOutput(travelTime.getFlightTime()[0])+":"+self.processOutput(travelTime.getFlightTime()[1])+":"+self.processOutput(travelTime.getFlightTime()[2]))
            if len(returnTime)==6: #this is single return time because it's being returned as a list so its len is 3 for hh mm ss
                self.returnTimeContent.configure(text="[" +self.processOutput(returnTime[0])+"/"+self.processOutput(returnTime[1])+"/"+self.processOutput(returnTime[2])+ "] " + self.processOutput(returnTime[3])+":"+self.processOutput(returnTime[4])+":"+self.processOutput(returnTime[5]))
            elif len(returnTime)==2: #double return time as it's a tuple of lists
                self.returnTimeContent.configure(text="["+self.processOutput(returnTime[0][0])+"/"+self.processOutput(returnTime[0][1])+"/"+self.processOutput(returnTime[0][2])+ "]" + " " +self.processOutput(returnTime[0][3]) + ":" +self.processOutput(returnTime[0][4]) + ":" +self.processOutput(returnTime[0][5]) + " - " +self.processOutput(returnTime[1][3]) + ":" +self.processOutput(returnTime[1][4])+":"+self.processOutput(returnTime[1][5]))
        else:
            #assembling clipboard detailed report
            output = ("Target is returning from [%s %s %s] and landing to [%s %s %s]\n"%(self.toGalaxyText.get(),self.toSolarText.get(),self.toSlotText.get(),self.fromGalaxyText.get(),self.fromSolarText.get(),self.fromSlotText.get())).center(40, " ")
            while int(self.travelSpeed)>=10:
                travelTime = TravelTime(ship,distance1,self.travelSpeed,self.uniSpeed)
                try:
                    arrivalTime = [self.processInput(self.yearArrival.get()),self.processInput(self.monthArrival.get()),self.processInput(self.dayArrival.get()),self.processInput(self.hourArrival.get()),self.processInput(self.minuteArrival.get()),self.processInput(self.secondArrival.get())]
                except:
                    messagebox.showinfo("Bad input", "Arrival time invalid!")
                    return
                if len(self.scanDelayEntry.get())==0:
                    scanDelay = 0
                else:
                    try:
                        scanDelay = int(self.scanDelayEntry.get())
                    except:
                        messagebox.showinfo("Bad input", "Scan delay invalid!")
                        return
                try:
                    recallTime = [self.processRecall(self.recallYearEntry.get()),self.processRecall(self.recallMonthEntry.get()),self.processRecall(self.recallDayEntry.get()),self.processRecall(self.recallHourEntry.get()),self.processRecall(self.recallMinuteEntry.get()),self.processRecall(self.recallSecondEntry.get())] #SERVER TIME, NOT ETA
                except:
                    messagebox.showinfo("Bad input", "Recall time invalid!")
                    return
                if recallTime[3:6] == [0,0,0]: #making sure it doesn't make double return times on definite recalls like when fleet reaches planet
                    recallTime = False
                returnTime = travelTime.getReturnTime(arrivalTime, scanDelay, recallTime)                
                if len(returnTime)==6: 
                    output+= ("                    (%s%%) [%s/%s/%s] %s:%s:%s\n"%(str(self.travelSpeed),self.processOutput(returnTime[0]),self.processOutput(returnTime[1]),self.processOutput(returnTime[2]),self.processOutput(returnTime[3]),self.processOutput(returnTime[4]),self.processOutput(returnTime[5])))
                        
                    #output+=("("+str(self.travelSpeed)+"%) "+"[" +self.processOutput(returnTime[0])+"/"+self.processOutput(returnTime[1])+"/"+self.processOutput(returnTime[2])+ "] " + self.processOutput(returnTime[3])+":"+self.processOutput(returnTime[4])+":"+self.processOutput(returnTime[5])+"\n").center(40, " ") #man I'd really string format this but after barely somehow assembling it I feel both ashamed and proud in the same time, will probably fixed in future versions 
                elif len(returnTime)==2: #double return time as it's a tuple of lists
                    output+= ("                    ("+str(self.travelSpeed)+"%) "+"["+self.processOutput(returnTime[0][0])+"/"+self.processOutput(returnTime[0][1])+"/"+self.processOutput(returnTime[0][2])+ "]" + " " +self.processOutput(returnTime[0][3]) + ":" +self.processOutput(returnTime[0][4]) + ":" +self.processOutput(returnTime[0][5]) + " - " +self.processOutput(returnTime[1][3]) + ":" +self.processOutput(returnTime[1][4])+":"+self.processOutput(returnTime[1][5])+"\n")
                self.travelSpeed-=10
            else:
                if recallTime and not recallTime[3:6]==[0,0,0]:
                    output+= "       (Considering a recall at [%s/%s/%s] %s:%s:%s)\n"%(self.recallDayEntry.get(),self.recallMonthEntry.get(),self.recallYearEntry.get(),self.recallHourEntry.get(),self.recallMinuteEntry.get(),self.recallSecondEntry.get())               
                output+=("    Combustion = %i | Impulse = %i | Hyperspace = %i\n"%(self.combo,self.impulse,self.hyper))
                output+=("                       Slowest ship: %s\n"%(ship.name))
                output+=("                          Player Class: %s\n"%(self.classCombo.get()))
                output+=("\n               Report generated with LanxCalc %s."%(version))
                pyperclip.copy(output)
                
    def initialize(self):
        maxColumns = 20
        self.grid()
        self.makeWeight(self,maxColumns)
        #frame with origin and destination coordinates
        coordinateFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth = 2)
        self.makeWeight(coordinateFrame,maxColumns)
        coordinateLabel = tk.Label(coordinateFrame,justify = tk.CENTER, text ="Coordinates and Arrival Time", font = ("Segoe UI",10,"bold"))
        coordinateLabel.grid(row=0,column=0,columnspan=maxColumns)        
        coordinateFrame.grid(row=2,column=0,columnspan=maxColumns,sticky = 'NSEW')
        arrivalLabel = tk.Label(coordinateFrame, justify = tk.CENTER, text = "Arrival Time:")
        arrivalLabel.grid(row=1,column=0,columnspan=5,sticky = 'E')
        arrivalFrame = tk.Frame(coordinateFrame,relief=tk.GROOVE,borderwidth = 2)
        arrivalFrame.grid(row=1,column=5,columnspan=15,sticky='WE')
        self.makeWeight(arrivalFrame,18)
        self.dayArrival = tk.Entry(arrivalFrame,justify = tk.CENTER,width=4)
        self.dayArrival.grid(row=0,column=0,columnspan=3)
        self.monthArrival = tk.Entry(arrivalFrame,justify = tk.CENTER,width=4)
        self.monthArrival.grid(row=0,column=3,columnspan=3)
        self.yearArrival = tk.Entry(arrivalFrame,justify = tk.CENTER,width=6)
        self.yearArrival.grid(row=0,column=6,columnspan=3)        
        self.hourArrival = tk.Entry(arrivalFrame,justify = tk.CENTER,width=4)
        self.hourArrival.grid(row=0,column=9,columnspan=3)
        self.minuteArrival = tk.Entry(arrivalFrame,justify = tk.CENTER,width=4)
        self.minuteArrival.grid(row=0,column=12,columnspan=3)
        self.secondArrival = tk.Entry(arrivalFrame,justify = tk.CENTER,width=4)
        self.secondArrival.grid(row=0,column=15,columnspan=3) 
        currentTime = dt.datetime.now()
        self.dayArrival.insert(0,str(currentTime.day))
        self.monthArrival.insert(0,str(currentTime.month))
        self.yearArrival.insert(0,str(currentTime.year))
        fromLabel = tk.Label(coordinateFrame, justify = tk.CENTER, text = "Origin:")
        fromLabel.grid(row=2,column=0,columnspan = 5)        
        self.fromGalaxyText = tk.Entry(coordinateFrame,justify = tk.CENTER,width=10)
        self.fromGalaxyText.grid(row=2,column=5,columnspan=int(maxColumns/4))
        self.fromGalaxyText.insert(0,"1")
        self.fromSolarText = tk.Entry(coordinateFrame,justify = tk.CENTER,width=10)
        self.fromSolarText.grid(row=2,column=10,columnspan=int(maxColumns/4))
        self.fromSolarText.insert(0,"1")
        self.fromSlotText = tk.Entry(coordinateFrame,justify = tk.CENTER,width=10)
        self.fromSlotText.grid(row=2,column=15,columnspan=int(maxColumns/4)) 
        self.fromSlotText.insert(0,"1")        
        toLabel = tk.Label(coordinateFrame, justify = tk.CENTER, text = "Destination:")
        toLabel.grid(row=3,column=0,columnspan = 5)
        self.toGalaxyText = tk.Entry(coordinateFrame,justify = tk.CENTER,width=10)
        self.toGalaxyText.grid(row=3,column=5,columnspan=int(maxColumns/4))
        self.toGalaxyText.insert(0,"1")
        self.toSolarText = tk.Entry(coordinateFrame,justify = tk.CENTER,width=10)
        self.toSolarText.grid(row=3,column=10,columnspan=int(maxColumns/4))
        self.toSolarText.insert(0,"1")
        self.toSlotText = tk.Entry(coordinateFrame,justify = tk.CENTER,width=10)
        self.toSlotText.grid(row=3,column=15,columnspan=int(maxColumns/4)) 
        self.toSlotText.insert(0,"1")
        #UNI OPTIONS
        uniOptionFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth = 2)
        uniOptionFrame.grid(row=3,column=0,columnspan=maxColumns,sticky='NSEW')
        self.makeWeight(uniOptionFrame,maxColumns)
        uniLabel = tk.Label(uniOptionFrame,justify = tk.CENTER, text = "Universe Settings", font = ("Segoe UI",10,"bold"))
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
        collectorBoostLabel = tk.Label(uniOptionFrame, justify = tk.CENTER, text = "Collector speed boost:")
        collectorBoostLabel.grid(row=5,column=0,columnspan=int(maxColumns/2), sticky = 'E')
        self.collectorBoostCombo = ttk.Combobox(uniOptionFrame, values = self.getBoostRange(1,0.25), state = 'readonly', justify = tk.CENTER, width = 4)
        self.collectorBoostCombo.grid(row=5,column=10,columnspan = int(maxColumns/2),sticky='W')
        self.collectorBoostCombo.set(0.25)
        self.collectorBoostCombo.bind("<<ComboboxSelected>>", self.saveUni)
        generalBoostLabel = tk.Label(uniOptionFrame, justify = tk.CENTER, text = "General speed boost:")
        generalBoostLabel.grid(row=6,column=0,columnspan=int(maxColumns/2), sticky = 'E')
        self.generalBoostCombo = ttk.Combobox(uniOptionFrame, values = self.getBoostRange(1,0.25), state = 'readonly', justify = tk.CENTER, width = 4)
        self.generalBoostCombo.grid(row=6,column=10,columnspan = int(maxColumns/2),sticky = 'W')
        self.generalBoostCombo.set(0.25)
        self.generalBoostCombo.bind("<<ComboboxSelected>>", self.saveUni)
        #DEFAULTS SET WHEN CREATING OBJECTS, NOW WE TRY TO LOAD FROM THE INI FILE
        self.loadUni("preset.ini")
        
        #PLAYER INFO
        playerInfoFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth = 2)
        playerInfoFrame.grid(row=4,column=0,columnspan=maxColumns,sticky = 'NSEW')
        self.makeWeight(playerInfoFrame,maxColumns)
        playerInfoLabel = tk.Label(playerInfoFrame,justify = tk.CENTER,text = "Player Info", font = ("Segoe UI",10,"bold"))
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
        self.classLabel = tk.Label(playerInfoFrame, justify = tk.CENTER, text = "Class:")
        self.classLabel.grid(row=4,column=0,columnspan=int(maxColumns/2), sticky = 'E')
        self.classCombo = ttk.Combobox(playerInfoFrame, values = ["Collector", "General", "Discoverer"], width = 10, state = 'readonly', justify = tk.CENTER)
        self.classCombo.grid(row=4, column = 10, columnspan = int(maxColumns/2), sticky = 'W')
        #FLEET INFO
        fleetFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth = 2)
        fleetFrame.grid(row=5, column=0, columnspan=maxColumns,sticky = 'NSEW')
        self.makeWeight(fleetFrame,maxColumns)
        fleetLabel = tk.Label(fleetFrame,justify=tk.CENTER, text = "Fleet", font = ("Segoe UI",10,"bold"))
        fleetLabel.grid(row=0,column=0,columnspan=maxColumns)
        slowestShipLabel = tk.Label(fleetFrame, justify = tk.CENTER, text = "Slowest ship in fleet:")
        slowestShipLabel.grid(row=2,column=0,columnspan = int(maxColumns/2),sticky = 'E')
        self.slowestShipCombo = ttk.Combobox(fleetFrame, values = ["Small Cargo","Large Cargo", "Light Fighter", "Heavy Fighter", "Cruiser", "Battleship", "Colony Ship", "Recycler", "Bomber", "Destroyer","Deathstar", "Battlecruiser", "Reaper", "Pathfinder"],state = "readonly",width=12,justify = tk.CENTER)
        self.slowestShipCombo.grid(row=2,column = 10,columnspan = int(maxColumns/2),sticky='W')
        assumedSpeedLabel = tk.Label(fleetFrame,justify = tk.CENTER, text = "Assumed speed:")
        assumedSpeedLabel.grid(row=3,column=0,columnspan=int(maxColumns/2),sticky='E')
        self.assumedSpeedCombo = ttk.Combobox(fleetFrame, values = [100,90,80,70,60,50,40,30,20,10],state="readonly",width=12,justify = tk.CENTER)
        self.assumedSpeedCombo.grid(row=3,column=10,columnspan=int(maxColumns/2),sticky='W')
        self.assumedSpeedCombo.set(100)
        recallLabel = tk.Label(fleetFrame,justify=tk.CENTER, text = "Recall time:")
        recallLabel.grid(row=4,column=0,columnspan=5)
        recallFrame=tk.Frame(fleetFrame,relief=tk.GROOVE,borderwidth = 2)
        recallFrame.grid(row=4,column=5,columnspan=15,sticky='WE')
        self.makeWeight(recallFrame,18)
        self.recallDayEntry = tk.Entry(recallFrame,justify = tk.CENTER,width=4)
        self.recallDayEntry.grid(row=0,column=0,columnspan=3)  
        self.recallMonthEntry = tk.Entry(recallFrame,justify = tk.CENTER,width=4)
        self.recallMonthEntry.grid(row=0,column=3,columnspan=3) 
        self.recallYearEntry = tk.Entry(recallFrame,justify = tk.CENTER,width=6)
        self.recallYearEntry.grid(row=0,column=6,columnspan=3)  
        self.recallDayEntry.insert(0,str(currentTime.day))
        self.recallMonthEntry.insert(0,str(currentTime.month))
        self.recallYearEntry.insert(0,str(currentTime.year))        
        self.recallHourEntry = tk.Entry(recallFrame,justify = tk.CENTER,width=4)
        self.recallHourEntry.grid(row=0,column=9,columnspan=3)
        self.recallMinuteEntry = tk.Entry(recallFrame,justify = tk.CENTER,width=4)
        self.recallMinuteEntry.grid(row=0,column=12,columnspan=3)
        self.recallSecondEntry = tk.Entry(recallFrame,justify = tk.CENTER,width=4)
        self.recallSecondEntry.grid(row=0,column=15,columnspan=3)
        scanDelayLabel = tk.Label(fleetFrame, justify = tk.CENTER, text = "Time between scans:")
        scanDelayLabel.grid(row=6,column=0,columnspan=int(maxColumns/2),sticky ='E')
        self.scanDelayEntry = tk.Entry(fleetFrame, justify = tk.CENTER,width=10)
        self.scanDelayEntry.grid(row=6,column=10,columnspan=int(maxColumns/2),sticky='W')
        resultFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth = 2)
        resultFrame.grid(row=7,column=0,columnspan=maxColumns,sticky='NSEW')
        self.makeWeight(resultFrame,maxColumns)
        speedCaption = tk.Label(resultFrame, justify = tk.CENTER, text = "Speed:", font = ("Segoe UI",10,"bold"))
        speedCaption.grid(row=0,column=0,columnspan=maxColumns)
        self.speedContent = tk.Label(resultFrame, justify = tk.CENTER, text = "(not calculated)", font = ("Segoe UI",11))
        self.speedContent.grid(row=1,column=0,columnspan=maxColumns)
        distanceCaption = tk.Label(resultFrame, justify = tk.CENTER, text = "Distance:", font = ("Segoe UI",10,"bold"))
        distanceCaption.grid(row=2,column=0,columnspan=maxColumns)
        self.distanceContent = tk.Label(resultFrame, justify = tk.CENTER, text = "(not calculated)", font = ("Segoe UI",11))
        self.distanceContent.grid(row=3,column=0,columnspan=maxColumns)        
        travelTimeCaption = tk.Label(resultFrame, justify =tk.CENTER, text = "Travel time (one way):", font = ("Segoe UI",10,"bold"))
        travelTimeCaption.grid(row=4,column=0,columnspan=maxColumns)
        self.travelTimeContent = tk.Label(resultFrame,justify = tk.CENTER, text = "(not calculated)", font = ("Segoe UI",11))
        self.travelTimeContent.grid(row=5,column=0,columnspan=maxColumns)
        returnTimeCaption = tk.Label(resultFrame, justify = tk.CENTER, text = "Return time:", font = ("Segoe UI",10,"bold"))
        returnTimeCaption.grid(row=6,column=0,columnspan=maxColumns)
        self.returnTimeContent = tk.Label(resultFrame, justify = tk.CENTER, text = "(not calculated)", font = ("Segoe UI",11))
        self.returnTimeContent.grid(row=7,column=0,columnspan=maxColumns)
        reportButton = tk.Button(self,justify=tk.CENTER, text = "Copy report",command=self.getReport, font = ("Segoe UI",10,"bold"))
        reportButton.grid(row=8,column=0,columnspan=6)
        calculateButton = tk.Button(self,justify=tk.CENTER, text = "Calculate",command=self.calculate, font = ("Segoe UI",10,"bold"))
        calculateButton.grid(row=8,column=6,columnspan=8,sticky="EW")
        
        
        
        
#LOGIC#########################
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
    def __init__(self, name, baseSpeed, drive, drives, shipType):
        self.name = name
        self.baseSpeed = baseSpeed
        self.drive = drive
        self.combo = drives[0]
        self.impulse = drives[1]
        self.hyper = drives[2]
        self.shipType = shipType
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
        
        
    def getDriveLevel(self,drive):
        if drive == "Combustion":
            return self.combo
        elif drive == "Impulse":
            return self.impulse
        elif drive == "Hyper":
            return self.hyper

    def getSpeed(self, playerClass):
        classBonus = 0
        if playerClass == "General":
            if (self.name == "Recycler" or self.shipType == "military") and self.name != "Deathstar":
                classBonus = float(app.generalBoostCombo.get()) #not quite sure why I get a string here (I explicitly add ints or floats in loadUni method), but hey! here's a shitty patch to work around it!
        elif playerClass == "Collector":
            if self.name == "Small Cargo" or self.name == "Large Cargo":
                classBonus = float(app.collectorBoostCombo.get())
        self.speed = round(self.baseSpeed*(classBonus + 1 + self.multiplier*self.getDriveLevel(self.drive)))
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
        timeInSeconds = round(((35000/self.flightSpeed)*(self.distance.getDistance()*1000/self.ship.getSpeed(app.classCombo.get()))**(0.5)+10)/self.uniSpeed)
        hours = int(str(timeInSeconds/3600).split(".")[0])
        remainder = timeInSeconds-hours*3600
        minutes = int(str(remainder/60).split(".")[0])
        seconds = remainder - minutes*60
        return hours, minutes, seconds
    def getReturnTime(self,arrivalTime, delay, recallTime):
        flightTime = self.getFlightTime()
        flightTime = dt.timedelta(hours=flightTime[0],minutes=flightTime[1],seconds=flightTime[2])
        arrival = dt.datetime(int(arrivalTime[0]),int(arrivalTime[1]),int(arrivalTime[2]),int(arrivalTime[3]),int(arrivalTime[4]),int(arrivalTime[5])) #year,month,day,hour,minute,second
        returnTime = arrival + flightTime
        
        if recallTime == False:
            return [returnTime.day,returnTime.month,returnTime.year,returnTime.hour,returnTime.minute,returnTime.second]
        
        else:
            recallTime = dt.datetime(int(recallTime[0]),int(recallTime[1]),int(recallTime[2]),int(recallTime[3]),int(recallTime[4]),int(recallTime[5]))
            recallInterval = arrival - recallTime
            
            #latest return time
            lateReturnTime = returnTime - 2*recallInterval
            delay = dt.timedelta(seconds=int(delay))
            earlyReturnTime = lateReturnTime - 2*delay
            if lateReturnTime == earlyReturnTime:
                return [earlyReturnTime.day,earlyReturnTime.month,earlyReturnTime.year,earlyReturnTime.hour,earlyReturnTime.minute,earlyReturnTime.second]
            else:
                return([earlyReturnTime.day,earlyReturnTime.month,earlyReturnTime.year,earlyReturnTime.hour,earlyReturnTime.minute,earlyReturnTime.second],[lateReturnTime.day,lateReturnTime.month,lateReturnTime.year,lateReturnTime.hour,lateReturnTime.minute,lateReturnTime.second]) #a tuple of lists
    
                
        
        
def createShips(drives):
    sc = Ship("Small Cargo", 5000, "Combustion",drives, "civil")
    lc = Ship("Large Cargo", 7500, "Combustion",drives, "civil")
    lf = Ship("Light Fighter", 12500, "Combustion",drives, "military")
    hf = Ship("Heavy Fighter", 10000, "Impulse",drives, "military")
    cru = Ship("Cruiser", 15000, "Impulse",drives, "military")
    bs = Ship("Battleship", 10000, "Hyper",drives, "military")
    colo = Ship("Colony Ship", 2500, "Impulse",drives, "civil")
    rec = Ship("Recycler", 2000, "Combustion",drives, "civil")
    bomb = Ship("Bomber", 4000, "Impulse",drives, "military")
    des = Ship("Destroyer", 5000, "Hyper",drives, "military")
    rip = Ship("Deathstar", 100, "Hyper",drives, "military")
    bc = Ship("Battlecruiser", 10000, "Hyper",drives, "military")
    rp = Ship("Reaper", 7000, "Hyper", drives, "military")
    pf = Ship("Pathfinder", 12000, "Hyper", drives, "military")
    return [sc,lc,lf,hf,cru,bs,colo,rec,bomb,des,rip,bc,rp,pf]


if __name__ == "__main__":
    app = LanxCalc(None)
    app.title('LanxCalc')
    app.resizable(False,False)
    app.iconbitmap('icon.ico')
    app.mainloop()