%% Make ND0002 Stimulus Lists - Experiment 1
% This script makes the stimulus list for ND002. 
% This script was adopted from EEG37 conducted at UT Dallas. 
%
% Critical List
%   The critical list comprises 256 total studied words. Half of the words
%   will be assigned to the informed condition, and the other half will be
%   in the uninformed condition. Half of the trials in each condition will
%   be assigned to to the shoebox task, and the other half to the manmade
%   task. In each task, there will be an equal number of YES and NO
%   answers. No attempt is made to cross the Manmade and Shoebox YES and
%   NO answers in each condition.
%
% Self-Paced Practice List
%   This practice phase comprises 8 words, and is meant to introduce
%   participants to the encoding task with self-paced word
%   presentation. There will be 4 informed trials and 4 uninformed trials.
%   These will be intermixed.
%
% Regular Practice List
%   This practice phase comprises 16 words, and is a practice phase for
%   the experiment proper. Thus, it incorporates the timed aspects of the
%   tasks. The trial distrubtion (25% in each cell formed by crossing
%   informed/uninformed and manmade/shoebox factors) is identical to the
%   critical list. No feedback will be provided here. 

%% Define options
nLists = 64; % Number of stimulus lists to create
nTrialsPerCell = 64; % Number of trials per cell
minTrials = 80; % Number of trials needed to escape the while loop

%% Define perl command
syscmd = 'perl c:\perl64\bin\shuffle.pl -c"0 0 0 0 0 0 0 0 3 3" temp.txt > output.txt';

%% Directory setup and load stimulus lists
% Get main experiment directory
scriptDir = fileparts(mfilename('fullpath'));

% Add path
addpath(genpath('X:\ND\MATLAB\general'));

% Set stimsDir to scriptDir
stimsDir = scriptDir;

%% Load word lists
% Critical word list
critFile = fullfile(stimsDir,'critical_words.csv');
critWords = loadtxt(critFile,'verbose','off','delim',',','skipline',1);

% Extract header, and remove from critWords
cols = loadtxt(critFile,'verbose','off','delim',',','nlines',1);
newCols = ['setID' cols 'item_type' 'study_judgment' 'study_condition']; % Columns to write
    
% Load practice 1 List
sprac1File = fullfile(stimsDir,'prac1_study_words.csv');
sprac1List = loadtxt(sprac1File,'verbose','off','delim',',','skipline',0);

% Load practice 2 List
sprac2File = fullfile(stimsDir,'prac2_study_words.csv');
sprac2List = loadtxt(sprac2File,'verbose','off','delim',',','skipline',0);

% Load practice test
tpracFile = fullfile(stimsDir,'prac_test_words.csv');
tpracList = loadtxt(tpracFile,'verbose','off','delim',',','skipline',0);

%% Seed RNG
rng(29276); 

