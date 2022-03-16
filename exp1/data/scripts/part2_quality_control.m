%% Quality Control Data
% This script organizes data from sourcedata and performs some quality
% control checks to test for good data. This follows the pre-registered
% criteria found on OSF (https://osf.io/4amct). These include:
%
% 1) Overall memory performance < .10 (determined by Hit Rate - False Alarm
%    Rate metric collapsed across study condition)
% 2) More than 20% of study trials excluded for wrong hand response or
%    multiple responses (collapsed across conditions). 
% 3) Fewer than 10% of confidence responses in the 2-5 bins (collapsed
%    across item type and study condition). 
%
% Subjects excluded for one of the above reasons are labeled as bad in the
% participants.tsv file.

%% Clear workspace
clear all;
clc;

%% Define thresholds for bad data
% Define the thresholds for data exclusion based on performance metrics. 
thresholds.p_bad_study    = .2; % Exclude if more than 20% of trials excluded for study nr or incorrect hand
thresholds.p_conf_not6or1 = .1; % Exclude if the 2-5 confidence responses not used more than 10% of all trials
thresholds.item_pr        = .1; % Exclude if overall item pr (collapsed over condition) below .1

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

%% Get participant list
% Read in participants.tsv file from raw
par_log_file = fullfile(directories.raw, 'participants.tsv');
par_log_opts = detectImportOptions(par_log_file, 'FileType', 'text' );
par_log      = readtable( par_log_file, par_log_opts );

% Add new columns to par_log
par_log.status(:)         = {'good'};
par_log.p_bad_study(:)    = 0;
par_log.p_conf_not6or1(:) = 0;
par_log.item_pr(:)        = 0;

%% Loop through participants
for pari = 1:size(par_log,1)
    
    %% Step 1: Gather Participant id
    % Get participant id
    id = sprintf('%03.0f',par_log.id(pari));
    
    % Print info to screen
    fprintf('\n\nQuality control of data for sub-%s:\n',id);
    
    % Make directory structure in data
    directories.par_data     = fullfile(directories.raw, sprintf('sub-%s', id) );
    
    % Initialize participant flags as good to start with. 
    study_resp_rate_good  = true; % proportion of excluded study trials < .2
    mem_perf_good         = true; % item pR >= .1
    conf_resp_rate_good   = true; % proportion use of confidenc
    
    %% Step 2: Load the test data (which can be used for all analyses
    % Load data
    test_file = fullfile( directories.par_data, sprintf('sub-%s_task-test.tsv', id) ); 
    test_opts = detectImportOptions( test_file, 'FileType', 'text' );
    test_data = readtable( test_file, test_opts );
    
    %% Step 3: Compute proportion of bad study trials     
    % Compute the proportion of excluded study trials
    p_bad_study = mean(~test_data.good_trial(ismember(test_data.old_new,'old')));
    
    % Update study_resp_rate_good flag if needed
    if p_bad_study > thresholds.p_bad_study
        study_resp_rate_good = false; 
    end
    
    % Print information to the screen
    fprintf('\tpBad Study Trials = %0.3f ', p_bad_study);
    if study_resp_rate_good 
        fprintf('(GOOD)\n'); 
    else
        fprintf('(BAD)\n'); 
    end
    
    % Update participant log with values
    par_log.p_bad_study(pari) = p_bad_study;
    
    %% Step 4: Compute Proportion of Confidence Bin 2-5 Use >=.1
    % Proportion of confidence bins 2-5 used
    test_conf_not6or1 = ismember(test_data.test_resp, [2 3 4 5]) & test_data.good_trial;
    p_not_6or1 = sum(test_conf_not6or1) / sum(test_data.good_trial);
    
    % Update conf_resp_rate_good flag if needed
    if p_not_6or1 < thresholds.p_conf_not6or1
        conf_resp_rate_good = false; 
    end
    
    % Print information to the screen
    fprintf('\tpTest Responses Excluding 6 or 1 = %0.3f ',p_not_6or1);
    if conf_resp_rate_good
        fprintf('(GOOD)\n');
    else
        fprintf('(BAD)\n');
    end
    
    % Update participant log with values
    par_log.p_conf_not6or1(pari) = p_not_6or1;
    
    %% Step 5: Compute item pR collapsed over cue condition
    % Compute item pR (pHit-pFA)
    old_trials = ismember(test_data.old_new,'old') & test_data.good_trial;
    new_trials = ismember(test_data.old_new,'new') & test_data.good_trial;
    old_resp   = ismember(test_data.test_resp,4:6) & test_data.good_trial;
    item_hits  = old_trials & old_resp;
    item_fas   = new_trials & old_resp;
    item_pHit = sum(item_hits)/sum(old_trials);
    item_pFA  = sum(item_fas)/sum(new_trials);
    item_pr   = item_pHit - item_pFA;
    
    % update mem_perf_good flag if needed
    if item_pr < thresholds.item_pr
        mem_perf_good = false; 
    end
    
    % Print information to the screen
    fprintf('\tItem pR = %0.3f ', item_pr)
    if mem_perf_good
        fprintf('(GOOD)\n');
    else
        fprintf('(BAD)\n');
    end
    
    % update participant log with values
    par_log.item_pr(pari) = item_pr;
    
    %% Step 6: Determine if subject is good or bad
    % Update participant status in par_log (default is good)
    if ~all([study_resp_rate_good mem_perf_good conf_resp_rate_good])
        par_log.status{pari} = 'bad';
    end
    
    %% Step 7: Copy subject data to analysis folder if good
    if strcmpi(par_log.status(pari),'good')
        copyfile( directories.par_data, fullfile(directories.data_files,sprintf('sub-%s',id)) );
    end
    
end

%% Save the participant log to BIDS
par_tsv_file = fullfile(directories.raw,'participants.tsv');
writetable(par_log,par_tsv_file,'FileType','text','Delimiter','\t');

%% Save participant log to analyses (remove 'bad' status subjects
par_tsv_file = fullfile(directories.data_files,'participants.tsv');
par_log(strcmpi(par_log.status,'bad'),:) = [];
writetable(par_log, par_tsv_file, 'FileType','text','Delimiter','\t');

        