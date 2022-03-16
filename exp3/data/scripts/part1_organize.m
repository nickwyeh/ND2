%% Organize  Data

% This script will organize study and test data from Experiment 3 and clean up variable names
% and responses. Study and test data will be combined for the quality
% control in the part2 script. This script requires the source data. 

% Step 1: Gather Participant ID and make directories
% Step 2:  Clean up variables to remove and load data
% Step 3: Subset study data
% Step 4: Subset test data
% Step 5: Combine study and test data structures
% Step 6 save test file with study data information
% Step 7: Load in demographics data and save participant log
%% Clear workspace
clear all;
clc;

%% Define main directories
% Directories
if ispc
    directories.top    = 'X:\EXPT\nd002\exp3\data';
elseif ismac
    directories.top    = '/Volumes/koendata/EXPT/nd002/exp3/data/';
elseif isunix
    directories.top    = '/koenlab/koendata/EXPT/nd002/exp3/data/';
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

% Make participant log data table
par_log_columns = {'OG_id' 'id' 'cb' 'list'};
par_log = cell2table( cell(length(participant_list),length(par_log_columns)), ...
    'VariableNames',par_log_columns );
%% Loop through participants
for pari = 1:length(participant_list)

    
    %% Step 1: Gather Participant ID and make directories
    % Convert participant to char type
    participant = participant_list{pari};
    
    % Get a new id
    id = sprintf('%03.0f',pari);
    og_id = participant;
    % Print info to screen
    fprintf('\n\nProcessing data for %s:\n\n',participant);
    
    % Make directory structure in data
    directories.par_source   = fullfile(directories.source, participant);
    directories.par_data     = fullfile(directories.raw, sprintf('sub-%s', id) );
    directories.par_analysis = fullfile(directories.data_files, sprintf('sub-%s', id) );
    
    % Make directories
    make_dirs({directories.par_data});
    
    %% Step 2:  Clean up variables to remove and load data
    % Define variables that are not needed 
    vars_to_remove = {'frameRate' 'date' 'expName' 'ran' 'order' 'visual_word_text_started' 'visual_word_text_stopped' ...
        'uninformed_cue_box_started' 'uninformed_cue_box_stopped' 'visual_word_fixation_started' 'visual_word_fixation_stopped' ...
        'visual_resp_started' 'visual_resp_stopped' 'visual_resp_keys' 'visual_resp_rt' 'OS' 'trials_order' 'trials_ran' 'trials_thisIndex'...
        'trials_thisN' 'trials_thisTrialN' 'trials_thisRepN' 'phase_progress' 'practice_key_resp_keys' 'practice_key_resp_rt'...
        'confirm_question_key_resp_keys' 'confirm_question_key_resp_rt' 'confirm_answer_key_resp_keys' 'confirm_answer_key_resp_rt'...
        'phases_thisRepN' 'phases_thisTrialN' 'phases_thisN' 'phases_thisIndex' 'phases_ran' 'phases_order'...
        'test_phase_thisRepN' 'test_phase_thisTrialN' 'test_phase_thisIndex' 'test_phase_ran' 'test_phase_order' 'test_phase_thisN'...
        'test_instructions' 'test_instruction_image' 'test_trials_thisRepN' 'test_trials_thisTrialN' 'test_trials_thisN' 'test_trials_thisIndex'...
        'test_trials_ran' 'test_trials_order' 'study_warning_key_resp_keys' 'study_warning_key_resp_rt'};
    
    % Load data
    source_study_test_file = fullfile( directories.par_source, sprintf('data_PARTICIPANT_study_test_online_proc_%s.csv', participant) ); 
    study_test_opts = detectImportOptions( source_study_test_file, 'FileType', 'text' );
    study_test_data = readtable( source_study_test_file, study_test_opts );
    study_test_data = study_test_data( :, ~ismember(study_test_data.Properties.VariableNames, vars_to_remove) );


    %% Step 3: Subset study data
    % Define the columns in the data to keep. 
    study_variables_to_keep = {'id' 'psychopyVersion' 'phase_name' 'study_phase' ...
        'word' 'manmade' 'shoebox' 'nletters' 'freq' 'nsyllables' 'concreteness' ...
        'old_new' 'study_judgment' 'cue_condition' 'cue_color' 'box_color' 'show_cue' 'show_nocue' ...
        'study_resp_key' 'study_resp' 'study_rt'};
    
    % Define the rows to keep in the data
    study_rows_to_keep = contains(study_test_data.phase_name,'study');
    n_study_rows = sum(study_rows_to_keep);
    if n_study_rows ~= 300
        error('There should be 300 rows in the study data for %s',participant);
    end
    
    % Subselect study_test_data to make study_data
    study_data = study_test_data(study_rows_to_keep,study_variables_to_keep);
    
    % Find the study_nr trials
    study_nr = isempty(study_data.study_resp_key) | ...
        ismember(study_data.study_resp_key, 'n/a');
    study_data.study_resp_key(study_nr) = {'n/a'}; % Make all study_resp_keys n/a
    study_data.study_rt(study_nr)       = -99;
    study_data.study_resp(study_nr)     = -99;
    study_data.study_good_trial         = double( ~study_nr );
    
    % Code for list and study counterbalancing 
    % If the first trial is informed 
    % A = informed, uninformed, uncued, uncued, uninformed, informed
    % B = uninformed, uncued, informed, informed, uncued, uninformed
    % C = uncued, informed, uninformed, uninformed, informed, uncued
    first_phase = study_data.phase_name{1};
    list = first_phase(end); % The last character is the list. Note it is a number coded as a string
    if contains(first_phase, 'uninformed')
        study_cb = 'B';
    elseif contains (first_phase, 'uncued')
        study_cb = 'C';
    else
        study_cb = 'A';
    end
    
    % Add study counterbalance(CB) and stimuli list
    study_data.study_cb(:) = study_cb;
    study_data.list(:)     = list;
    
    % Move them in the data table
    study_data = movevars(study_data,{'study_cb' 'list'},'After','id');
    
    % Update ID in  data
    study_data.id(:) = {id}; 

    % Create study_judgment accuracy variable.
    cap_no = {'N','n'};
    cap_yes = {'Y','y'};
    for yn = 1:size(study_data,1)
        if ismember(study_data.study_judgment(yn),'manmade')& ismember(study_data.manmade(yn),cap_no)
            study_data.study_judgment_correct_resp(yn) = 2;
        elseif ismember(study_data.study_judgment(yn),'manmade')& ismember(study_data.manmade(yn),cap_yes)
            study_data.study_judgment_correct_resp(yn) = 1;
        elseif ismember(study_data.study_judgment(yn),'shoebox')& ismember(study_data.shoebox(yn),cap_no)
            study_data.study_judgment_correct_resp(yn) = 2;
        elseif ismember(study_data.study_judgment(yn),'shoebox')& ismember(study_data.shoebox(yn),cap_yes)
            study_data.study_judgment_correct_resp(yn) = 1;
            
            
        end
    end
    % code stay/switch
    
    study_data.stayswitch                      = repmat({'na'},size(study_data,1),1); % initialize
    switch1        = zeros(size(study_data,1),1); % Initialize
    stay1   = zeros(size(study_data,1),1); % Initialize
    
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
    d = diff([0; stay1==1; 0]);
    startidx = find(d==1); %contains first stay value
    lgt = find(d==-1)-startidx ;%contains the number of consec stay trials for the start idx
    study_data.stayswitch_run                      = repmat({'na'},size(study_data,1),1); % initialize vector
    
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
    % find the start and number of consec switch trials
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
    
    
    %% Step 4: Subset test data
    % Define the variables for the test data to keep
    test_variables_to_keep = {'id' 'test_cb' 'word' 'old_new' 'study_judgment' ...
        'cue_condition' 'item_resp' 'item_rt' 'item_acc' 'old_new_resp' ...
        'sm_resp' 'sm_rt' 'sm_acc' };
    
    % Determine the test_rows to keep 
    test_rows_to_keep = contains(study_test_data.phase_name, '_crit');
    n_test_rows = sum(test_rows_to_keep);
    if n_test_rows ~= 450
        error('There should be 450 rows in the test data for %s',participant);
    end
    
    % Subselect trials for test data (Note you can use cell array of
    % strings to index columns in data tables. 
    test_data = study_test_data(test_rows_to_keep,test_variables_to_keep);
    
    % Add study CB to list
    test_data.study_cb(:) = study_cb;
    test_data.list(:)     = list;
    
    % Move them in the data table
    test_data = movevars(test_data,{'study_cb' 'list'},'After','id');
   
    % Convert some columns to double format 
    test_data.item_resp = cellfun(@str2double,test_data.item_resp);
    test_data.item_rt   = cellfun(@str2double,test_data.item_rt);
    test_data.item_acc  = cellfun(@str2double,test_data.item_acc);
    test_data.sm_resp   = cellfun(@str2double,test_data.sm_resp);
    test_data.sm_acc    = cellfun(@str2double,test_data.sm_acc);
    test_data.sm_rt     = cellfun(@str2double,test_data.sm_rt);
    
    % Check for empty response if item_resp or in sm_resp when an item_resp
    % was a 4, 5, or 6 (the latter is a source resp timeout and bad trial)
    bad_test_trials =  isnan(test_data.item_resp) | ...
        (ismember(test_data.item_resp,4:6) & isnan(test_data.sm_resp));
    test_data.test_good_trial = double(~bad_test_trials);
    
    % Update missing values to -99. Note that even item_resps that are a 4,
    % 5, or 6, but are missing a source response are treated as missing data
    % because we do not have the full data for that trial. 
    test_data.item_resp(bad_test_trials) = -99;
    test_data.item_rt(bad_test_trials)   = -99;
    test_data.item_acc(bad_test_trials)  = -99;
    test_data.sm_resp(bad_test_trials)   = -99;
    test_data.sm_rt(bad_test_trials)     = -99;
    test_data.sm_acc(bad_test_trials)    = -99;
    
    %Update test id
    test_data.id(:) = study_data.id(1);

    % Determine file names
    study_beh_file = fullfile(directories.par_data,sprintf('sub-%s_task-study.tsv',id));
    test_beh_file = fullfile(directories.par_data,sprintf('sub-%s_task-test.tsv',id));


    % Save data files
    writetable(study_data, study_beh_file, 'FileType', 'text','Delimiter','\t');
    %writetable(test_data, test_beh_file, 'FileType', 'text','Delimiter','\t');

    %% Step 5: Combine study and test data structures
    % Copy variables good_trial, study_nr, study_wrong_hand over
    test_data.study_resp       = -99*ones(size(test_data,1),1); % Initialize as all missing dat
    test_data.study_rt         = nan(size(test_data,1),1); % Initialize study_rt vector
    test_data.study_good_trial = ones(size(test_data,1),1); % Initialize study_good_trial variable as 1 (so all new items are good) 
    test_data.manmade          = cell(1,size(test_data,1))'; % Initialize
    test_data.shoebox          = cell(1,size(test_data,1))';% Initialize
    test_data.study_judgment_correct_resp = -99*ones(size(test_data,1),1); % Initialize as all missing dat
    idx = cellfun(@isempty,test_data.manmade); % Find the indexes of empty cell
    test_data.manmade(idx) = {'n/a'};         % Replace the empty cells with 'na'
     idx = cellfun(@isempty,test_data.shoebox); % Find the indexes of empty cell
    test_data.shoebox(idx) = {'n/a'};         % Replace the empty cells with 'na'
     test_data.stayswitch =  cell(1,size(test_data,1))';
    test_data.stayswitch_run =  cell(1,size(test_data,1))';
    % Find test_data rows with study_trials and add new data
    for trli = 1:size(test_data,1)
        
        % If a new item, skip it all
        if ismember(test_data.old_new(trli),'new')
            test_data.stayswitch(trli)       = {'new'};
            test_data.stayswitch_run(trli)   = {'new'};
            continue;
            
        else
            
            % Find the study index
            study_idx = find(ismember(study_data.word, test_data.word(trli)));
            
            % Copy into current trial of test_data
            test_data.study_resp(trli)       = study_data.study_resp(study_idx);
            test_data.study_rt(trli)         = study_data.study_rt(study_idx);
            test_data.study_good_trial(trli) = study_data.study_good_trial(study_idx);
            test_data.manmade(trli)          = study_data.manmade(study_idx);
            test_data.shoebox(trli)          = study_data.shoebox(study_idx);
            test_data.study_judgment_correct_resp(trli) = study_data.study_judgment_correct_resp(study_idx);
            test_data.stayswitch(trli)       = study_data.stayswitch(study_idx);
            test_data.stayswitch_run(trli)   = study_data.stayswitch_run(study_idx);
        end
        
    end 
    
    % Get an 'overall' good trial column for test data
    test_data.good_trial = test_data.study_good_trial & test_data.test_good_trial;

    %% Step 6 save test file with study data information
    % Determine file names
    combo_beh_file = fullfile(directories.par_data,sprintf('sub-%s_task-test.tsv',id));
    
    
    % Save data files
    writetable(test_data, combo_beh_file, 'FileType', 'text','Delimiter','\t');
    
    % Add info to participant log
    new_data = {participant id study_cb list};
    par_log{pari,:} = new_data;

end

%% Step 7: Load in demographics data and save participant log
% add in participant log information.
demo_data_file = fullfile( directories.source, sprintf('p2e3_demographics.csv') );
demo_opts = detectImportOptions( demo_data_file, 'FileType', 'text' );
demo_data = readtable( demo_data_file, demo_opts );
% select variables to add to participant log
demo_variables_to_keep = {'OG_id' 'Age' 'Gender' 'Ethnicity'};
demo_subset_data = demo_data(:,demo_variables_to_keep);
%Join participant log and demo_data
par_demo_log = join(par_log,demo_subset_data);
final_variables_to_keep ={'id' 'cb' 'list' 'Age' 'Gender' 'Ethnicity'};
final_par_demo_log = par_demo_log(:,final_variables_to_keep);
% Save the participant log
par_tsv_file = fullfile(directories.raw,'participants.tsv');
writetable(final_par_demo_log,par_tsv_file,'FileType','text','Delimiter','\t');