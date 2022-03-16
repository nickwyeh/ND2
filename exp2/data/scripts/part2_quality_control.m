%%Quality Control Data

% This script performs some quality
% control checks to test for good data. This follows the pre-registered
% criteria found on OSF (https://osf.io/5zre9)for exp2. These include:
%
% 1) Overall memory performance < .10 (determined by Hit Rate - False Alarm
%    Rate metric collapsed across study condition)
% 2) Multiple responses (collapsed across conditions). 
% 3) Source memory performance <  .05
% 4) Proportion of excluded test trials < .2
% 5) Fewer than 10% of confidence responses in the 2-5 bins (collapsed
%    across item type and study condition). 
%
% Subjects excluded for one of the above reasons are labelled 'bad'
% A participant log noting good and bad data is merged with participant log
% from part1_organize script


% Step 1: Gather Participant ID and make directories
% Step 2 load data and set up
% Step 3 Compute the proportion of excluded study trials < .2
% Step 4 Compute the proportion of excluded test trials < .2
% Step 5 item pr exclusion < .1
% Step 6 Source memory pR on good trials
% Step 7 Proportion of Confidence Bin 2-5 Use >=.1
% Step 8 Determine if good or bad data
% Step 9: Save the combined participant log to data files folder for part3_analyze.m script
%% Clear workspace
clear all;
clc;

%% Define main directories
% Directories
if ispc
    directories.top    = 'X:\EXPT\nd002\exp2\data';
elseif ismac
    directories.top    = '/Volumes/koendata/EXPT/nd002/exp2/data/';
elseif isunix
    directories.top    = '/koenlab/koendata/EXPT/nd002/exp2/data/';
end
directories.raw        = fullfile(directories.top, 'raw');
directories.source     = fullfile(directories.top, 'sourcedata');
directories.analyses   = fullfile(directories.top, 'analyses');
directories.data_files = fullfile(directories.analyses, 'data_files');

% Make directories if needed
make_dirs({directories.analyses directories.data_files});

% Read in participants.tsv file from raw
par_log_file = fullfile(directories.raw, 'participants.tsv');
par_log_opts = detectImportOptions(par_log_file, 'FileType', 'text' );
par_log      = readtable( par_log_file, par_log_opts );

% Make cells to store bad participants and for what reason
bad_other  = {}; % For the fire alarm and technical issues
bad_mem    = {};
bad_study  = {};
bad_test   = {};
bad_conf   = {};
bad_source = {};

% Add new columns to par_log
par_log.status(:)         = {'good'};
par_log.p_bad_study(:)    = 0;
par_log.p_bad_test(:)     = 0;
par_log.p_conf_not6or1(:) = 0;
par_log.item_pr(:)        = 0;
par_log.source_pr(:)      = 0;


