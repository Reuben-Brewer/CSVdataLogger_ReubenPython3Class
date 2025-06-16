% Reuben Brewer, Ph.D.
% reuben.brewer@gmail.com
% www.reubotics.com
% 
% Apache 2 License
% Software Revision L, 06/16/2025
% 
% Verified working on: MATLAB R2024a.
% 
% __author__ = 'reuben.brewer'

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function ConvertedColumnData = ParseNumericColumn(ColumnDataAsCells, ColumnIndexInt)
%PARSESNUMERICCOLUMN Converts a column from a cell array to numeric values.
%   ConvertedColumnData = ParseNumericColumn(ColumnDataAsCells, ColumnIndexInt)
%
%   Inputs:
%       ColumnDataAsCells  - full cell array from readcell()
%       ColumnIndexInt  - the column number to extract (e.g. 1 for first column)
%
%   Output:
%       ConvertedColumnData - a numeric column vector (NaN if conversion fails)

    ColumnDataAsCells = ColumnDataAsCells(2:end, ColumnIndexInt); % Extract column, skip header (assumed in row 1)

    ColumnDataAsCellsCleaned = cellfun(@(s) strrep(strtrim(string(s)), '+', ''), ColumnDataAsCells, 'UniformOutput', false); % Clean strings: remove '+' and trim whitespace

    ConvertedColumnData = cellfun(@str2double, ColumnDataAsCellsCleaned); % Convert to double

end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clc;
clear;
close all;
format longG;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
set(0, 'defaultTextInterpreter', 'none'); %Turn off the default LaTex intepreter so that underscores don't become exponents.
set(0, 'defaultAxesTickLabelInterpreter', 'none'); %Turn off the default LaTex intepreter so that underscores don't become exponents.
set(0, 'defaultLegendInterpreter', 'none'); %Turn off the default LaTex intepreter so that underscores don't become exponents.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
FontName = "Arial"
FontSize = 12

set(0, 'defaultAxesFontName', FontName); %Also takes care of the legend
set(0, 'defaultAxesFontSize', FontSize); %Also takes care of the legend
set(0, 'defaultTextFontName', FontName);
set(0, 'defaultTextFontSize', FontSize);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
FigureWidth = 640;
FigureHeight = 480;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CSVfileNameNoExtension = "ReubenTest_Trial_1_06_16_2025---13_06_17"

TitleString = "MATLAB_TestLoadAndPlotCSV_CSVdataLogger_ReubenPython3Class"
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CSVdirectory = "C:\CSVfiles\";
addpath(CSVdirectory);
CSVdata = readcell(CSVfileNameNoExtension + ".csv"); %readmatrix is only for numerical data

[NumberOfRows, NumberOfColumns] = size(CSVdata)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Time = ParseNumericColumn(CSVdata, 1);
PeriodicInput_CalculatedValue_1 = ParseNumericColumn(CSVdata, 2); 
PeriodicInput_CalculatedValue_2 = ParseNumericColumn(CSVdata, 3);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
try

    NoteToAddToFile_Literal = string(CSVdata(1, NumberOfColumns-1))
    
    if NoteToAddToFile_Literal == "NoteToAddToFile"
        NoteToAddToFile_Actual = "NoteToAddToFile: " + string(CSVdata(1, NumberOfColumns))
    else
        NoteToAddToFile_Actual = "NoteToAddToFile:"
    end

catch

    NoteToAddToFile_Actual = "NoteToAddToFile:"

end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Figure_1 = figure("Name", "PeriodicInput_CalculatedValue_1/2");
Figure_1.Position = [0, FigureHeight, FigureWidth, FigureHeight];

yyaxis left;
plot(Time, PeriodicInput_CalculatedValue_1, 'LineStyle', '-', 'LineWidth', 1, 'Color', 'b');
ylabel('PeriodicInput_CalculatedValue_1');

