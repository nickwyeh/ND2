%% Data Analysis

%ROCs for participant 
%Computes memory (hits/FA, item_pr, F, Ro) and organizes studyRT's for informed/uninformed conditions.
%Outputs memory and RT data.
%Outputs ROC proportions


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
directories.analyses   = fullfile(directories.top, 'analyses');
directories.data_files = fullfile(directories.analyses, 'data_files');

%% Get participant list to analyze
% Read in participants.tsv file from analyses/data_files
par_log_file = fullfile(directories.data_files, 'participants.tsv');
par_log_opts = detectImportOptions(par_log_file, 'FileType', 'text' );
par_log      = readtable( par_log_file, par_log_opts );

%% Initialize output data (cell array)
% Create an empty cell arrays to store data. Data will be in long format
conf_data   = cell2table( cell(0,4), ...
    'VariableNames',{'id' 'cue_condition' 'conf_bin' 'proportion'} );
hit_fa_data   = cell2table( cell(0,3), ...
    'VariableNames',{'id' 'cue_condition' 'proportion'} );
mem_acc_data  = cell2table( cell(0,6), ...
    'VariableNames',{'id' 'cue_condition' 'auc' 'item_pr' 'Ro' 'F'} );
study_rt_data = cell2table( cell(0,4), ...
    'VariableNames',{'id' 'cue_condition' 'subsequent_memory' 'median_rt'} );

study_acc_data = cell2table( cell(0,4),...
'VariableNames', {'id'  'cue_condition' 'correct_hand' 'proportion'});

pivot_table = array2table(zeros(0,24), 'VariableNames',{'id','stim_set','psychopyVersion','word','manmade','shoebox',...
    'nletters','freq','nsyllables','concreteness','old_new','study_judgment','cue_condition','test_resp','test_rt',...
    'study_judgment_correct_resp','stayswitch','stayswitch_run','study_resp','study_rt','correct_hand','study_nr',...
    'good_trial', 'trial'});
% set up variables for aggregate ROC plots
 meta_targf = [0 0 0 0 0 0 ;0 0 0 0 0 0 ];
 meta_luref = [0 0 0 0 0 0 ;0 0 0 0 0 0 ];

