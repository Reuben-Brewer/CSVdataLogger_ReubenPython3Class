###########################

CSVdataLogger_ReubenPython3Class

Code (including ability to hook to Tkinter GUI) to save data in CSV format.
Includes code to automatically plot data in Excel and MATLAB.

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision Q, 12/22/2025

Verified working on:

Python 3.11/12/13

Windows 10/11 64-bit

Raspberry Pi Bookworm

###########################

########################### Python module installation instructions, all OS's

############

test_program_for_CSVdataLogger_ReubenPython3Class.py

CSVdataLogger_ReubenPython3Class, ListOfModuleDependencies: ['EntryListWithBlinking_ReubenPython2and3Class', 'ReubenGithubCodeModulePaths']

CSVdataLogger_ReubenPython3Class, ListOfModuleDependencies_TestProgram: ['keyboard', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'ReubenGithubCodeModulePaths']

CSVdataLogger_ReubenPython3Class, ListOfModuleDependencies_NestedLayers: ['GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class', 'numpy', 'pexpect', 'psutil', 'pyautogui', 'ReubenGithubCodeModulePaths']

CSVdataLogger_ReubenPython3Class, ListOfModuleDependencies_All:['EntryListWithBlinking_ReubenPython2and3Class', 'GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class', 'keyboard', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'numpy', 'pexpect', 'psutil', 'pyautogui', 'ReubenGithubCodeModulePaths']

############

############

ExcelPlot_CSVdataLogger_ReubenPython3Code.py

ExcelPlot_CSVdataLogger_ReubenPython3Code, ListOfModuleDependencies_All:['pandas', 'win32com.client', 'xlsxwriter', 'xlutils.copy', 'xlwt']

pip install pywin32=311

pip install xlsxwriter==3.2.9 #Might have to manually delete older version from /lib/site-packages if it was distutils-managed. Works overall, but the function ".set_size" doesn't do anything.

pip install xlutils==2.0.0

pip install xlwt==1.3.0

############

###########################