yyaxis right;
plot(Time, PeriodicInput_CalculatedValue_2, 'LineStyle', '-', 'LineWidth', 1, 'Color', [1, 0.5, 0]);  %orange = [1, 0.5, 0];  % RGB triplet
ylabel('PeriodicInput_CalculatedValue_2');

xlabel('Time (S)');
title({TitleString, CSVfileNameNoExtension, "PeriodicInput_CalculatedValue_1/2 vs Time", NoteToAddToFile_Actual});
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Input = PeriodicInput_CalculatedValue_1;
Output = PeriodicInput_CalculatedValue_2;

N = 1; %PolyfitNorder
PolyfitModel_OutputVsInput = polyfit(Input, Output, N);

PolyfitModel_OutputVsInput

Figure_OutputVsInput = figure("Name", "OutputActualAndEstimatedVsTime");
Figure_OutputVsInput.Position = [2*FigureWidth, FigureHeight, FigureWidth, FigureHeight];
plot(Time, Output,'b.'); %ACTUAL/MEASURED

hold on;
PolyfitDetailsString = string("Polyfit (Order N = " + num2str(N) + "): [");

OutputPredictedFromPolyfit = zeros(length(Input), 1);
for I = 1:1:N+1

    OutputPredictedFromPolyfit = OutputPredictedFromPolyfit + PolyfitModel_OutputVsInput(I)*Input.^((N+1)-I);

    PolyfitDetailsString = PolyfitDetailsString + num2str(PolyfitModel_OutputVsInput(I));

    if I < N + 1
        PolyfitDetailsString = PolyfitDetailsString + ", ";
    end
end

PolyfitDetailsString = PolyfitDetailsString + "]";

plot(Time, OutputPredictedFromPolyfit,'g.');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ErrorThresholdForTrackingInDeg = 0.2;
Time__OnlyPointsThatTripErrorTrackingThreshold = 0;
Output__OnlyPointsThatTripErrorTrackingThreshold = 0;
ErrorOfPrediction = zeros(length(Input), 1);
for Index = 1:1:length(ErrorOfPrediction)
    ErrorOfPrediction(Index) = Output(Index) - OutputPredictedFromPolyfit(Index);

    if ErrorOfPrediction(Index) >= ErrorThresholdForTrackingInDeg
        Time__OnlyPointsThatTripErrorTrackingThreshold = [Time__OnlyPointsThatTripErrorTrackingThreshold; Time(Index)];
        Output__OnlyPointsThatTripErrorTrackingThreshold = [Output__OnlyPointsThatTripErrorTrackingThreshold; Output(Index)];
    end
    
end

Time__OnlyPointsThatTripErrorTrackingThreshold = Time__OnlyPointsThatTripErrorTrackingThreshold(2:end); %Remove the initial (0, 0).
Output__OnlyPointsThatTripErrorTrackingThreshold = Output__OnlyPointsThatTripErrorTrackingThreshold(2:end); %Remove the initial (0, 0).

plot(Time, ErrorOfPrediction,'r.');
ErrorPlotHandle = plot(Time__OnlyPointsThatTripErrorTrackingThreshold, Output__OnlyPointsThatTripErrorTrackingThreshold,'LineStyle', 'none', 'Marker', 's', 'Color', 'm', 'MarkerFaceColor', 'm', "MarkerSize", 7);
%isempty(ErrorPlotHandle)

legend("Actual Output", "Predicted Output (Estimated From Polyfit on Input)", "Error", "OverThreshold");
title({TitleString, CSVfileNameNoExtension, "Output (Actual/Measured, Predicted via Polyfit) Vs Time with,", PolyfitDetailsString, NoteToAddToFile_Actual});

Mean_ErrorOfPrediction = mean(ErrorOfPrediction)
Std_ErrorOfPrediction = std(ErrorOfPrediction)
Max_ErrorOfPrediction = max(abs(ErrorOfPrediction))
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%