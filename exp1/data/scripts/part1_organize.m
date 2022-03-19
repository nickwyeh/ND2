%% Organize data from sourcedata
% To do, clean up stay/switch code with more informative variable names.
%% Clear workspace
clear all;
clc;

%% Define main directories
% Directories
if ispc
    directories.top    = 'X:\EXPT\nd002\exp1\data';
elseif ismac
    directories.top    = '/Volumes/koendata/EXPT/nd002/exp1/data/';
elseif isunix
    directories.top    = '/koenlab/koendata/EXPT/nd002/exp1/data/';
end
directories.raw        = fullfile(directories.top, 'raw');
directories.source     = fullfile(directories.top, 'sourcedata');
directories.analyses   = fullfile(directories.top, 'analyses');
directories.data_files = fullfile(directories.analyses, 'data_files');

% Make directories if needed
make_dirs({directories.analyses directories.data_files});

%% Get participant list to organize
% Read all in source data
participant_list = dir(fullfile(directories.source,'sub-*'));
participant_list = {participant_list.name};

%% Make output for participant log columns
% Make output data table
par_log_columns = {'uid' 'id' 'list'};
par_log = cell2table( cell(length(participant_list),length(par_log_columns)), ...
    'VariableNames',par_log_columns );

%% Loop through participants
for pari = 1:length(participant_list)
    
    %% Step 1: Gather Participant ID and make directories
    % Convert participant to char type
    participant = participant_list{pari};
    
    % Get a new id
    id = sprintf('%03.0f',pari);
    
    % Print info to screen
    fprintf('\n\nOrganizing data for %s\n',participant);
    
    % Make directory structure in data
    directories.par_source   = fullfile(directories.source, participant);
    directories.par_data     = fullfile(directories.raw, sprintf('sub-%s', id) );
    directories.par_analysis = fullfile(directories.data_files, sprintf('sub-%s', id) );
    
    % Make directories
    make_dirs({directories.par_data});
    
    %% Step 2: Load and clean up study data variables
    % Load study data
    source_study_file = fullfile( directories.par_source, sprintf('%s_task-study_beh.tsv', participant) );
    study_opts        = detectImportOptions( source_study_file, 'FileType', 'text' );
    study_data        = readtable( source_study_file, study_opts );
    
    % Check for accurate number of rows in data file
    if size(study_data,1) ~= 256
        error('There should be 256 rows in the study data for %s',participant);
    end
    
    % Define variablers to remove and remove them
    if ismember('frameRate',study_data.Properties.VariableNames)
        study_vars_to_remove = {'frameRate' 'date' 'expName' 'ran' 'order' 'setID' 'TrialNumber'};
    else
        study_vars_to_remove = {'date' 'expName' 'ran' 'order' 'setID' 'TrialNumber'};
    end
    study_data(:,study_vars_to_remove) = [];
    
    % Update id with new id
    study_data.id(:) = str2double(id);
    
    % Add a study_resp column, update it to a numerical code, and code for
    % a wrong_hand_resp
    study_data.study_resp = repmat(-99,length(study_data.study_resp_keys),1);
    study_data.correct_hand = ones(length(study_data.study_resp_keys),1);
    for respi = 1:length(study_data.study_resp_keys)
        
        % Get the current trial's response and study judgment
        this_resp = study_data.study_resp_keys(respi);
        this_task = study_data.study_judgment(respi);
 
        % Code for the response code (1=yes, 2=no)
        if ismember(this_resp,{'j' 'f'})
            study_data.study_resp(respi) = 1;
        elseif ismember(this_resp,{'d' 'k'})
            study_data.study_resp(respi) = 2;
        elseif strcmpi(this_resp,'None')
            study_data.study_resp_keys{respi} = 'n/a';
            study_data.study_resp_rt(respi) = -99;
        end
        
        % Code for wrong hand
        if strcmpi(this_task,'shoebox') && ismember(this_resp,{'j' 'k'})
            study_data.correct_hand(respi) = 0;
        elseif strcmpi(this_task,'manmade') && ismember(this_resp,{'f' 'd'})
            study_data.correct_hand(respi) = 0;
        end
    end
    
    % Code for study_nr and bad trials
    study_data.study_nr = double(study_data.study_resp == -99);
    study_data.good_trial = double( study_data.correct_hand & ~study_data.study_nr );
    
    % Create study_judgment accuracy variable for reviewer comments.
    cap_no = {'N','n'};
    cap_yes = {'Y','y'};
    for yn = 1:size(study_data,1)
        if ismember(study_data.study_judgment(yn), 'manmade') & ismember(study_data.manmade(yn), cap_no)
            study_data.study_judgment_correct_resp(yn) = 2;
        elseif ismember(study_data.study_judgment(yn), 'manmade') & ismember(study_data.manmade(yn), cap_yes)
            study_data.study_judgment_correct_resp(yn) = 1;
        elseif ismember(study_data.study_judgment(yn), 'shoebox') & ismember(study_data.shoebox(yn), cap_no)
            study_data.study_judgment_correct_resp(yn) = 2;
        elseif ismember(study_data.study_judgment(yn), 'shoebox') & ismember(study_data.shoebox(yn), cap_yes)
            study_data.study_judgment_correct_resp(yn) = 1;
        end
    end
    
    % Add code to look at stay/switch trials. 
    study_data.stayswitch = repmat({'na'},size(study_data,1),1); 
    switch1               = zeros(size(study_data, 1),1);
    stay1                 = zeros(size(study_data,1),1);
    
    %Stay trials are shoebox-shoebox, or manmade-manmade
    %Switch trials are shoebox-manmade,manmade-shoebox
    for i = 1:size(study_data(:,1))
        if i == 1
            study_data.stayswitch(i) = {'switch'};
            switch1(i) = 1;
        elseif ismember(study_data.study_judgment(i-1), study_data.study_judgment(i))
            study_data.stayswitch(i) = {'stay'};
            stay1(i) = 1;
        else
            study_data.stayswitch(i) = {'switch'};
            switch1(i) = 1;
            
        end
        
    end
    % find start and lengeth of stay trials
    % To do: clean up variable names with informative names.
    d = diff([0; stay1==1; 0]);
    startidx = find(d==1); %contains first stay value
    lgt = find(d==-1)-startidx ;%contains the number of consec stay trials for the start idx
    study_data.stayswitch_run   = repmat({'na'},size(study_data,1),1); 
    
    % code stay0, stay1, stay2....stayn'th values.
    for i = 1:length(startidx)
        counter = 0; %  counter for consec stay trials
        for ii = 1:lgt(i)
            % combine stay with counter
            a = num2str(counter);
            b = 'stay';
            c = [b a];
            
            if ii == 1
                study_data.stayswitch_run(startidx(i)) = {c}; %set first occurance as stay0
                
            else
                si = startidx(i);
                si = si + counter;
                study_data.stayswitch_run(si) = {c};
            end
            counter = counter + 1;
        end
    end
    % find the start and number of consecutive switch trials
    % To do: clean up variable names.
    d = diff([0; switch1==1; 0]);
    startidx = find(d==1);
    lgt = find(d==-1)-startidx;
    for i = 1:length(startidx)
        counter = 0;
        for ii = 1:lgt(i)
            a = num2str(counter);
            b = 'switch';
            c = [b a];
            
            if ii == 1
                study_data.stayswitch_run(startidx(i)) = {c};
            else
                si = startidx(i);
                si = si + counter;
                study_data.stayswitch_run(si) = {c};
            end
            counter = counter + 1;
        end
    end
    
    % Reorder and rename data columns
    new_col_order = {'id' 'stim_set' 'psychopyVersion'  'word' 'manmade' 'shoebox' ...
        'nletters' 'freq' 'nsyllables' 'concreteness' 'item_type' 'study_judgment' ...
        'study_condition' 'study_resp_keys' 'study_resp' 'study_resp_rt' ...
        'correct_hand' 'study_judgment_correct_resp' 'study_nr' 'good_trial' 'stayswitch' 'stayswitch_run'};
    study_data = study_data(:,new_col_order);
    cols_to_rename = {'item_type' 'study_condition' 'study_resp_keys' 'study_resp_rt'};
    new_col_names  = {'old_new' 'cue_condition' 'study_resp_key' 'study_rt'};
    study_data.Properties.VariableNames(cols_to_rename) = new_col_names;
    
    %% Step 3: Load and clean up test data
    % Load study data
    source_test_file = fullfile( directories.par_source, sprintf('%s_task-test_beh.tsv', participant) );
    test_opts        = detectImportOptions( source_test_file, 'FileType', 'text' );
    test_data        = readtable( source_test_file, test_opts );
    
    % Check for accurate number of rows in data file
    if size(test_data,1) ~= 384
        error('There should be 384 rows in the test data for %s',participant);
    end
    
    % Define variablers to remove and remove them
    if ismember('frameRate',test_data.Properties.VariableNames)
        test_vars_to_remove = {'frameRate' 'date' 'expName' 'ran' 'order' 'setID' 'TrialNumber'};
    else
        test_vars_to_remove = {'date' 'expName' 'ran' 'order' 'setID' 'TrialNumber'};
    end
    test_data(:,test_vars_to_remove) = [];
    
    % Update id with new id
    test_data.id(:) = str2double(id);
    
    % Reorder and rename data columns
    new_col_order = {'id' 'stim_set' 'psychopyVersion'  'word' 'manmade' 'shoebox' ...
        'nletters' 'freq' 'nsyllables' 'concreteness' 'item_type' 'study_judgment' ...
        'study_condition' 'test_resp_response' 'test_resp_rt' };
    test_data = test_data(:,new_col_order);
    cols_to_rename = {'item_type' 'study_condition' 'test_resp_response' 'test_resp_rt'};
    new_col_names  = {'old_new' 'cue_condition' 'test_resp' 'test_rt'};
    test_data.Properties.VariableNames(cols_to_rename) = new_col_names;
    
    %% Step 4: Combine Study and Test data Tables
    % Join test_resp and test_rt to study_data
    study_data = join(study_data,test_data,'Keys','word','RightVariables',{'test_resp' 'test_rt'});
    test_data.study_judgment_correct_resp = -99*ones(size(test_data,1),1); % Initialize as all missing dat
    test_data.stayswitch =  cell(1,size(test_data,1))';
    test_data.stayswitch_run =  cell(1,size(test_data,1))';
    % Join study_resp, study_rt, correct_hand, study_nr, study_good_trial
    % Find test_data rows with study_trials and add new data
    for trli = 1:size(test_data,1)
        
        if ismember(test_data.old_new(trli),'new')
            
            test_data.study_resp(trli)   = -99;
            test_data.study_rt(trli)     = -99;
            test_data.correct_hand(trli) = 0; % 1/22 nick changed from 1 to 0
            test_data.study_nr(trli)     = 0;
            test_data.good_trial(trli)   = 1;
            test_data.stayswitch(trli)       = {'new'};
            test_data.stayswitch_run(trli)   = {'new'};
            
        else
            
            % Find the study index
            study_idx = find(ismember(study_data.word, test_data.word(trli)));
            
            % Copy into current trial of test_data
            test_data.study_resp(trli)   = study_data.study_resp(study_idx);
            test_data.study_rt(trli)     = study_data.study_rt(study_idx);
            test_data.correct_hand(trli) = study_data.correct_hand(study_idx);% 1/22 nick changed from study_nr to correct_hand
            test_data.study_nr(trli)     = study_data.study_nr(study_idx);
            test_data.good_trial(trli)   = study_data.good_trial(study_idx);
            test_data.study_judgment_correct_resp(trli) = study_data.study_judgment_correct_resp(study_idx);
            test_data.stayswitch(trli)       = study_data.stayswitch(study_idx);
            test_data.stayswitch_run(trli)   = study_data.stayswitch_run(study_idx);
            
        end
        
    end
    
    %% Step 5: Save the data files
    % Save study data
    study_out_file = fullfile(directories.par_data, sprintf('sub-%s_task-study.tsv',id));
    writetable(study_data, study_out_file, 'FileType','text','Delimiter','\t');
    
    % Save test data
    test_out_file = fullfile(directories.par_data, sprintf('sub-%s_task-test.tsv',id));
    writetable(test_data, test_out_file, 'FileType','text','Delimiter','\t');
    
    %% Step 6: Update participant log
    % Add row for this participant to the participant log
    par_log(pari,:) = {strrep(participant,'sub-','') id test_data.stim_set(1)};
    
end

%% Save the participant log to BIDS
par_tsv_file = fullfile(directories.raw,'participants.tsv');
writetable(par_log,par_tsv_file,'FileType','text','Delimiter','\t');