%% Loop through participants
for pari = 1:size(par_log,1)
    
    %% Step 1: Gather Participant ID and make directories
    % Get participant ID
    id = sprintf('%03.0f',par_log.id(pari));
    
    % Print info to screen
    fprintf('\n\nEstimating data for %s:\n',id);
    
    % Make directory structure in data
    directories.par_analysis = fullfile(directories.data_files, sprintf('sub-%s',id));
    
    % Load behavioral data
    data_file  = fullfile(directories.par_analysis,sprintf('sub-%s_task-test.tsv',id));
    opts       = detectImportOptions(data_file, 'FileType', 'text');
    test_data  = readtable(data_file, opts);
    
    %% Step 2: Prepare Data for ROC Analysis
    % Get trial vectors
    good_trial = test_data.good_trial;
    old_trial  = ismember(test_data.old_new,'old');
    informed   = ismember(test_data.cue_condition,'informed');
    uninformed = ismember(test_data.cue_condition,'uninformed');
    % Get the targf and luref vectors for the ROC Toolbox
    targf = [];
    luref = [];
    c = 1; % counter
    for i = 6:-1:1
        targf(1,c) = sum( test_data.test_resp(old_trial & informed & good_trial) == i );
        targf(2,c) = sum( test_data.test_resp(old_trial & ~informed & good_trial) == i );
        luref(1,c) = sum( test_data.test_resp(~old_trial & good_trial) == i );
        c = c+1;
    end
    luref = repmat(luref,size(targf,1),1); % Replicate this in a second row for ROC Toolbox use
    
    %% Step 3: Fit with roc_solver and extract relevant memory data
    % Specify model design options
    model = 'dpsd';
    [nConds, nBins] = size(targf);
    parNames = {'Ro' 'F'};
    ignoreConds = 2; % Ignore fit values for 2nd row in luref (2 old, 1 new design)
    fitStat = '-LL';
    
    % Specify other options for bookkeeping
    condLabels = {'Informed' 'Uninformed'};
    modelID = 'dpsd';
    
    % Specify optimization options
    options = optimset('fmincon');
    options.Display = 'notify';
    options.MaxFunEvals = 100000;
    options.TolX = 1e-10; % Set options of tolerance for parameter changes
    
    % Initialize parameter matrix and bounds
    [x0,lb,ub] = gen_pars(model,nBins,nConds,parNames);
    lb(:,3) = 0; % Change F lower bound to 0
    
    % Specify     
    roc_data = roc_solver(targf,luref,model,fitStat,x0,lb,ub, ...
        'subID',id, ...
        'modelID',modelID, ...
        'condLabels',condLabels, ...
        'ignoreConds',ignoreConds, ...
        'options', options, ...
        'saveFig', directories.par_analysis, ...
        'figTimeout', 5);
    
    % Save roc_data to .mat file
    save(fullfile(directories.par_analysis,sprintf('sub-%s_desc-rocdata.mat',id)));

    % Get values out for short-hand variable naming
    informed_hits        = roc_data.observed_data.accuracy_measures.HR(1);
    uninformed_hits      = roc_data.observed_data.accuracy_measures.HR(2);
    informed_auc         = roc_data.observed_data.accuracy_measures.auc(1);
    uninformed_auc       = roc_data.observed_data.accuracy_measures.auc(2);
    false_alarms         = roc_data.observed_data.accuracy_measures.FAR(1); % 2 is duplicate given design
    informed_cor_recog   = informed_hits - false_alarms;
    uninformed_cor_recog = uninformed_hits - false_alarms;
    informed_Ro          = roc_data.dpsd_model.parameters.Ro(1);
    uninformed_Ro        = roc_data.dpsd_model.parameters.Ro(2);
    informed_F           = roc_data.dpsd_model.parameters.F(1);
    uninformed_F         = roc_data.dpsd_model.parameters.F(2);
    
     %% Check study judgment accuracy (reviewer comments)
    study_trial = ismember(test_data.old_new,'old');
    % 1 = yes, 2 = no
    study_hit = (ismember(test_data.study_resp,1) & ismember(test_data.study_judgment_correct_resp,1))|...
    (ismember(test_data.study_resp,2) & ismember(test_data.study_judgment_correct_resp,2));

    study_hand_hit = (ismember(test_data.old_new,'old') & ismember(test_data.correct_hand,1));

    informed_study = mean(study_hit(old_trial & good_trial & informed));
    uninformed_study = mean(study_hit(old_trial & good_trial & uninformed));
    
    informed_study_hand = mean(study_hand_hit(old_trial  & informed));
    uninformed_study_hand = mean(study_hand_hit(old_trial  & uninformed));
    
    study_acc_data =  vertcat(study_acc_data, ...
        {id  'informed' informed_study_hand informed_study}, ...
        {id  'uninformed' uninformed_study_hand uninformed_study});
    %% Step 4: Store memory data in data frames
    % Store confidence data
    conf_data = vertcat(conf_data, ...
        {id 'informed' 6 roc_data.observed_data.target.proportions(1,1)}, ...
        {id 'informed' 5 roc_data.observed_data.target.proportions(1,2)}, ...
        {id 'informed' 4 roc_data.observed_data.target.proportions(1,3)}, ...
        {id 'informed' 3 roc_data.observed_data.target.proportions(1,4)}, ...
        {id 'informed' 2 roc_data.observed_data.target.proportions(1,5)}, ...
        {id 'informed' 1 roc_data.observed_data.target.proportions(1,6)}, ...
        {id 'uninformed' 6 roc_data.observed_data.target.proportions(2,1)}, ...
        {id 'uninformed' 5 roc_data.observed_data.target.proportions(2,2)}, ...
        {id 'uninformed' 4 roc_data.observed_data.target.proportions(2,3)}, ...
        {id 'uninformed' 3 roc_data.observed_data.target.proportions(2,4)}, ...
        {id 'uninformed' 2 roc_data.observed_data.target.proportions(2,5)}, ...
        {id 'uninformed' 1 roc_data.observed_data.target.proportions(2,6)}, ...
        {id 'new' 6 roc_data.observed_data.lure.proportions(1,1)}, ...
        {id 'new' 5 roc_data.observed_data.lure.proportions(1,2)}, ...
        {id 'new' 4 roc_data.observed_data.lure.proportions(1,3)}, ...
        {id 'new' 3 roc_data.observed_data.lure.proportions(1,4)}, ...
        {id 'new' 2 roc_data.observed_data.lure.proportions(1,5)}, ...
        {id 'new' 1 roc_data.observed_data.lure.proportions(1,6)} ...
        );
    
    % Store hit and FA data
    hit_fa_data = vertcat(hit_fa_data, ...
        {id 'informed' informed_hits}, ...
        {id 'uninformed' uninformed_hits}, ...
        {id 'new' false_alarms} );
    
    % Store HR-FAR, Ro, and F data
    mem_acc_data = vertcat(mem_acc_data, ...
        {id 'informed' informed_auc informed_cor_recog informed_Ro informed_F}, ...
        {id 'uninformed' uninformed_auc uninformed_cor_recog uninformed_Ro uninformed_F } );
    % unstack to wide format
    memory_acc_data_wide = unstack(mem_acc_data,{'auc','item_pr','Ro','F'},'cue_condition');

       % create pivot table
    % Add trial numbers
    for ii = 1:size(test_data,1)
        test_data.trial(ii) = ii;
    end
    pivot_table = vertcat(pivot_table,test_data);
    %% Step 5: Analysis of median RTs by cue condition and subsequent memory
    % Gather trials of use
    old_resp  = ismember(test_data.test_resp,4:6); % Get vector of old item responses
    study_rts = test_data.study_rt; % Get out RTs now
    
    % Get a median RT and store in study_rt_data
    study_rt_data = vertcat(study_rt_data, ...
        {id 'informed' 'hit' median(study_rts(informed & old_trial & old_resp & good_trial))}, ...
        {id 'informed' 'miss' median(study_rts(informed & old_trial & ~old_resp & good_trial))},...
        {id 'uninformed' 'hit' median(study_rts(~informed & old_trial & old_resp & good_trial))},...
        {id 'uninformed' 'miss' median(study_rts(~informed & old_trial & ~old_resp & good_trial))} );

    %% step 6: store aggregate hits and lures for ROC plots
    temp_targf = [];
    temp_luref = [];
    c = 1; % counter
    for i = 6:-1:1
        temp_targf(1,c) = sum( test_data.test_resp(old_trial & informed & good_trial) == i ) ;
        meta_targf(1,c) =  meta_targf(1,c) + temp_targf(1,c);
        
        temp_targf(2,c) = sum( test_data.test_resp(old_trial & ~informed & good_trial) == i ) ;
        meta_targf(2,c) = temp_targf(2,c)+ meta_targf(2,c);
        temp_luref(1,c) = sum( test_data.test_resp(~old_trial & good_trial) == i ) ;
        meta_luref(1,c) = temp_luref(1,c) + meta_luref(1,c);
        temp_luref(2,c) = temp_luref(1,c);
        meta_luref(2,c) = temp_luref(2,c) + meta_luref(2,c);
        c = c+1;
    end
