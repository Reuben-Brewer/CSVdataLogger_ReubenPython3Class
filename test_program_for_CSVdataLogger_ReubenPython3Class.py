# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision J, 06/03/2025

Verified working on: Python 3.11/3.12 for Windows 10/11 64-bit and Raspberry Pi Bookworm (may work on Mac in non-GUI mode, but haven't tested yet).
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
import keyboard

from tkinter import * #Python 3
import tkinter.font as tkFont #Python 3
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
                #TriangularInput_CalculatedValue_1 = abs((TriangularInput_TimeGain*CurrentTime_MainLoopThread % SinusoidalInput_PeriodInSeconds) - TriangularInput_Height0toPeak) + TriangularInput_MinValue
        
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

##########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG

    global CSVdataLogger_ReubenPython3ClassObject
    global CSVdataLogger_OPEN_FLAG
    global SHOW_IN_GUI_CSVdataLogger_FLAG

    global MyPrint_ReubenPython2and3ClassObject
    global MyPrint_OPEN_FLAG
    global SHOW_IN_GUI_MyPrint_FLAG

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        ##########################################################################################################
        ##########################################################################################################

            ##########################################################################################################
            if CSVdataLogger_OPEN_FLAG == 1 and SHOW_IN_GUI_CSVdataLogger_FLAG == 1:
                CSVdataLogger_ReubenPython3ClassObject.GUI_update_clock()
            ##########################################################################################################

            ##########################################################################################################
            if MyPrint_OPEN_FLAG == 1 and SHOW_IN_GUI_MyPrint_FLAG == 1:
                MyPrint_ReubenPython2and3ClassObject.GUI_update_clock()
            ##########################################################################################################

            root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
        ##########################################################################################################
        ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG
    global CSVdataLogger_ReubenPython3ClassObject_IsSavingFlag

    print("ExitProgram_Callback event fired!")

    if CSVdataLogger_ReubenPython3ClassObject_IsSavingFlag == 0:
        EXIT_PROGRAM_FLAG = 1
    else:
        print("ExitProgram_Callback, ERROR! Still saving data.")
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_TABS_IN_GUI_FLAG

    ########################################################################################################## KEY GUI LINE
    ##########################################################################################################
    root = Tk()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    global TabControlObject
    global Tab_MainControls
    global Tab_CSVdataLogger
    global Tab_MyPrint

    if USE_TABS_IN_GUI_FLAG == 1:
        ##########################################################################################################
        TabControlObject = ttk.Notebook(root)

        Tab_CSVdataLogger = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_CSVdataLogger, text='   CSVdataLogger   ')

        Tab_MainControls = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MainControls, text='   Main Controls   ')

        Tab_MyPrint = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MyPrint, text='   MyPrint Terminal   ')

        TabControlObject.pack(expand=1, fill="both")  # CANNOT MIX PACK AND GRID IN THE SAME FRAME/TAB, SO ALL .GRID'S MUST BE CONTAINED WITHIN THEIR OWN FRAME/TAB.

        ############# #Set the tab header font
        TabStyle = ttk.Style()
        TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        #############

        ##########################################################################################################
    else:
        ##########################################################################################################
        Tab_MainControls = root
        Tab_CSVdataLogger = root
        Tab_MyPrint = root
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    ##########################################################################################################
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title("test_program_for_CSVdataLogger_ReubenPython3Class")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################  THIS BLOCK MUST COME LAST IN def GUI_Thread() REGARDLESS OF CODE.
    ##########################################################################################################
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    #################################################
    #################################################
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
    #################################################
    #################################################

    #################################################
    #################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_TABS_IN_GUI_FLAG
    USE_TABS_IN_GUI_FLAG = 1

    global USE_CSVdataLogger_FLAG
    USE_CSVdataLogger_FLAG = 1

    global USE_MyPrint_FLAG
    USE_MyPrint_FLAG = 1

    global USE_MyPlotterPureTkinterStandAloneProcess_FLAG
    USE_MyPlotterPureTkinterStandAloneProcess_FLAG = 1

    global USE_Keyboard_FLAG
    USE_Keyboard_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global SHOW_IN_GUI_CSVdataLogger_FLAG
    SHOW_IN_GUI_CSVdataLogger_FLAG = 1

    global SHOW_IN_GUI_MyPrint_FLAG
    SHOW_IN_GUI_MyPrint_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
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
    #################################################
    #################################################

    #################################################
    #################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0

    global root

    global root_Xpos
    root_Xpos = 900

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1920 - root_Xpos

    global root_height
    root_height = 1020 - root_Ypos

    global TabControlObject
    global Tab_MainControls
    global Tab_CSVdataLogger
    global Tab_MyPrint

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30

    global ControlInput_AcceptableValues
    ControlInput_AcceptableValues = ["GUI", "VINThub", "Sine", "Cosine", "Triangular", "Square"]

    global ControlInput_1
    ControlInput_1 = "Sine"

    global ControlInput_MinValue_1
    ControlInput_MinValue_1 = -3.0

    global ControlInput_MaxValue_1
    ControlInput_MaxValue_1 = 3.0

    global ControlInput_Period_1
    ControlInput_Period_1 = 4.0

    global ControlInput_CalculatedValue_1
    SinusoidalInput_CalculatedValue_1 = 0.0

    global ControlInput_2
    ControlInput_2 = "Triangular"

    global ControlInput_MinValue_2
    ControlInput_MinValue_2 = -1.0

    global ControlInput_MaxValue_2
    ControlInput_MaxValue_2 = 5.0

    global ControlInput_Period_2
    ControlInput_Period_2 = 3

    global ControlInput_CalculatedValue_2
    SinusoidalInput_CalculatedValue_2 = 0.0
    #################################################
    #################################################

    #################################################
    #################################################
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

    global CSVdataLogger_MostRecentDict_SaveFlag
    CSVdataLogger_MostRecentDict_SaveFlag = -1

    global CSVdataLogger_MostRecentDict_DataQueue_qsize
    CSVdataLogger_MostRecentDict_DataQueue_qsize = -1

    global CSVdataLogger_MostRecentDict_VariableNamesForHeaderList
    CSVdataLogger_MostRecentDict_VariableNamesForHeaderList = []

    global CSVdataLogger_MostRecentDict_FilepathFull
    CSVdataLogger_MostRecentDict_FilepathFull = ""

    global CSVdataLogger_HeaderWrittenYetFlag
    CSVdataLogger_HeaderWrittenYetFlag = 0

    global CSVdataLogger_IsSavingFlag
    CSVdataLogger_IsSavingFlag = 0

    #################################################
    global CSVdataLogger_CSVfile_DirectoryPath

    if platform.system() == "Windows":
        CSVdataLogger_CSVfile_DirectoryPath = os.getcwd() + "\\CSVfiles"
    else:
        CSVdataLogger_CSVfile_DirectoryPath = os.getcwd() + "//CSVfiles" #Linux requires the opposite-direction slashes
    #################################################

    #################################################
    global CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList #unicorn
    CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList = ["Time",
                                                                                    "ControlInput_CalculatedValue_1",
                                                                                    "ControlInput_CalculatedValue_2"]
    #################################################

    #################################################
    #################################################

    #################################################
    #################################################
    global MyPrint_ReubenPython2and3ClassObject

    global MyPrint_OPEN_FLAG
    MyPrint_OPEN_FLAG = -1
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject

    global MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG
    MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = -1

    global MyPlotterPureTkinterStandAloneProcess_MostRecentDict
    MyPlotterPureTkinterStandAloneProcess_MostRecentDict = dict()

    global MyPlotterPureTkinterStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag
    MyPlotterPureTkinterStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = -1

    global LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess
    LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess = -11111.0
    #################################################
    #################################################

    #################################################  KEY GUI LINE
    #################################################
    if USE_GUI_FLAG == 1:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread)
        GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
        time.sleep(0.5)  #Allow enough time for 'root' to be created that we can then pass it into other classes.
    else:
        root = None
        Tab_MainControls = None
        Tab_CSVdataLogger = None
        Tab_MyPrint = None
    #################################################
    #################################################

    #################################################
    #################################################

    #################################################
    global CSVdataLogger_ReubenPython3ClassObject_GUIparametersDict
    CSVdataLogger_ReubenPython3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_CSVdataLogger_FLAG),
                                    ("root", Tab_CSVdataLogger),
                                    ("EnableInternal_MyPrint_Flag", 1),
                                    ("NumberOfPrintLines", 10),
                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                    ("GUI_ROW", GUI_ROW_CSVdataLogger),
                                    ("GUI_COLUMN", GUI_COLUMN_CSVdataLogger),
                                    ("GUI_PADX", GUI_PADX_CSVdataLogger),
                                    ("GUI_PADY", GUI_PADY_CSVdataLogger),
                                    ("GUI_ROWSPAN", GUI_ROWSPAN_CSVdataLogger),
                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_CSVdataLogger)])
    #################################################

    #################################################
    global CSVdataLogger_ReubenPython3ClassObject_setup_dict
    CSVdataLogger_ReubenPython3ClassObject_setup_dict = dict([("GUIparametersDict", CSVdataLogger_ReubenPython3ClassObject_GUIparametersDict),
                                                                                ("NameToDisplay_UserSet", "CSVdataLogger"),
                                                                                ("CSVfile_DirectoryPath", CSVdataLogger_CSVfile_DirectoryPath),
                                                                                ("FileNamePrefix", "CSV_file_"),
                                                                                ("VariableNamesForHeaderList", CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList),
                                                                                ("MainThread_TimeToSleepEachLoop", 0.010),
                                                                                ("SaveOnStartupFlag", 0)])
    #################################################

    #################################################
    if USE_CSVdataLogger_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            CSVdataLogger_ReubenPython3ClassObject = CSVdataLogger_ReubenPython3Class(CSVdataLogger_ReubenPython3ClassObject_setup_dict)
            CSVdataLogger_OPEN_FLAG = CSVdataLogger_ReubenPython3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("CSVdataLogger_ReubenPython3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################

    #################################################
    #################################################

    #################################################
    #################################################
    if USE_CSVdataLogger_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if CSVdataLogger_OPEN_FLAG != 1:
                print("Failed to open CSVdataLogger_ReubenPython3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPrint_ReubenPython2and3ClassObject_GUIparametersDict
    MyPrint_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MyPrint_FLAG),
                                                                    ("root", Tab_MyPrint),
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
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPrint_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPrint_OPEN_FLAG != 1:
                print("Failed to open MyPrint_ReubenPython2and3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
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
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG != 1:
                print("Failed to open MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_Keyboard_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        keyboard.on_press_key("esc", ExitProgram_Callback)
    #################################################
    #################################################

    #################################################
    #################################################
    #################################################
    print("Starting main loop 'test_program_for_CSVdataLogger_ReubenPython3Class.")
    StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()

    while(EXIT_PROGRAM_FLAG == 0):

        ####################################################
        ####################################################
        CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
        ####################################################
        ####################################################

        ################################################### GET's
        ###################################################
        if CSVdataLogger_OPEN_FLAG == 1:
            CSVdataLogger_ReubenPython3ClassObject_IsSavingFlag = CSVdataLogger_ReubenPython3ClassObject.IsSaving()
        else:
            CSVdataLogger_ReubenPython3ClassObject_IsSavingFlag = 0
        ###################################################
        ###################################################

        #################################################### GET's
        ####################################################
        if CSVdataLogger_OPEN_FLAG == 1:

            CSVdataLogger_MostRecentDict = CSVdataLogger_ReubenPython3ClassObject.GetMostRecentDataDict()

            if "Time" in CSVdataLogger_MostRecentDict:
                CSVdataLogger_MostRecentDict_Time = CSVdataLogger_MostRecentDict["Time"]
                CSVdataLogger_MostRecentDict_DataStreamingFrequency_CalculatedFromMainThread = CSVdataLogger_MostRecentDict["DataStreamingFrequency_CalculatedFromMainThread"]
                CSVdataLogger_MostRecentDict_AcceptNewDataFlag = CSVdataLogger_MostRecentDict["AcceptNewDataFlag"]
                CSVdataLogger_MostRecentDict_SaveFlag = CSVdataLogger_MostRecentDict["SaveFlag"]
                CSVdataLogger_MostRecentDict_DataQueue_qsize = CSVdataLogger_MostRecentDict["DataQueue_qsize"]
                CSVdataLogger_MostRecentDict_VariableNamesForHeaderList = CSVdataLogger_MostRecentDict["VariableNamesForHeaderList"]
                CSVdataLogger_MostRecentDict_FilepathFull = CSVdataLogger_MostRecentDict["FilepathFull"]

                #print("CSVdataLogger_MostRecentDict: " + str(CSVdataLogger_MostRecentDict))
        ####################################################
        ####################################################

        #################################################### SET's
        ####################################################

        ####################################################
        ControlInput_CalculatedValue_1 = GetLatestWaveformValue(CurrentTime_MainLoopThread, 
                                                                ControlInput_MinValue_1, 
                                                                ControlInput_MaxValue_1, 
                                                                ControlInput_Period_1, 
                                                                ControlInput_1)
        ####################################################

        ####################################################
        ControlInput_CalculatedValue_2 = GetLatestWaveformValue(CurrentTime_MainLoopThread, 
                                                                ControlInput_MinValue_2, 
                                                                ControlInput_MaxValue_2, 
                                                                ControlInput_Period_2, 
                                                                ControlInput_2)
        ####################################################

        ####################################################
        if CSVdataLogger_OPEN_FLAG == 1:
            CSVdataLogger_ReubenPython3ClassObject.AddDataToCSVfile_ExternalFunctionCall([CurrentTime_MainLoopThread,
                                                                                          ControlInput_CalculatedValue_1,
                                                                                          ControlInput_CalculatedValue_2])
        ####################################################

        ####################################################
        ####################################################

        #################################################### SET's
        ####################################################
        if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:

            ####################################################
            try:
                MyPlotterPureTkinterStandAloneProcess_MostRecentDict = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.GetMostRecentDataDict()

                if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess_MostRecentDict:
                    MyPlotterPureTkinterStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                    if MyPlotterPureTkinterStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag == 1:
                        if CurrentTime_MainLoopThread - LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess >= 0.040:
                            MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExternalAddPointOrListOfPointsToPlot(["Channel0", "Channel1"], [CurrentTime_MainLoopThread]*2, [ControlInput_CalculatedValue_1, ControlInput_CalculatedValue_2])

                            LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess = CurrentTime_MainLoopThread
            ####################################################

            ####################################################
            except:
                exceptions = sys.exc_info()[0]
                print("MyPlotterPureTkinterStandAloneProcess, exceptions: %s" % exceptions)
                traceback.print_exc()
            ####################################################

        ####################################################
        ####################################################

        time.sleep(0.010)
    #################################################
    #################################################
    #################################################

    ################################################# THIS IS THE EXIT ROUTINE!
    #################################################
    print("Exiting main program 'test_program_for_CSVdataLogger_ReubenPython3Class.")

    #################################################
    if CSVdataLogger_OPEN_FLAG == 1:
        CSVdataLogger_ReubenPython3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:
        MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    #################################################

##########################################################################################################
##########################################################################################################