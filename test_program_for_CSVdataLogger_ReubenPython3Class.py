# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision P, 07/14/2025

Verified working on: Python 3.11/3.12 for Windows 10/11 64-bit and Raspberry Pi Bookworm.
'''

__author__ = 'reuben.brewer'

###########################################################
from CSVdataLogger_ReubenPython3Class import *
from MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class import *
from MyPrint_ReubenPython2and3Class import *
###########################################################

###########################################################
import os
import sys
import platform
import time
import datetime
import threading
import collections
from collections import OrderedDict
import keyboard
import random
from random import randint

from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
###########################################################

###########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
###########################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
def GetLatestWaveformValue(CurrentTime, MinValue, MaxValue, Period, WaveformTypeString="Sine"):
    
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################
            OutputValue = 0.0
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            WaveformTypeString_ListOfAcceptableValues = ["Sine", "Cosine", "Triangular", "Square"]
        
            if WaveformTypeString not in WaveformTypeString_ListOfAcceptableValues:
                print("GetLatestWaveformValue: Error, WaveformTypeString must be in " + str(WaveformTypeString_ListOfAcceptableValues))
                return -11111.0
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if WaveformTypeString == "Sine":
    
                TimeGain = math.pi/Period
                OutputValue = (MaxValue + MinValue)/2.0 + 0.5*abs(MaxValue - MinValue)*math.sin(TimeGain*CurrentTime)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Cosine":
    
                TimeGain = math.pi/Period
                OutputValue = (MaxValue + MinValue)/2.0 + 0.5*abs(MaxValue - MinValue)*math.cos(TimeGain*CurrentTime)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Triangular":
                TriangularInput_TimeGain = 1.0
                TriangularInput_MinValue = -5
                TriangularInput_MaxValue = 5.0
                TriangularInput_PeriodInSeconds = 2.0
        
                #TriangularInput_Height0toPeak = abs(TriangularInput_MaxValue - TriangularInput_MinValue)
                #TriangularInput_CalculatedValue_1 = abs((TriangularInput_TimeGain*CurrentTime_CalculatedFromMainThread % PeriodicInput_PeriodInSeconds) - TriangularInput_Height0toPeak) + TriangularInput_MinValue
        
                A = abs(MaxValue - MinValue)
                P = Period
    
                #https://stackoverflow.com/questions/1073606/is-there-a-one-line-function-that-generates-a-triangle-wave
                OutputValue = (A / (P / 2)) * ((P / 2) - abs(CurrentTime % (2 * (P / 2)) - P / 2)) + MinValue
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Square":
    
                TimeGain = math.pi/Period
                MeanValue = (MaxValue + MinValue)/2.0
                SinusoidalValue =  MeanValue + 0.5*abs(MaxValue - MinValue)*math.sin(TimeGain*CurrentTime)
                
                if SinusoidalValue >= MeanValue:
                    OutputValue = MaxValue
                else:
                    OutputValue = MinValue
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            else:
                OutputValue = 0.0
            ##########################################################################################################
            ##########################################################################################################
            
            return OutputValue

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("GetLatestWaveformValue: Exceptions: %s" % exceptions)
            return -11111.0
            traceback.print_exc()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

    number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

    ListOfStringsToJoin = []

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if isinstance(input, str) == 1:
        ListOfStringsToJoin.append(input)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
        element = float(input)
        prefix_string = "{:." + str(number_of_decimal_places) + "f}"
        element_as_string = prefix_string.format(element)

        ##########################################################################################################
        ##########################################################################################################
        if element >= 0:
            element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
            element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
        else:
            element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
        ##########################################################################################################
        ##########################################################################################################

        ListOfStringsToJoin.append(element_as_string)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, list) == 1:

        if len(input) > 0:
            for element in input: #RECURSION
                ListOfStringsToJoin.append(ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a list() or []
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, tuple) == 1:

        if len(input) > 0:
            for element in input: #RECURSION
                ListOfStringsToJoin.append("TUPLE" + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a list() or []
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, dict) == 1:

        if len(input) > 0:
            for Key in input: #RECURSION
                ListOfStringsToJoin.append(str(Key) + ": " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a dict()
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    else:
        ListOfStringsToJoin.append(str(input))
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if len(ListOfStringsToJoin) > 1:

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        StringToReturn = ""
        for Index, StringToProcess in enumerate(ListOfStringsToJoin):

            ################################################
            if Index == 0: #The first element
                if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                    StringToReturn = "{"
                elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                    StringToReturn = "("
                else:
                    StringToReturn = "["

                StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
            ################################################

            ################################################
            elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                StringToReturn = StringToReturn + StringToProcess + ", "
            ################################################

            ################################################
            else: #The last element
                StringToReturn = StringToReturn + StringToProcess

                if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                    StringToReturn = StringToReturn + "}"
                elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                    StringToReturn = StringToReturn + ")"
                else:
                    StringToReturn = StringToReturn + "]"

            ################################################

        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    elif len(ListOfStringsToJoin) == 1:
        StringToReturn = ListOfStringsToJoin[0]

    else:
        StringToReturn = ListOfStringsToJoin

    return StringToReturn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

######################################################################################################
######################################################################################################
def ConvertDictToProperlyFormattedStringForPrinting(DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

    ProperlyFormattedStringForPrinting = ""
    ItemsPerLineCounter = 0

    for Key in DictToPrint:

        if isinstance(DictToPrint[Key], dict): #RECURSION
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                 str(Key) + ":\n" + \
                                                 ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

        else:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                 str(Key) + ": " + \
                                                 ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)

        if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
            ItemsPerLineCounter = ItemsPerLineCounter + 1
        else:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
            ItemsPerLineCounter = 0

    return ProperlyFormattedStringForPrinting
######################################################################################################
######################################################################################################


##########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def getTimeStampString():

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%m_%d_%Y---%H_%M_%S')

    return st
##########################################################################################################
##########################################################################################################

######################################################################################################
######################################################################################################
######################################################################################################
def UpdateGUItabObjectsOrderedDict():

    global EXIT_PROGRAM_FLAG

    global USE_CSVdataLogger_FLAG
    global CSVdataLogger_OPEN_FLAG
    global SHOW_IN_GUI_CSVdataLogger_FLAG

    global USE_MyPrint_FLAG
    global MyPrint_OPEN_FLAG
    global SHOW_IN_GUI_MyPrint_FLAG

    global GUItabObjectsOrderedDict

    try:

        if EXIT_PROGRAM_FLAG == 0:

            ######################################################################################################
            ######################################################################################################
            if len(GUItabObjectsOrderedDict) == 0: #Not yet populated
                GUItabObjectsOrderedDict = OrderedDict([("MainControls", dict([("UseFlag", 1), ("ShowFlag", 1), ("GUItabObjectName", "MainControls"), ("GUItabNameToDisplay", "MainControls"), ("IsTabCreatedFlag", 0), ("TabObject", None)])),
                                       ("CSVdataLogger", dict([("UseFlag", USE_CSVdataLogger_FLAG), ("ShowFlag", SHOW_IN_GUI_CSVdataLogger_FLAG), ("GUItabObjectName", "CSVdataLogger"), ("GUItabNameToDisplay", "CSVdataLogger"), ("IsTabCreatedFlag", 0), ("TabObject", None)])),
                                       ("MyPrint", dict([("UseFlag", USE_MyPrint_FLAG), ("ShowFlag", SHOW_IN_GUI_MyPrint_FLAG), ("GUItabObjectName", "MyPrint"), ("GUItabNameToDisplay", "MyPrint"), ("IsTabCreatedFlag", 0), ("TabObject", None)]))])
            ######################################################################################################
            ######################################################################################################

            ######################################################################################################
            ######################################################################################################
            GUItabObjectsOrderedDict["MainControls"]["OpenFlag"] = 1
            GUItabObjectsOrderedDict["CSVdataLogger"]["OpenFlag"] = CSVdataLogger_OPEN_FLAG
            GUItabObjectsOrderedDict["MyPrint"]["OpenFlag"] = MyPrint_OPEN_FLAG
            ######################################################################################################
            ######################################################################################################

            #print("UpdateGUItabObjectsOrderedDict, GUItabObjectsOrderedDict: " + str(GUItabObjectsOrderedDict))

    except:
        exceptions = sys.exc_info()[0]
        print("UpdateGUItabObjectsOrderedDict, exceptions: %s" % exceptions)
        traceback.print_exc()

######################################################################################################
######################################################################################################
######################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global MAIN_WHILE_LOOP_ENTERED_FLAG
    global USE_GUI_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global TKinter_LightRedColor
    global TKinter_LightGreenColor
    global TKinter_LightBlueColor
    global TKinter_LightYellowColor
    global TKinter_DefaultGrayColor
    global GreenCheckmarkPhotoImage
    global RedXphotoImage
    global TabControlObject
    global GUItabObjectsOrderedDict

    global ExperimentActivelyTesting_State
    global ExperimentActivelyTesting_State_LAST
    global ExperimentActivelyTesting_TimeElapsedInExperiment

    global ExperimentRecordAllData_Button
    global ExperimentRecordAllData_State_ToBeSet

    global CSVdataLogger_ReubenPython3ClassObject
    global CSVdataLogger_OPEN_FLAG
    global SHOW_IN_GUI_CSVdataLogger_FLAG
    global CSVdataLogger_Label
    global CSVdataLogger_MostRecentDict

    global MyPrint_ReubenPython2and3ClassObject
    global MyPrint_OPEN_FLAG
    global SHOW_IN_GUI_MyPrint_FLAG

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

            ######################################################################################################
            ######################################################################################################
            ######################################################################################################
            if MAIN_WHILE_LOOP_ENTERED_FLAG == 0:

                for TabNameStringAsKey in GUItabObjectsOrderedDict:

                    ######################################################################################################
                    ######################################################################################################
                    if "IsTabCreatedFlag" in GUItabObjectsOrderedDict[TabNameStringAsKey]:
                        if GUItabObjectsOrderedDict[TabNameStringAsKey]["IsTabCreatedFlag"] == 1:

                            ######################################################################################################
                            if GUItabObjectsOrderedDict[TabNameStringAsKey]["OpenFlag"] == 1:
                                TabControlObject.tab(GUItabObjectsOrderedDict[TabNameStringAsKey]["TabObject_InternalStringName"], state='normal')
                                TabControlObject.tab(GUItabObjectsOrderedDict[TabNameStringAsKey]["TabObject_InternalStringName"], image=GreenCheckmarkPhotoImage)
                            ######################################################################################################

                            ######################################################################################################
                            else:
                                TabControlObject.tab(GUItabObjectsOrderedDict[TabNameStringAsKey]["TabObject_InternalStringName"], state='disabled')
                                TabControlObject.tab(GUItabObjectsOrderedDict[TabNameStringAsKey]["TabObject_InternalStringName"], image=RedXphotoImage)
                            ######################################################################################################

                    ######################################################################################################
                    ######################################################################################################

            ######################################################################################################
            ######################################################################################################
            ######################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ActiveGUItabName = str(TabControlObject.tab(TabControlObject.select(), "text"))
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            if ActiveGUItabName == GUItabObjectsOrderedDict["MainControls"]["GUItabNameToDisplay"]:

                ##########################################################################################################
                ##########################################################################################################
                if CSVdataLogger_OPEN_FLAG == 1 and SHOW_IN_GUI_CSVdataLogger_FLAG == 1:
                    CSVdataLogger_ReubenPython3ClassObject.GUI_update_clock()
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                GUIobjectNamesListToDisableForExperiment = ["ExperimentRecordAllData_Button"]
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if ExperimentActivelyTesting_State == 1 and ExperimentActivelyTesting_State_LAST != ExperimentActivelyTesting_State: #STARTING the experiment

                    ExperimentActivelyTesting_Button["text"] = "Press to stop experiment"
                    ExperimentActivelyTesting_Button["bg"] = TKinter_LightRedColor

                    for GUIobjectName in GUIobjectNamesListToDisableForExperiment:
                        if GUIobjectName != "PeriodicInput_RadioButtonObjectsList":
                            eval(GUIobjectName)["state"] = "disabled"
                        else:
                            for element in eval(GUIobjectName):
                                element["state"] = "disabled"
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                elif ExperimentActivelyTesting_State == 0 and ExperimentActivelyTesting_State_LAST != ExperimentActivelyTesting_State: #STOPPING the experiment

                    ExperimentActivelyTesting_Button["text"] = "Press to start experiment"
                    ExperimentActivelyTesting_Button["bg"] = TKinter_LightGreenColor

                    for GUIobjectName in GUIobjectNamesListToDisableForExperiment:
                        if GUIobjectName != "PeriodicInput_RadioButtonObjectsList":
                            eval(GUIobjectName)["state"] = "normal"
                        else:
                            for element in eval(GUIobjectName):
                                element["state"] = "normal"
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if ExperimentRecordAllData_State_ToBeSet == 1:
                    ExperimentRecordAllData_Button["bg"] = TKinter_LightRedColor
                    ExperimentRecordAllData_Button["text"] = "Recording"
                else:
                    ExperimentRecordAllData_Button["bg"] = TKinter_LightGreenColor
                    ExperimentRecordAllData_Button["text"] = "Not recording"
                ##########################################################################################################
                ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            if CSVdataLogger_OPEN_FLAG == 1 and SHOW_IN_GUI_CSVdataLogger_FLAG == 1:
                if ActiveGUItabName == GUItabObjectsOrderedDict["CSVdataLogger"]["GUItabNameToDisplay"]:
                     
                    ##########################################################################################################
                    ##########################################################################################################
                    CSVdataLogger_Label["text"] = ConvertDictToProperlyFormattedStringForPrinting(CSVdataLogger_MostRecentDict, 
                                                                    NumberOfDecimalsPlaceToUse = 3, 
                                                                    NumberOfEntriesPerLine = 1, 
                                                                    NumberOfTabsBetweenItems = 3)
                    ##########################################################################################################
                    ##########################################################################################################
                    
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            if MyPrint_OPEN_FLAG == 1 and SHOW_IN_GUI_MyPrint_FLAG == 1:
                if ActiveGUItabName == GUItabObjectsOrderedDict["MyPrint"]["GUItabNameToDisplay"]:
                    MyPrint_ReubenPython2and3ClassObject.GUI_update_clock()
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
            root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG
    global CSVdataLogger_MostRecentDict_IsSavingFlag

    print("ExitProgram_Callback event fired!")

    if CSVdataLogger_MostRecentDict_IsSavingFlag == 0:
        EXIT_PROGRAM_FLAG = 1
    else:
        print("ExitProgram_Callback, ERROR! Still saving data.")
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global my_platform
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCallbackInterval_Milliseconds
    global GUIbuttonWidth
    global GUIbuttonPadX
    global GUIbuttonPadY
    global GUIbuttonFontSize
    global USE_GUI_FLAG
    global TKinter_LightRedColor
    global TKinter_LightGreenColor
    global TKinter_LightBlueColor
    global TKinter_LightYellowColor
    global TKinter_DefaultGrayColor

    global GreenCheckmarkPhotoImage
    global RedXphotoImage
    global GUItabObjectsOrderedDict
    global TabControlObject

    ########################################################################################################## KEY GUI LINE
    ##########################################################################################################
    root = Tk()
    ##########################################################################################################
    ##########################################################################################################

    ###################################################################################################### SET THE DEFAULT FONT FOR ALL WIDGETS CREATED AFTTER/BELOW THIS CALL
    ######################################################################################################
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=8)
    root.option_add("*Font", default_font)
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150)  # RGB
    TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150)  # RGB
    TKinter_LightBlueColor = '#%02x%02x%02x' % (150, 150, 255)  # RGB
    TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
    TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    try:
        GreenCheckmarkPhotoImage = PhotoImage(file=os.getcwd() + "//GreenCheckmark.gif")
        RedXphotoImage = PhotoImage(file=os.getcwd()  + "//RedXmark.gif")

    except:
        
        print("test_program_for_CSVdataLogger_ReubenPython3Class.py, GUI_Thread: GreenCheckmark.gif not found in os.getcwd()")
        
        try:
            GreenCheckmarkPhotoImage = PhotoImage(file=os.getcwd() + "//ParametersToBeLoaded//GreenCheckmark.gif")
            RedXphotoImage = PhotoImage(file=os.getcwd()  + "//ParametersToBeLoaded//RedXmark.gif")
        
        except:
            
            print("test_program_for_CSVdataLogger_ReubenPython3Class.py, GUI_Thread: GreenCheckmark.gif not found in os.getcwd() + //ParametersToBeLoaded")
            
            try:
                GreenCheckmarkPhotoImage = PhotoImage(file=os.getcwd() + "//InstallFiles_and_SupportDocuments//GreenCheckmark.gif")
                RedXphotoImage = PhotoImage(file=os.getcwd()  + "//InstallFiles_and_SupportDocuments//RedXmark.gif")
    
            except:
                exceptions = sys.exc_info()[0]
                print("test_program_for_CSVdataLogger_ReubenPython3Class.py, GUI_Thread: GreenCheckmark.gif not found in os.getcwd() + //InstallFiles_and_SupportDocuments")
                #traceback.print_exc()
                
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    TabControlObject = ttk.Notebook(root)
    ######################################################################################################

    ######################################################################################################
    TabCounter = 0
    for TabNameStringAsKey in GUItabObjectsOrderedDict:

        #############
        if GUItabObjectsOrderedDict[TabNameStringAsKey]["UseFlag"] == 1:
            GUItabObjectsOrderedDict[TabNameStringAsKey]["TabObject"] = ttk.Frame(TabControlObject)
            TabControlObject.add(GUItabObjectsOrderedDict[TabNameStringAsKey]["TabObject"], text=GUItabObjectsOrderedDict[TabNameStringAsKey]["GUItabNameToDisplay"])

            if TabCounter == 0:
                GUItabObjectsOrderedDict[TabNameStringAsKey]["TabObject_InternalStringName"] = ".!notebook.!frame"
            else:
                GUItabObjectsOrderedDict[TabNameStringAsKey]["TabObject_InternalStringName"] = ".!notebook.!frame" + str(TabCounter + 1)

            TabControlObject.tab(GUItabObjectsOrderedDict[TabNameStringAsKey]["TabObject_InternalStringName"], compound='top')
            GUItabObjectsOrderedDict[TabNameStringAsKey]["IsTabCreatedFlag"] = 1
            TabCounter = TabCounter + 1
        else:
            GUItabObjectsOrderedDict[TabNameStringAsKey]["TabObject"] = None
        #############

    ######################################################################################################

    ######################################################################################################
    TabControlObject.grid(row=0, column=0, sticky='nsew')

    ############# #Set the tab header font
    TabStyle = ttk.Style()
    TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
    #############

    ######################################################################################################

    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    global CSVdataLogger_Label
    CSVdataLogger_Label = Label(GUItabObjectsOrderedDict["CSVdataLogger"]["TabObject"], text="CSVdataLogger_Label", width=100, font=("Helvetica", 10))
    CSVdataLogger_Label.grid(row=0, column=0, padx=GUIbuttonPadX, pady=GUIbuttonPadY, columnspan=1, rowspan=1)
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    global ExperimentControlGuiFrame
    ExperimentControlGuiFrame = Frame(GUItabObjectsOrderedDict["MainControls"]["TabObject"])
    #ExperimentControlGuiFrame["borderwidth"] = 2
    #ExperimentControlGuiFrame["relief"] = "ridge"
    ExperimentControlGuiFrame.grid(row=0, column=0, padx=GUIbuttonPadX, pady=GUIbuttonPadY, rowspan=1, columnspan=1, sticky='w')
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    global ExperimentActivelyTesting_Button
    ExperimentActivelyTesting_Button = Button(ExperimentControlGuiFrame, text="Press to start experiment", state="normal", bg=TKinter_LightGreenColor, width=GUIbuttonWidth, command=lambda: ExperimentActivelyTesting_Button_Response())
    ExperimentActivelyTesting_Button.grid(row=0, column=0, padx=GUIbuttonPadX, pady=GUIbuttonPadY, columnspan=1, rowspan=1)
    ExperimentActivelyTesting_Button.config(font=("Helvetica", GUIbuttonFontSize))
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    global ExperimentRecordAllData_Button
    ExperimentRecordAllData_Button = Button(ExperimentControlGuiFrame, text="Record", state="normal", width=GUIbuttonWidth, command=lambda: ExperimentRecordAllData_Button_Response())
    ExperimentRecordAllData_Button.grid(row=0, column=1, padx=GUIbuttonPadX, pady=GUIbuttonPadY, columnspan=1, rowspan=1)
    ExperimentRecordAllData_Button.config(font=("Helvetica", GUIbuttonFontSize))
    ######################################################################################################
    ######################################################################################################

    ########################################################################################################## THIS BLOCK MUST COME 2ND-TO-LAST IN defGUI_Thread() IF USING TABS.
    ##########################################################################################################
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title("test_program_for_CSVdataLogger_ReubenPython3Class")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################  THIS BLOCK MUST COME LAST IN defGUI_Thread() REGARDLESS OF CODE.
    ##########################################################################################################
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################

######################################################################################################
######################################################################################################
def ExperimentActivelyTesting_Button_Response():
    global ExperimentActivelyTesting_State
    global ExperimentActivelyTesting_EventNeedsToBeFiredFlag

    if ExperimentActivelyTesting_State == 0:
        ExperimentActivelyTesting_EventNeedsToBeFiredFlag = 1
    else:
        ExperimentActivelyTesting_State = 2 #stops the experiment

######################################################################################################
######################################################################################################

######################################################################################################
######################################################################################################
def ExperimentRecordAllData_Button_Response():
    global ExperimentRecordAllData_EventNeedsToBeFiredFlag
    global ExperimentRecordAllData_State_ToBeSet

    if ExperimentRecordAllData_State_ToBeSet == 1:
        ExperimentRecordAllData_State_ToBeSet = 0
    else:
        ExperimentRecordAllData_State_ToBeSet = 1

    ExperimentRecordAllData_EventNeedsToBeFiredFlag = 1

######################################################################################################
######################################################################################################

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
if __name__ == '__main__':

    ######################################################################################################
    ######################################################################################################
    random.seed() #For random-number-generation
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    global my_platform

    if platform.system() == "Linux":

        if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
            my_platform = "pi"
        else:
            my_platform = "linux"

    elif platform.system() == "Windows":
        my_platform = "windows"

    elif platform.system() == "Darwin":
        my_platform = "mac"

    else:
        my_platform = "other"

    print("The OS platform is: " + my_platform)
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_CSVdataLogger_FLAG
    USE_CSVdataLogger_FLAG = 1

    global USE_MyPrint_FLAG
    USE_MyPrint_FLAG = 1

    global USE_MyPlotterPureTkinterStandAloneProcess_FLAG
    USE_MyPlotterPureTkinterStandAloneProcess_FLAG = 1

    global USE_Keyboard_FLAG
    USE_Keyboard_FLAG = 1
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    global SHOW_IN_GUI_CSVdataLogger_FLAG
    SHOW_IN_GUI_CSVdataLogger_FLAG = 1

    global SHOW_IN_GUI_MyPrint_FLAG
    SHOW_IN_GUI_MyPrint_FLAG = 1
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    global GUI_ROW_CSVdataLogger
    global GUI_COLUMN_CSVdataLogger
    global GUI_PADX_CSVdataLogger
    global GUI_PADY_CSVdataLogger
    global GUI_ROWSPAN_CSVdataLogger
    global GUI_COLUMNSPAN_CSVdataLogger
    GUI_ROW_CSVdataLogger = 1

    GUI_COLUMN_CSVdataLogger = 0
    GUI_PADX_CSVdataLogger = 1
    GUI_PADY_CSVdataLogger = 1
    GUI_ROWSPAN_CSVdataLogger = 1
    GUI_COLUMNSPAN_CSVdataLogger = 1
    GUI_WIDTH_CSVdataLogger = -1
    GUI_HEIGHT_CSVdataLogger = -1
    GUI_STICKY_CSVdataLogger = ""

    global GUI_ROW_MyPrint
    global GUI_COLUMN_MyPrint
    global GUI_PADX_MyPrint
    global GUI_PADY_MyPrint
    global GUI_ROWSPAN_MyPrint
    global GUI_COLUMNSPAN_MyPrint
    GUI_ROW_MyPrint = 2

    GUI_COLUMN_MyPrint = 0
    GUI_PADX_MyPrint = 1
    GUI_PADY_MyPrint = 1
    GUI_ROWSPAN_MyPrint = 1
    GUI_COLUMNSPAN_MyPrint = 1
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global MAIN_WHILE_LOOP_ENTERED_FLAG
    MAIN_WHILE_LOOP_ENTERED_FLAG = 0

    global CurrentTime_CalculatedFromMainThread
    CurrentTime_CalculatedFromMainThread = -11111.0

    global StartingTime_CalculatedFromMainThread
    StartingTime_CalculatedFromMainThread = -11111.0

    global root

    global root_Xpos
    root_Xpos = 900

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1920 - root_Xpos

    global root_height
    root_height = 1020 - root_Ypos

    global GUIbuttonPadX
    GUIbuttonPadX = 1

    global GUIbuttonPadY
    GUIbuttonPadY = 1

    global GUIbuttonWidth
    GUIbuttonWidth = 40

    global GUIbuttonFontSize
    GUIbuttonFontSize = 12

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30

    global PeriodicInput_AcceptableValues
    PeriodicInput_AcceptableValues = ["GUI", "VINThub", "Sine", "Cosine", "Triangular", "Square"]

    global PeriodicInput_Type_1
    PeriodicInput_Type_1 = "Sine"

    global PeriodicInput_MinValue_1
    PeriodicInput_MinValue_1 = -1.0

    global PeriodicInput_MaxValue_1
    PeriodicInput_MaxValue_1 = 1.0

    global PeriodicInput_Period_1
    PeriodicInput_Period_1 = 1.0

    global PeriodicInput_CalculatedValue_1
    PeriodicInput_CalculatedValue_1 = 0.0

    global PeriodicInput_Type_2
    PeriodicInput_Type_2 = "Sine"

    global PeriodicInput_MinValue_2
    PeriodicInput_MinValue_2 = -1.0

    global PeriodicInput_MaxValue_2
    PeriodicInput_MaxValue_2 = 1.0

    global PeriodicInput_Period_2
    PeriodicInput_Period_2 = 1.0

    global PeriodicInput_CalculatedValue_2
    PeriodicInput_CalculatedValue_2 = 0.0
    
    global NoiseCounter
    NoiseCounter = 0

    global NoiseCounter_FireEveryNth
    NoiseCounter_FireEveryNth = 5

    global NoiseAmplitude_Percent0to1OfPeriodicInputAmplitude
    NoiseAmplitude_Percent0to1OfPeriodicInputAmplitude = 0.25
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    global ExperimentActivelyTesting_EventNeedsToBeFiredFlag
    ExperimentActivelyTesting_EventNeedsToBeFiredFlag = 0

    global ExperimentActivelyTesting_EventFiredAtTimeSeconds
    ExperimentActivelyTesting_EventFiredAtTimeSeconds = 0.0

    global Experiment_FixedDurationInSeconds
    Experiment_FixedDurationInSeconds = 10.0

    global ExperimentActivelyTesting_TimeElapsedInExperiment
    ExperimentActivelyTesting_TimeElapsedInExperiment = 0.0

    global ExperimentActivelyTesting_State
    ExperimentActivelyTesting_State = 0

    global ExperimentActivelyTesting_State_LAST
    ExperimentActivelyTesting_State_LAST = 0

    global ExperimentRecordAllData_EventNeedsToBeFiredFlag
    ExperimentRecordAllData_EventNeedsToBeFiredFlag = 0

    global ExperimentRecordAllData_State_ToBeSet
    ExperimentRecordAllData_State_ToBeSet = 0

    global TrialNumber
    TrialNumber = 0
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    global CSVdataLogger_ReubenPython3ClassObject

    global CSVdataLogger_OPEN_FLAG
    CSVdataLogger_OPEN_FLAG = -1

    global CSVdataLogger_MostRecentDict
    CSVdataLogger_MostRecentDict = dict()

    global CSVdataLogger_MostRecentDict_Time
    CSVdataLogger_MostRecentDict_Time = -11111.0

    global CSVdataLogger_MostRecentDict_DataStreamingFrequency_CalculatedFromMainThread
    CSVdataLogger_MostRecentDict_DataStreamingFrequency_CalculatedFromMainThread = -11111.0

    global CSVdataLogger_MostRecentDict_AcceptNewDataFlag
    CSVdataLogger_MostRecentDict_AcceptNewDataFlag = -1

    global CSVdataLogger_MostRecentDict_DataQueue_qsize
    CSVdataLogger_MostRecentDict_DataQueue_qsize = -1

    global CSVdataLogger_MostRecentDict_VariableNamesForHeaderList
    CSVdataLogger_MostRecentDict_VariableNamesForHeaderList = []

    global CSVdataLogger_MostRecentDict_FilepathFull
    CSVdataLogger_MostRecentDict_FilepathFull = ""

    global CSVdataLogger_MostRecentDict_FilenamePrefix
    CSVdataLogger_MostRecentDict_FilenamePrefix = ""

    global CSVdataLogger_MostRecentDict_TrialNumber
    CSVdataLogger_MostRecentDict_TrialNumber = -1

    global CSVdataLogger_MostRecentDict_NoteToAddToFile
    CSVdataLogger_MostRecentDict_NoteToAddToFile = ""

    global CSVdataLogger_MostRecentDict_IsSavingFlag
    CSVdataLogger_MostRecentDict_IsSavingFlag = 0

    ######################################################################################################
    global CSVdataLogger_CSVfile_DirectoryPath

    if platform.system() == "Windows":
        CSVdataLogger_CSVfile_DirectoryPath = os.getcwd() + "\\CSVfiles"
    else:
        CSVdataLogger_CSVfile_DirectoryPath = os.getcwd() + "//CSVfiles" #Linux requires the opposite-direction slashes
    ######################################################################################################

    ######################################################################################################
    global CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList #unicorn
    CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList = ["Time",
                                                                                    "PeriodicInput_CalculatedValue_1",
                                                                                    "PeriodicInput_CalculatedValue_2"]
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    global MyPrint_ReubenPython2and3ClassObject

    global MyPrint_OPEN_FLAG
    MyPrint_OPEN_FLAG = -1
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject

    global MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG
    MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = -1

    global MyPlotterPureTkinterStandAloneProcess_MostRecentDict
    MyPlotterPureTkinterStandAloneProcess_MostRecentDict = dict()

    global MyPlotterPureTkinterStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag
    MyPlotterPureTkinterStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = -1

    global LastTime_CalculatedFromMainThread_MyPlotterPureTkinterStandAloneProcess
    LastTime_CalculatedFromMainThread_MyPlotterPureTkinterStandAloneProcess = -11111.0
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    global GUItabObjectsOrderedDict
    GUItabObjectsOrderedDict = OrderedDict()

    UpdateGUItabObjectsOrderedDict()
    ######################################################################################################
    ######################################################################################################

    #######################################################################################################  KEY GUI LINE
    ######################################################################################################
    if USE_GUI_FLAG == 1:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread)
        GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
        time.sleep(0.5)  #Allow enough time for 'root' to be created that we can then pass it into other classes.

    else:
        pass
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    global CSVdataLogger_ReubenPython3ClassObject_GUIparametersDict
    CSVdataLogger_ReubenPython3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_CSVdataLogger_FLAG),
                                    ("root", GUItabObjectsOrderedDict["MainControls"]["TabObject"]),
                                    ("EnableInternal_MyPrint_Flag", 0),
                                    ("NumberOfPrintLines", 10),
                                    ("UseBorderAroundThisGuiObjectFlag", 1),
                                    ("GUI_ROW", GUI_ROW_CSVdataLogger),
                                    ("GUI_COLUMN", GUI_COLUMN_CSVdataLogger),
                                    ("GUI_PADX", GUI_PADX_CSVdataLogger),
                                    ("GUI_PADY", GUI_PADY_CSVdataLogger),
                                    ("GUI_ROWSPAN", GUI_ROWSPAN_CSVdataLogger),
                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_CSVdataLogger),
                                    ("GUI_WIDTH", GUI_WIDTH_CSVdataLogger),
                                    ("GUI_HEIGHT", GUI_HEIGHT_CSVdataLogger),
                                    ("GUI_STICKY", GUI_STICKY_CSVdataLogger)])
    ######################################################################################################

    ######################################################################################################
    global CSVdataLogger_ReubenPython3ClassObject_setup_dict
    CSVdataLogger_ReubenPython3ClassObject_setup_dict = dict([("GUIparametersDict", CSVdataLogger_ReubenPython3ClassObject_GUIparametersDict),
                                                                ("CSVfile_DirectoryPath", CSVdataLogger_CSVfile_DirectoryPath),
                                                                ("FilenamePrefix", "ThisIsYourBrainOnPrefixes_"),
                                                                ("VariableNamesForHeaderList", CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList),
                                                                ("MainThread_TimeToSleepEachLoop", 0.010),
                                                                ("SaveOnStartupFlag", 0),
                                                                ("EnableSaveButtonFlag", 0),
                                                                ("ShowSaveButtonFlag", 0),
                                                                ("SimplifyDataLabelFlag", 0)])
    ######################################################################################################

    ######################################################################################################
    if USE_CSVdataLogger_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            CSVdataLogger_ReubenPython3ClassObject = CSVdataLogger_ReubenPython3Class(CSVdataLogger_ReubenPython3ClassObject_setup_dict)
            CSVdataLogger_OPEN_FLAG = CSVdataLogger_ReubenPython3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("CSVdataLogger_ReubenPython3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    if USE_CSVdataLogger_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if CSVdataLogger_OPEN_FLAG != 1:
                print("Failed to open CSVdataLogger_ReubenPython3Class.")
                ExitProgram_Callback()
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    UpdateGUItabObjectsOrderedDict()
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    global MyPrint_ReubenPython2and3ClassObject_GUIparametersDict
    MyPrint_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MyPrint_FLAG),
                                                                    ("root", GUItabObjectsOrderedDict["MyPrint"]["TabObject"]),
                                                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                    ("GUI_ROW", GUI_ROW_MyPrint),
                                                                    ("GUI_COLUMN", GUI_COLUMN_MyPrint),
                                                                    ("GUI_PADX", GUI_PADX_MyPrint),
                                                                    ("GUI_PADY", GUI_PADY_MyPrint),
                                                                    ("GUI_ROWSPAN", GUI_ROWSPAN_MyPrint),
                                                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_MyPrint)])

    global MyPrint_ReubenPython2and3ClassObject_setup_dict
    MyPrint_ReubenPython2and3ClassObject_setup_dict = dict([("NumberOfPrintLines", 10),
                                                            ("WidthOfPrintingLabel", 200),
                                                            ("PrintToConsoleFlag", 1),
                                                            ("LogFileNameFullPath", os.getcwd() + "//TestLog.txt"),
                                                            ("GUIparametersDict", MyPrint_ReubenPython2and3ClassObject_GUIparametersDict)])

    if USE_MyPrint_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPrint_ReubenPython2and3ClassObject = MyPrint_ReubenPython2and3Class(MyPrint_ReubenPython2and3ClassObject_setup_dict)
            MyPrint_OPEN_FLAG = MyPrint_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPrint_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    if USE_MyPrint_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPrint_OPEN_FLAG != 1:
                print("Failed to open MyPrint_ReubenPython2and3Class.")
                ExitProgram_Callback()
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    UpdateGUItabObjectsOrderedDict()
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict = dict([("EnableInternal_MyPrint_Flag", 1),
                                                                                                ("NumberOfPrintLines", 10),
                                                                                                ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                                                ("GraphCanvasWidth", 890),
                                                                                                ("GraphCanvasHeight", 700),
                                                                                                ("GraphCanvasWindowStartingX", 0),
                                                                                                ("GraphCanvasWindowStartingY", 0),
                                                                                                ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 20)])

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict = dict([("GUIparametersDict", MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict),
                                                                                        ("ParentPID", os.getpid()),
                                                                                        ("WatchdogTimerExpirationDurationSeconds_StandAlonePlottingProcess", 5.0),
                                                                                        ("CurvesToPlotNamesAndColorsDictOfLists", dict([("NameList", ["Channel0", "Channel1"]),
                                                                                                                                        ("MarkerSizeList", [3, 3]),
                                                                                                                                        ("LineWidthList", [3, 3]),
                                                                                                                                        ("ColorList", ["Red", "Green"])])),
                                                                                        ("NumberOfDataPointToPlot", 50),
                                                                                        ("XaxisNumberOfTickMarks", 10),
                                                                                        ("YaxisNumberOfTickMarks", 10),
                                                                                        ("XaxisNumberOfDecimalPlacesForLabels", 3),
                                                                                        ("YaxisNumberOfDecimalPlacesForLabels", 3),
                                                                                        ("XaxisAutoscaleFlag", 1),
                                                                                        ("YaxisAutoscaleFlag", 1),
                                                                                        ("X_min", 0.0),
                                                                                        ("X_max", 20.0),
                                                                                        ("Y_min", -30.0),
                                                                                        ("Y_max", 30.0),
                                                                                        ("XaxisDrawnAtBottomOfGraph", 0),
                                                                                        ("XaxisLabelString", "Time (sec)"),
                                                                                        ("YaxisLabelString", "Y-units (units)"),
                                                                                        ("ShowLegendFlag", 1)])

    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict)
            MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject, exceptions: %s" % exceptions)
            traceback.print_exc()
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG != 1:
                print("Failed to open MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class.")
                ExitProgram_Callback()
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    if USE_Keyboard_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        keyboard.on_press_key("esc", ExitProgram_Callback)
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    while(EXIT_PROGRAM_FLAG == 0):

        ######################################################################################################
        ######################################################################################################
        ######################################################################################################
        if MAIN_WHILE_LOOP_ENTERED_FLAG == 0:
            MAIN_WHILE_LOOP_ENTERED_FLAG = 1
            StartingTime_CalculatedFromMainThread = getPreciseSecondsTimeStampString()
        ######################################################################################################
        ######################################################################################################
        ######################################################################################################

        ######################################################################################################
        ######################################################################################################
        ######################################################################################################
        CurrentTime_CalculatedFromMainThread = getPreciseSecondsTimeStampString() - StartingTime_CalculatedFromMainThread
        ######################################################################################################
        ######################################################################################################
        ######################################################################################################

        ###################################################################################################### GET's
        ######################################################################################################
        ######################################################################################################
        if CSVdataLogger_OPEN_FLAG == 1:

            CSVdataLogger_MostRecentDict = CSVdataLogger_ReubenPython3ClassObject.GetMostRecentDataDict()

            if "Time" in CSVdataLogger_MostRecentDict:
                CSVdataLogger_MostRecentDict_Time = CSVdataLogger_MostRecentDict["Time"]
                CSVdataLogger_MostRecentDict_DataStreamingFrequency_CalculatedFromMainThread = CSVdataLogger_MostRecentDict["DataStreamingFrequency_CalculatedFromMainThread"]
                CSVdataLogger_MostRecentDict_AcceptNewDataFlag = CSVdataLogger_MostRecentDict["AcceptNewDataFlag"]
                CSVdataLogger_MostRecentDict_DataQueue_qsize = CSVdataLogger_MostRecentDict["DataQueue_qsize"]
                CSVdataLogger_MostRecentDict_VariableNamesForHeaderList = CSVdataLogger_MostRecentDict["VariableNamesForHeaderList"]
                CSVdataLogger_MostRecentDict_FilepathFull = CSVdataLogger_MostRecentDict["FilepathFull"]
                CSVdataLogger_MostRecentDict_FilenamePrefix = CSVdataLogger_MostRecentDict["FilenamePrefix"]
                CSVdataLogger_MostRecentDict_TrialNumber = CSVdataLogger_MostRecentDict["TrialNumber"]
                CSVdataLogger_MostRecentDict_NoteToAddToFile = CSVdataLogger_MostRecentDict["NoteToAddToFile"]
                CSVdataLogger_MostRecentDict_IsSavingFlag = CSVdataLogger_MostRecentDict["IsSavingFlag"]

                CSVdataLogger_FileNamePrefix = CSVdataLogger_MostRecentDict_FilenamePrefix #Update in case the user entered something different into the GUI's entry.
                TrialNumber = CSVdataLogger_MostRecentDict_TrialNumber #Update in case the user entered something different into the GUI's entry.

                #print("CSVdataLogger_MostRecentDict: " + str(CSVdataLogger_MostRecentDict))
        ######################################################################################################
        ######################################################################################################
        ######################################################################################################

        ###################################################################################################### unicorn
        ######################################################################################################
        ######################################################################################################
        if ExperimentActivelyTesting_EventNeedsToBeFiredFlag == 1:

            ######################################################################################################
            ######################################################################################################
            if ExperimentActivelyTesting_State == 0:

                ######################################################################################################
                ExperimentRecordAllData_State_ToBeSet = 1
                ExperimentRecordAllData_EventNeedsToBeFiredFlag = 1
                ######################################################################################################

                ######################################################################################################
                ExperimentActivelyTesting_EventFiredAtTimeSeconds = CurrentTime_CalculatedFromMainThread
                ExperimentActivelyTesting_State_LAST = 0
                ExperimentActivelyTesting_State = 1
                ######################################################################################################

            ######################################################################################################
            ######################################################################################################

            ######################################################################################################
            ######################################################################################################
            elif ExperimentActivelyTesting_State == 1:

                ExperimentActivelyTesting_TimeElapsedInExperiment = CurrentTime_CalculatedFromMainThread - ExperimentActivelyTesting_EventFiredAtTimeSeconds

                if ExperimentActivelyTesting_TimeElapsedInExperiment >= Experiment_FixedDurationInSeconds:
                    ExperimentActivelyTesting_State_LAST = 1
                    ExperimentActivelyTesting_State = 2

                else:
                    pass #Set how you want actuators/motors to change states/speeds DURING the experiment

            ######################################################################################################
            ######################################################################################################
            else:

                pass #Typically want to disable/stop motors as this is where the experiment ends.

                ExperimentRecordAllData_State_ToBeSet = 0 #STOP RECORDING THE CSV
                ExperimentRecordAllData_EventNeedsToBeFiredFlag = 1

                ExperimentActivelyTesting_State_LAST = 2
                ExperimentActivelyTesting_State = 0

                TrialNumber = TrialNumber + 1
                if CSVdataLogger_OPEN_FLAG == 1:
                    CSVdataLogger_ReubenPython3ClassObject.SetTrialNumber(TrialNumber)

                print("\n********** Experiment completed! **********\n")
                ExperimentActivelyTesting_EventNeedsToBeFiredFlag = 0

            ######################################################################################################
            ######################################################################################################

        ######################################################################################################
        ######################################################################################################
        ######################################################################################################

        ######################################################################################################
        ######################################################################################################
        if ExperimentRecordAllData_EventNeedsToBeFiredFlag == 1:


            ######################################################################################################
            if ExperimentRecordAllData_State_ToBeSet == 1:
                Timestamp = getTimeStampString()

                CSVfile_DirectoryPath_Input = CSVdataLogger_CSVfile_DirectoryPath
                print("CSVfile_DirectoryPath_Input: " + CSVfile_DirectoryPath_Input)
            ######################################################################################################

            ######################################################################################################
            if CSVdataLogger_OPEN_FLAG == 1:
                if ExperimentRecordAllData_State_ToBeSet == 1:
                    CSVdataLogger_ReubenPython3ClassObject.CreateCSVfileAndStartWritingData(CSVfile_DirectoryPath_Input = "",
                                                                                            FilenamePrefix_Input = CSVdataLogger_FileNamePrefix,
                                                                                            TrialNumber_Input = TrialNumber,
                                                                                            NoteToAddToFile_Input = "",
                                                                                            VariableNamesForHeaderList_Input = CSVdataLogger_MostRecentDict_VariableNamesForHeaderList)
                                                                                            
                else:
                    CSVdataLogger_ReubenPython3ClassObject.StopWritingDataAndCloseCSVfileImmediately()
            ######################################################################################################

            ExperimentRecordAllData_EventNeedsToBeFiredFlag = 0
        ######################################################################################################
        ######################################################################################################



        ###################################################################################################### SET's
        ######################################################################################################
        ######################################################################################################

        ######################################################################################################
        ######################################################################################################
        PeriodicInput_CalculatedValue_1 = GetLatestWaveformValue(CurrentTime_CalculatedFromMainThread, 
                                                                PeriodicInput_MinValue_1, 
                                                                PeriodicInput_MaxValue_1, 
                                                                PeriodicInput_Period_1, 
                                                                PeriodicInput_Type_1)
        ######################################################################################################
        ######################################################################################################

        ######################################################################################################
        ######################################################################################################

        ######################################################################################################
        PeriodicInput_CalculatedValue_2 = PeriodicInput_CalculatedValue_1*2.0 + 3.0
        ######################################################################################################

        ######################################################################################################
        NoiseCounter = NoiseCounter + 1
        if NoiseCounter == NoiseCounter_FireEveryNth:
            NoiseAmplitude = NoiseAmplitude_Percent0to1OfPeriodicInputAmplitude * abs(PeriodicInput_MaxValue_1 - PeriodicInput_MinValue_1)
            NoiseValue = random.uniform(-1.0 * NoiseAmplitude, NoiseAmplitude)
            PeriodicInput_CalculatedValue_2 = PeriodicInput_CalculatedValue_2 + NoiseValue
            NoiseCounter = 0
        ######################################################################################################
        
        ######################################################################################################
        ######################################################################################################

        ######################################################################################################
        ######################################################################################################
        if CSVdataLogger_OPEN_FLAG == 1:
            CSVdataLogger_ReubenPython3ClassObject.AddDataToCSVfile_ExternalFunctionCall([CurrentTime_CalculatedFromMainThread,
                                                                                          PeriodicInput_CalculatedValue_1,
                                                                                          PeriodicInput_CalculatedValue_2])
        ######################################################################################################
        ######################################################################################################

        ######################################################################################################
        ######################################################################################################
        ######################################################################################################

        ###################################################################################################### SET's
        ######################################################################################################
        ######################################################################################################
        if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:

            ######################################################################################################
            ######################################################################################################
            try:
                MyPlotterPureTkinterStandAloneProcess_MostRecentDict = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.GetMostRecentDataDict()

                if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess_MostRecentDict:
                    MyPlotterPureTkinterStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                    if MyPlotterPureTkinterStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag == 1:
                        if CurrentTime_CalculatedFromMainThread - LastTime_CalculatedFromMainThread_MyPlotterPureTkinterStandAloneProcess >= 0.040:
                            MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExternalAddPointOrListOfPointsToPlot(["Channel0", "Channel1"], [CurrentTime_CalculatedFromMainThread]*2, [PeriodicInput_CalculatedValue_1, PeriodicInput_CalculatedValue_2])

                            LastTime_CalculatedFromMainThread_MyPlotterPureTkinterStandAloneProcess = CurrentTime_CalculatedFromMainThread
            ######################################################################################################
            ######################################################################################################

            ######################################################################################################
            ######################################################################################################
            except:
                exceptions = sys.exc_info()[0]
                print("MyPlotterPureTkinterStandAloneProcess, exceptions: %s" % exceptions)
                traceback.print_exc()
            ######################################################################################################
            ######################################################################################################

        ######################################################################################################
        ######################################################################################################
        ######################################################################################################

        time.sleep(0.040)

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################

    ###################################################################################################### THIS IS THE EXIT ROUTINE!
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    print("Exiting main program 'test_program_for_CSVdataLogger_ReubenPython3Class.")

    ######################################################################################################
    if CSVdataLogger_OPEN_FLAG == 1:
        CSVdataLogger_ReubenPython3ClassObject.ExitProgram_Callback()
    ######################################################################################################

    ######################################################################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject.ExitProgram_Callback()
    ######################################################################################################

    ######################################################################################################
    if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:
        MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExitProgram_Callback()
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