end

study_acc_data_wide = unstack(study_acc_data,{'correct_hand' 'proportion'},'cue_condition');
% Study RT to wide
study_rt_data_wide = unstack(study_rt_data,'median_rt','cue_condition');
study_rt_data_wide = unstack(study_rt_data_wide,{'informed' 'uninformed'},'subsequent_memory');
study_rt_data_wide.Properties.VariableNames(5:end) = ...
    cellfun(@(x) strcat(x,'_median_studyrt'), study_rt_data_wide.Properties.VariableNames(5:end), 'UniformOutput', false);

% Join the three wide data tables
all_data_wide = join(memory_acc_data_wide,study_rt_data_wide);

%% Write ALL memory and reaction time data tables to file
writetable(study_acc_data_wide,fullfile(directories.analyses,'study_acc_data_wide.csv'));

writetable(conf_data,fullfile(directories.analyses,'conf_data_long.csv'),'FileType','text','Delimiter','\t');
writetable(hit_fa_data,fullfile(directories.analyses,'hit_fa_data_long.csv'),'FileType','text','Delimiter','\t');
writetable(mem_acc_data,fullfile(directories.analyses,'mem_acc_data_long.csv'),'FileType','text','Delimiter','\t');
writetable(study_rt_data,fullfile(directories.analyses,'study_rt_data_long.csv'),'FileType','text','Delimiter','\t');
writetable(all_data_wide,fullfile(directories.analyses,'all_data_wide.csv'));
writetable(study_rt_data_wide, fullfile(directories.analyses,'studyrt_wide.csv'));
writetable(pivot_table,fullfile(directories.analyses,'pivot_table.csv'));