%% Create lists
for i = 1:nLists
    
    % Make the list folder and ID
    setID = sprintf('set%d',i);
    fprintf('create %s...\n',setID);
    
    % Make a folder
    setDir = fullfile(stimsDir,setID);
    if ~exist(setDir,'dir'), mkdir(setDir); end
    
    % Randomly select words
    while true
        
        % Randomize critWords
        critWords = randomize_matrix(critWords);
        
        % Split into two sets and find Yes/No
        manmade.all = critWords(1:192,:);
        manmade.yes = manmade.all(strcmpi(manmade.all(:,2),'Y'),:);
        manmade.no = manmade.all(strcmpi(manmade.all(:,2),'N'),:);
        shoebox.all = critWords(193:end,:);
        shoebox.yes = shoebox.all(strcmpi(shoebox.all(:,3),'Y'),:);
        shoebox.no = shoebox.all(strcmpi(shoebox.all(:,3),'N'),:);
        
        if size(manmade.yes,1) > minTrials && size(manmade.no,1) > minTrials && ...
                size(shoebox.yes,1) > minTrials && size(shoebox.no,1) > minTrials
            break
        end
        
    end
    
    % Divide old words into 4 ST phases
    sel = 1:nTrialsPerCell/2;
    manWords.pre = [vertcat(manmade.yes(sel,:),manmade.no(sel,:)) ...
        repmat({'old'},nTrialsPerCell,1) repmat({'manmade'},nTrialsPerCell,1) ...
        repmat({'informed'},nTrialsPerCell,1)];
    sel = sel + nTrialsPerCell/2;
    manWords.post = [vertcat(manmade.yes(sel,:),manmade.no(sel,:)) ...
        repmat({'old'},nTrialsPerCell,1) repmat({'manmade'},nTrialsPerCell,1) ...
        repmat({'uninformed'},nTrialsPerCell,1)];
    sel = 1:nTrialsPerCell/2;
    shoeWords.pre = [vertcat(shoebox.yes(sel,:),shoebox.no(sel,:)) ...
        repmat({'old'},nTrialsPerCell,1) repmat({'shoebox'},nTrialsPerCell,1) ...
        repmat({'informed'},nTrialsPerCell,1)];
    sel = sel + nTrialsPerCell/2;
    shoeWords.post = [vertcat(shoebox.yes(sel,:),shoebox.no(sel,:)) ...
        repmat({'old'},nTrialsPerCell,1) repmat({'shoebox'},nTrialsPerCell,1) ...
        repmat({'uninformed'},nTrialsPerCell,1)];
    
    % Create old word lists
    oldWords = vertcat(manWords.pre, manWords.post, shoeWords.pre, shoeWords.post);
    
    % Get new words
    temp = vertcat( ...
        manmade.yes(sel(end)+1:end,:), ...
        manmade.no(sel(end)+1:end,:), ...
        shoebox.yes(sel(end)+1:end,:), ...
        shoebox.no(sel(end)+1:end,:));
    newWords = [temp repmat({'new'},128,1) repmat({'new'},128,1) repmat({'new'},128,1)];
    
    %% Make study list
    % Write to TSV file
    cell2csv('temp.txt',[oldWords repmat({''},size(oldWords,1),1)],sprintf('\t'));
    
    % Run command
    [s,r] = system(syscmd);
    
    % Load the list
    studyList = loadtxt('output.txt','verbose','off','delim',sprintf('\t'));
    delete temp.txt output.txt;
    
    % Add set ID then add header row
    studyList = [repmat({setID},size(studyList,1),1) studyList];
    studyList = vertcat(newCols,studyList);
    
    % Write study list to csv file
    studyFile = fullfile(setDir,sprintf('%s_crit_study.csv',setID));
    cell2csv(studyFile,studyList,',');
    
    %% Make test list
    testWords = vertcat(oldWords,newWords);
    
    % Write to TSV file
    cell2csv('temp.txt',[testWords repmat({''},size(testWords,1),1)],sprintf('\t'));
    
    % Run command
    [s,r] = system(syscmd);
    
    % Load the list
    testList = loadtxt('output.txt','verbose','off','delim',sprintf('\t'));
    delete temp.txt output.txt;
    
    % Add set ID then add header row
    testList = [repmat({setID},size(testList,1),1) testList];
    testList = vertcat(newCols,testList);
    
    % Write study list to csv file
    testFile = fullfile(setDir,sprintf('%s_crit_test.csv',setID));
    cell2csv(testFile,testList,',');
    
    %% Make practice lists
    % Self-Paced Study Practice 1
    sprac1List = [repmat({setID},size(sprac1List,1),1) sprac1List];
    cell2csv(fullfile(setDir,sprintf('%s_prac1_study.csv',setID)),sprac1List,',');   
    
    % Study Practice 2
    sprac2List = [repmat({setID},size(sprac2List,1),1) sprac2List];
    cell2csv(fullfile(setDir,sprintf('%s_prac2_study.csv',setID)),sprac2List,',');   
    
    % Test Practice 
    tpracList = [repmat({setID},size(tpracList,1),1) tpracList];
    cell2csv(fullfile(setDir,sprintf('%s_prac_test.csv',setID)),tpracList,',');   
    
end
    
    
    