%% Loop through participants
for pari = 1:size(par_log,1)
    
    %% Step 1: Gather Participant ID and make directories
  
    % Get  id
    id = sprintf('%03.0f',par_log.id(pari));
    % Print info to screen
    fprintf('\n\nProcessing data for %s:\n\n',id);
    
    % Make directory structure in data
    directories.par_data     = fullfile(directories.raw, sprintf('sub-%s', id) );
    directories.par_data     = fullfile(directories.raw, sprintf('sub-%s', id) );
    directories.par_analysis = fullfile(directories.data_files, sprintf('sub-%s', id) );
    
    % Make directories
    make_dirs({directories.par_data});
       
    %% Step 2 load data and set up
    % Load data
    test_file = fullfile( directories.par_data, sprintf('sub-%s_task-test.tsv', id) );
    test_opts = detectImportOptions( test_file, 'FileType', 'text' );
    test_data = readtable( test_file, test_opts );
    
    % Print info to screen
    fprintf('TESTING DATA QUALITY AND EXCLUSION CRITERIA:\n')
    
    % Assign study cb and list
    study_cb = test_data.study_cb{1};
    list = test_data.list(1);
    
    % Initialize all values (start as true)
    study_resp_rate_good  = true; % proportion of excluded study trials < .2
    test_resp_rate_good   = true; % proportion of test response timeouts below ###
    mem_perf_good         = true; % item pR >= .1
    source_perf_good      = true; % source pR >= .05
    conf_resp_rate_good   = true; % proportion use of confidence bins 2-5 >= .1
    
    %% Step 3 Compute the proportion of excluded study trials < .2
    pBad_study = mean(~test_data.study_good_trial(ismember(test_data.old_new,'old')));
    if pBad_study > .2, study_resp_rate_good = false; end
    fprintf('\tpBad Study Trials = %0.3f ', pBad_study);
    if study_resp_rate_good 
        fprintf('(GOOD)\n'); 
    else
        fprintf('(BAD)\n'); 
        bad_study = vertcat(bad_study,id);
    end
        % Update participant log with values
    par_log.p_bad_study(pari) = pBad_study;
    
    %% Step 4 Compute the proportion of excluded test trials < .2
    pBad_test = mean(~test_data.test_good_trial);
    if pBad_test > .2, test_resp_rate_good = false; end
    fprintf('\tpBad Test Trials = %0.3f ', pBad_test);
    if test_resp_rate_good 
        fprintf('(GOOD)\n'); 
    else
        fprintf('(BAD)\n'); 
        bad_test = vertcat(bad_test,id);
    end
        % Update participant log with values
    par_log.p_bad_test(pari) = pBad_test;
    %% Step 5 item pr exclusion < .1
    % Hit - FA of .1 across all conditions
    % old responses are item_resp of 4-guess old, 5-maybe old, 6-sure old
    old_trials = ismember(test_data.old_new,'old') & test_data.good_trial;
    new_trials = ismember(test_data.old_new,'new') & test_data.good_trial;
    old_resp   = ismember(test_data.item_resp,4:6) & test_data.good_trial;
    item_hits  = old_trials & old_resp;
    item_fas   = new_trials & old_resp;
    item_pHit = sum(item_hits)/sum(old_trials);
    item_pFA  = sum(item_fas)/sum(new_trials);
    item_pr   = item_pHit - item_pFA;
    if item_pr < .1, mem_perf_good = false; end
    fprintf('\tItem pR = %0.3f ', item_pr)
    if mem_perf_good
        fprintf('(GOOD)\n');
    else
        fprintf('(BAD)\n');
        bad_mem = vertcat(bad_mem,id);
    end
    
        % update participant log with values
    par_log.item_pr(pari) = item_pr;
    
    %% Step 6 Source memory pR on good trials
    % Code source accuracy as shoebox response (sm_resp==4) to a shoebox
    % item OR a manmande response (sm_resp==5) to a manmade item.
    source_cor = (test_data.sm_resp==4 & ismember(test_data.study_judgment,'shoebox')) | ...
        (test_data.sm_resp==5 & ismember(test_data.study_judgment,'manmade')) ;
    source_phits    = sum(source_cor)/sum(item_hits);
    source_pdk      = sum( test_data.sm_resp(item_hits) == 6) / sum(item_hits);
    source_pr = (source_phits-(.5*(1-source_pdk))) / (1-(.5*(1-source_pdk)));
    if source_pr < .05, source_perf_good = false; end
    fprintf('\tSource pHit = %0.3f \n', source_phits)
    fprintf('\tSource pDK  = %0.3f \n', source_pdk)
    fprintf('\tSource pR = %0.3f ', source_pr)
    if source_perf_good
        fprintf('(GOOD)\n');
    else
        fprintf('(BAD)\n');
        bad_source = vertcat(bad_source,id);
    end
            % Update participant log with values
    par_log.source_pr(pari) = source_pr;

    
    %% Step 7 Proportion of Confidence Bin 2-5 Use >=.1
    test_conf_not6or1 = ismember(test_data.item_resp, [2 3 4 5]) & test_data.good_trial;
    pNot6or1 = sum(test_conf_not6or1) / sum(test_data.good_trial);
    if pNot6or1 < .1, conf_resp_rate_good = false; end
    fprintf('\tpTest Responses Excluding 6 or 1 = %0.3f ',pNot6or1);
    if conf_resp_rate_good
        fprintf('(GOOD)\n');
    else
        fprintf('(BAD)\n');
        bad_conf = vertcat(bad_conf,id);
    end
        % Update participant log with values
    par_log.p_conf_not6or1(pari) = pNot6or1;
    
    %% Step 8 Determine if good or bad
    if ~all([study_resp_rate_good test_resp_rate_good mem_perf_good ...
            source_perf_good conf_resp_rate_good])
        participant_status = 'bad';
    else
        participant_status = 'good';
    end
         % Update participant log with values
      par_log.status{pari} = participant_status;
      
  
    % add participant status to data
    test_data.status  = repmat(participant_status, height(test_data), 1);
    
      
    % Create file names and write data table to file in analysis folder
    make_dirs({directories.par_analysis})
    combo_beh_file = fullfile( directories.par_analysis, sprintf('sub-%s_data_coded.tsv', id) );
    writetable(test_data, combo_beh_file, 'FileType','text','Delimiter','\t');
    
    
end
%% step 9: Save the combined participant log to data files folder for part3_analyze.m script
par_tsv_file = fullfile(directories.data_files,'participants.tsv');
writetable(par_log,par_tsv_file,'FileType','text','Delimiter','\t');