%% Step 7 get ROC values aggregated across participants, Fit with roc_solver
    % Specify model design options
    model = 'dpsd';
    [nConds, nBins] = size(meta_targf);
    parNames = {'Ro' 'F'};
    ignoreConds = 2; % Ignore fit values for 2nd row in luref (2 old, 1 new design)
    fitStat = '-LL';
    
    % Specify other options for bookkeeping
    condLabels = {'Informed' 'Uninformed'};
    modelID = 'dpsd';
    
    % Specify optimization options
    options = optimset('fmincon');
    options.Display = 'notify';
    options.MaxFunEvals = 100000;
    options.TolX = 1e-10; % Set options of tolerance for parameter changes
    
    % Initialize parameter matrix and bounds
    [x0,lb,ub] = gen_pars(model,nBins,nConds,parNames);
    lb(:,3) = 0; % Change F lower bound to 0
    
    % Specify
    roc_data = roc_solver(meta_targf,meta_luref,model,fitStat,x0,lb,ub, ...
        'subID',id, ...
        'modelID',modelID, ...
        'condLabels',condLabels, ...
        'ignoreConds',ignoreConds, ...
        'options', options, ...
        'saveFig', directories.par_analysis, ...
        'figTimeout', 1);
    
% Store aggregated across participants predicted values
    save(fullfile(directories.par_analysis,'meta_roc_data.mat'),'roc_data');
meta_data = cell2table(  cell(0,4),...
    'VariableNames', {'meta' 'informed' 'uninformed' 'Fa_pred'});

hit_pred = array2table(roc_data.dpsd_model.predicted_rocs.roc.target',...
    'VariableNames',{'informed_pred' 'uninformed_pred'})

fa_pred = array2table(roc_data.dpsd_model.predicted_rocs.roc.lure(1,:)',...
    'VariableNames',{'lure_pred'});
meta_data = [hit_pred fa_pred];

% Store cumulative data
meta_cumulative_data = cell2table(  cell(0,4),...
    'VariableNames', {'Bin' 'Condition' 'hit_c' 'fa_c'});
meta_cumulative_data = vertcat(meta_cumulative_data, ...
    {6 'informed' roc_data.observed_data.target.cumulative(1,1) roc_data.observed_data.lure.cumulative(1,1) }, ...
    {5 'informed' roc_data.observed_data.target.cumulative(1,2) roc_data.observed_data.lure.cumulative(1,2) }, ...
    {4 'informed' roc_data.observed_data.target.cumulative(1,3) roc_data.observed_data.lure.cumulative(1,3) }, ...
    {3 'informed' roc_data.observed_data.target.cumulative(1,4) roc_data.observed_data.lure.cumulative(1,4) }, ...
    {2 'informed' roc_data.observed_data.target.cumulative(1,5) roc_data.observed_data.lure.cumulative(1,5) }, ...
    {1 'informed' roc_data.observed_data.target.cumulative(1,6) roc_data.observed_data.lure.cumulative(1,6) }, ...
    {6 'uninformed' roc_data.observed_data.target.cumulative(2,1) roc_data.observed_data.lure.cumulative(2,1) }, ...
    {5 'uninformed' roc_data.observed_data.target.cumulative(2,2) roc_data.observed_data.lure.cumulative(2,2) }, ...
    {4 'uninformed' roc_data.observed_data.target.cumulative(2,3) roc_data.observed_data.lure.cumulative(2,3) }, ...
    {3 'uninformed' roc_data.observed_data.target.cumulative(2,4) roc_data.observed_data.lure.cumulative(2,4) }, ...
    {2 'uninformed' roc_data.observed_data.target.cumulative(2,5) roc_data.observed_data.lure.cumulative(2,5) }, ...
    {1 'uninformed' roc_data.observed_data.target.cumulative(2,6) roc_data.observed_data.lure.cumulative(2,6) } );
     
% save data for ROC graphs
writetable(meta_data,fullfile(directories.analyses,'meta_person.csv'),'FileType','text','Delimiter',',');
writetable(meta_cumulative_data,fullfile(directories.analyses,'meta_average.csv'),'FileType','text','Delimiter',',');