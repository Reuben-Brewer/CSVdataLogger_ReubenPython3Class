###########################

CSVdataLogger_ReubenPython3Class

Code (including ability to hook to Tkinter GUI) to save data in CSV format.
Includes code to automatically plot data in Excel.

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision I, 05/27/2025

Verified working on:

Python 3.11/3.12

Windows  10/11 64-bit

Raspberry Pi Bookworm

###########################

########################### Python module installation instructions, all OS's

############

test_program_for_CSVdataLogger_ReubenPython3Class.py

CSVdataLogger_ReubenPython3Class, ListOfModuleDependencies: ['future.builtins']

CSVdataLogger_ReubenPython3Class, ListOfModuleDependencies_TestProgram: ['keyboard', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class']

CSVdataLogger_ReubenPython3Class, ListOfModuleDependencies_NestedLayers: ['future.builtins', 'numpy', 'pexpect', 'psutil']

CSVdataLogger_ReubenPython3Class, ListOfModuleDependencies_All:['future.builtins', 'keyboard', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class', 'numpy', 'pexpect', 'psutil']

############

############

ExcelPlot_CSVdataLogger_ReubenPython3Code.py

ExcelPlot_CSVdataLogger_ReubenPython3Code, ListOfModuleDependencies_All:['pandas', 'win32com.client', 'xlsxwriter', 'xlutils.copy', 'xlwt']

pip install pywin32         #version 305.1 as of 10/17/24

pip install xlsxwriter      #version 3.2.0 as of 10/17/24. Might have to manually delete older version from /lib/site-packages if it was distutils-managed. Works overall, but the function ".set_size" doesn't do anything.

pip install xlutils         #version 2.0.0 as of 10/17/24

pip install xlwt            #version 1.3.0 as of 10/17/24

############

###########################
