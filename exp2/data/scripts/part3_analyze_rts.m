%% Data Analysis

% ROC analysis of Experiment 2 data, see https://pubmed.ncbi.nlm.nih.gov/27573007/ for information on the ROC toolbox used for analysis.
% Memory, study RTs, and ROC data is collected here for analysis.


% Step 1: Gather Participant ID and make directories
% Step 2: Prepare Data for ROC Analysis
% Step 3: Fit with roc_solver
% Step 4: Compute and organize  memory data
% Step 5: Median RTs by cue condition and subsequent memory and store confidence data
% Step 6: Collect data for aggregate ROC data
% Step 7: Make each cell array a memory and study RT's data tables (in wide and long formats) and save data
% Step 8: Fit aggreated data withroc_solver and save data
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
directories.analyses   = fullfile(directories.top, 'analyses');
directories.data_files = fullfile(directories.analyses, 'data_files');

%% Get participant list to analyze
% Read all in source data

% Read in participants.tsv file from data_files
par_log_file = fullfile(directories.data_files, 'participants.tsv');
par_log_opts = detectImportOptions(par_log_file, 'FileType', 'text' );
par_log      = readtable( par_log_file, par_log_opts );

%Get participants who have good data (passed quality control behavioral measures)
participant_list = par_log.id(strcmpi(par_log.status,'good'));
participant_list = par_log.id;

% create tables (confidence, hits/fa, memory acc, studyrt) for data
conf_data   = cell2table( cell(0,5), ...
    'VariableNames',{'id' 'cue_condition' 'conf_bin' 'proportion' 'freq'} );

hit_fa_data = cell2table(  cell(0,6),...
'VariableNames', {'participant' 'status' 'study_cb' 'list' 'study_condition' 'proportion'});

memory_acc_data = cell2table(  cell(0,13),...
    'VariableNames', {'participant' 'status' 'study_cb' 'list'  'study_condition' 'auc' 'corrected_recognition' 'Ro' 'F'  'corrected_source' 'sourcePr' 'source_hit' 'source_dk'});

study_rt_data   = cell2table(  cell(0,7),...
    'VariableNames',{'participant' 'status' 'study_cb' 'list'  'study_condition' 'subsequent_memory' 'median_rt'});

study_acc_data = cell2table( cell(0,6),...
'VariableNames', {'participant' 'status' 'study_cb' 'list' 'study_condition' 'proportion'});

 meta_targf = [0 0 0 0 0 0 ;0 0 0 0 0 0 ];
 meta_luref = [0 0 0 0 0 0 ;0 0 0 0 0 0 ];
%% Loop through participants
for pari = 1:length(participant_list)
    
    %% Step 1: Gather Participant ID and make directories
    % Convert participant to char type
    participant = sprintf('%03.0f',participant_list(pari));
    % Print info to screen
    fprintf('\n\nProcessing data for %s:\n\n',participant);
    
    % Make directory structure in data
    directories.par_analysis = fullfile(directories.data_files,  sprintf('sub-%s',participant));
    
    % Load behavioral data
    data_file = fullfile(directories.par_analysis,sprintf('sub-%s_data_coded.tsv',participant));
    opts       = detectImportOptions(data_file, 'FileType', 'text');
    test_data  = readtable(data_file, opts);
    
    % Assign counterbanacing information
    study_cb = cell2mat(test_data.study_cb(1));
    list = test_data.list(1);
    
    % Assign good/bad participant status
    status = test_data.status{1};
    
    %% Step 2: Prepare Data for ROC Analysis
    % Get trial vectors
    good_rt_trial = test_data.item_rt > .60;
    count_good_rts = numel(good_rt_trial(good_rt_trial>0))
    good_trial = test_data.good_trial;
    old_trial  = ismember(test_data.old_new,'old');
    informed   = ismember(test_data.cue_condition,'informed');
    uninformed = ismember(test_data.cue_condition,'uninformed');
    % Get old trials
    targf = [];
    luref = [];
    c = 1; % counter
     for i = 6:-1:1
            targf(1,c) = sum( test_data.item_resp(old_trial & informed & good_trial & good_rt_trial) == i );
            targf(2,c) = sum( test_data.item_resp(old_trial & ~informed & good_trial & good_rt_trial) == i );
            luref(1,c) = sum( test_data.item_resp(~old_trial & good_trial & good_rt_trial) == i );
            c = c+1;
     end
    luref = repmat(luref,size(targf,1),1); % Replicate this in a second row for ROC Toolbox use
    
    %% Step 3: Fit with roc_solver
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
        'subID',participant, ...
        'modelID',modelID, ...
        'condLabels',condLabels, ...
        'ignoreConds',ignoreConds, ...
        'options', options, ...
        'saveFig', directories.par_analysis, ...
        'figTimeout', 1);
    
    % Save roc_data to .mat file
%     save(fullfile(directories.par_analysis,'roc_data.mat'),'roc_data');
    %% Step 4 Compute and organize  memory data
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
    
    % Get needed trial vectors for source pR
    old_resp     = ismember(test_data.item_resp,4:6); %old responses (4-guess old,5- maybe old,6 sure old) 
    
    
    % Code source accuracy as shoebox response (sm_resp==4) to a shoebox
    % item OR a manmande response (sm_resp==5) to a manmade item.
    source_cor = (test_data.sm_resp==4 & ismember(test_data.study_judgment,'shoebox')) | ...
        (test_data.sm_resp==5 & ismember(test_data.study_judgment,'manmade')) ;
    source_dk  = test_data.sm_resp==6;
    source_inc = (test_data.sm_resp==4 & ismember(test_data.study_judgment,'manmade')) |...
        (test_data.sm_resp==5 & ismember(test_data.study_judgment,'shoebox'));
    
    % Compute source pR (assumping an item hit)
    p_shit_informed = mean(source_cor(old_trial & old_resp & informed & good_trial & good_rt_trial));
    p_sdk_informed  = mean(source_dk(old_trial & old_resp & informed & good_trial & good_rt_trial));
    informed_sourcePR = (p_shit_informed - .5*(1-p_sdk_informed)) / (1 - .5*(1-p_sdk_informed));
    p_shit_uninformed = mean(source_cor(old_trial & old_resp & ~informed & good_trial & good_rt_trial));
    p_sdk_uninformed  = mean(source_dk(old_trial & old_resp & ~informed & good_trial & good_rt_trial));
    uninformed_sourcePR = (p_shit_uninformed - .5*(1-p_sdk_uninformed)) / (1 - .5*(1-p_sdk_uninformed));

 % Compute secondary measure of source memory performance (reviewer
    % suggestion)
    % Corrected source memory (hits-false alarms) as a function of
    % cue condition
    % hits = "manmade"|manmade + "shoebox"|shoebox
    %False alarm = "shoebox"|manmade + "manmade"|shoebox
    
    %False alarms 
    source_fa_informed      = mean(source_inc(old_trial & old_resp & informed & good_trial & good_rt_trial));
    source_fa_uninformed    = mean(source_inc(old_trial & old_resp & uninformed & good_trial & good_rt_trial));
    %hits - FA
    cr_s_informed           = (p_shit_informed - source_fa_informed);
    cr_s_uninformed         = (p_shit_uninformed - source_fa_uninformed);
    
    
   
%% Check study judgment accuracy (reviewer comments)
    study_trial = ismember(test_data.old_new,'old');
    good_study_trial = test_data.study_good_trial;
    % 1 = yes, 2 = no
    study_hit = (ismember(test_data.study_resp,1) & ismember(test_data.study_judgment_correct_resp,1))|...
    (ismember(test_data.study_resp,2) & ismember(test_data.study_judgment_correct_resp,2));

    informed_study = mean(study_hit(old_trial & good_study_trial & informed & good_rt_trial));
    uninformed_study = mean(study_hit(old_trial & good_study_trial & uninformed & good_rt_trial));
    
    study_acc_data =  vertcat(study_acc_data, ...
        {participant status study_cb list 'informed' informed_study}, ...
        {participant status study_cb list 'uninformed' uninformed_study})
    
    % Store hit and FA data
    hit_fa_data = vertcat(hit_fa_data, ...
        {participant status study_cb list 'informed' informed_hits}, ...
        {participant status study_cb list 'uninformed' uninformed_hits}, ...
        {participant status study_cb list 'new' false_alarms });
   
     memory_acc_data = vertcat(memory_acc_data, ...
        {participant status study_cb list 'informed' informed_auc informed_cor_recog informed_Ro informed_F   cr_s_informed informed_sourcePR p_shit_informed p_sdk_informed}, ...
        {participant status study_cb list 'uninformed' uninformed_auc uninformed_cor_recog uninformed_Ro uninformed_F   cr_s_uninformed uninformed_sourcePR p_shit_uninformed p_sdk_uninformed} );
 
    %% Step 5: Median RTs by cue condition and subsequent memory and store confidence data
    % Gather trials of use
    study_rts = test_data.study_rt; % Get out RTs now
    source_miss = source_dk | source_inc; % Create a source_miss bin
    
    % Get a median RT and store in study_rt_data
    study_rt_data = vertcat(study_rt_data, ...
        { participant status study_cb list 'informed'  'SC'   median(study_rts(informed & old_trial & old_resp & source_cor & good_trial & good_rt_trial)) }, ...
        { participant status study_cb list 'informed'  'SIDK' median(study_rts(informed & old_trial & old_resp & source_miss & good_trial & good_rt_trial)) }, ...
        { participant status study_cb list 'informed'  'Miss' median(study_rts(informed & old_trial & ~old_resp & good_trial & good_rt_trial)) }, ...
        { participant status study_cb list 'uninformed'  'SC'   median(study_rts(~informed & old_trial & old_resp & source_cor & good_trial & good_rt_trial)) }, ...
        { participant status study_cb list 'uninformed'  'SIDK' median(study_rts(~informed & old_trial & old_resp & source_miss & good_trial & good_rt_trial)) }, ...
        { participant status study_cb list 'uninformed'  'Miss' median(study_rts(~informed & old_trial & ~old_resp & good_trial & good_rt_trial)) } );
        
     % Store confidence data
    conf_data = vertcat(conf_data, ...
        {participant 'informed' 6 roc_data.observed_data.target.proportions(1,1) roc_data.observed_data.target.frequency(1,1) }, ...
        {participant 'informed' 5 roc_data.observed_data.target.proportions(1,2) roc_data.observed_data.target.frequency(1,2)}, ...
        {participant 'informed' 4 roc_data.observed_data.target.proportions(1,3) roc_data.observed_data.target.frequency(1,3)}, ...
        {participant 'informed' 3 roc_data.observed_data.target.proportions(1,4) roc_data.observed_data.target.frequency(1,4)}, ...
        {participant 'informed' 2 roc_data.observed_data.target.proportions(1,5) roc_data.observed_data.target.frequency(1,5)}, ...
        {participant 'informed' 1 roc_data.observed_data.target.proportions(1,6) roc_data.observed_data.target.frequency(1,6)}, ...
        {participant 'uninformed' 6 roc_data.observed_data.target.proportions(2,1) roc_data.observed_data.target.frequency(2,1)}, ...
        {participant 'uninformed' 5 roc_data.observed_data.target.proportions(2,2) roc_data.observed_data.target.frequency(2,2)}, ...
        {participant 'uninformed' 4 roc_data.observed_data.target.proportions(2,3) roc_data.observed_data.target.frequency(2,3)}, ...
        {participant 'uninformed' 3 roc_data.observed_data.target.proportions(2,4) roc_data.observed_data.target.frequency(2,4)}, ...
        {participant 'uninformed' 2 roc_data.observed_data.target.proportions(2,5) roc_data.observed_data.target.frequency(2,5)}, ...
        {participant 'uninformed' 1 roc_data.observed_data.target.proportions(2,6) roc_data.observed_data.target.frequency(2,6)}, ...
        {participant 'new' 6 roc_data.observed_data.lure.proportions(1,1) roc_data.observed_data.lure.frequency(1,1)}, ...
        {participant 'new' 5 roc_data.observed_data.lure.proportions(1,2) roc_data.observed_data.lure.frequency(1,2)}, ...
        {participant 'new' 4 roc_data.observed_data.lure.proportions(1,3) roc_data.observed_data.lure.frequency(1,3)}, ...
        {participant 'new' 3 roc_data.observed_data.lure.proportions(1,4) roc_data.observed_data.lure.frequency(1,4)}, ...
        {participant 'new' 2 roc_data.observed_data.lure.proportions(1,5) roc_data.observed_data.lure.frequency(1,5)}, ...
        {participant 'new' 1 roc_data.observed_data.lure.proportions(1,6) roc_data.observed_data.lure.frequency(1,6)} ...
        );
    
   %% Step 6 collect data for aggregate ROC data
    temp_targf = [];
    temp_luref = [];
        c = 1; % counter
     for i = 6:-1:1
            temp_targf(1,c) = sum( test_data.item_resp(old_trial & informed & good_trial & good_rt_trial) == i ) ;
            meta_targf(1,c) =  meta_targf(1,c) + temp_targf(1,c);
            
            temp_targf(2,c) = sum( test_data.item_resp(old_trial & ~informed & good_trial & good_rt_trial) == i ) ;
            meta_targf(2,c) = temp_targf(2,c)+ meta_targf(2,c);
            temp_luref(1,c) = sum( test_data.item_resp(~old_trial & good_trial & good_rt_trial) == i ) ;
            meta_luref(1,c) = temp_luref(1,c) + meta_luref(1,c);
            temp_luref(2,c) = temp_luref(1,c);
            meta_luref(2,c) = temp_luref(2,c) + meta_luref(2,c);
            c = c+1;
     end

    
end

%% Step 7: Make each cell array a data table (in wide and long formats) and save data
study_acc_data_wide = unstack(study_acc_data,{'proportion'},'study_condition');
% Hit and FA data
hit_fa_data_wide = unstack(hit_fa_data,'proportion','study_condition', ...
    'NewDataVariableNames',{'informed_hits','false_alarms','uninformed_hits'});
hit_fa_data_wide = movevars(hit_fa_data_wide,{'uninformed_hits'},'After','informed_hits');

% Accuracy Measure Data
memory_acc_data_wide = unstack(memory_acc_data,{'auc','corrected_recognition','Ro','F','corrected_source','sourcePr' 'source_hit' 'source_dk'},'study_condition');

% Study RT Data
study_rt_data_wide = unstack(study_rt_data,'median_rt','study_condition');
study_rt_data_wide = unstack(study_rt_data_wide,{'informed' 'uninformed'},'subsequent_memory');
study_rt_data_wide.Properties.VariableNames(5:end) = ...
    cellfun(@(x) strcat(x,'_median_studyrt'), study_rt_data_wide.Properties.VariableNames(5:end), 'UniformOutput', false);


% Join the three wide data tables
all_data_wide = join(hit_fa_data_wide,memory_acc_data_wide);
% all_data_wide = join(all_data_wide,study_rt_data_wide);


% Write ALL data tables to file
writetable(study_acc_data_wide,fullfile(directories.analyses,'rt_study_acc_data_wide.csv'));

writetable(hit_fa_data,fullfile(directories.analyses,'rt_hit_fa_data_long.csv'));
writetable(memory_acc_data,fullfile(directories.analyses,'rt_memory_acc_data_long.csv'));
writetable(study_rt_data,fullfile(directories.analyses,'rt_study_rt_data_long.csv'));
% writetable(all_data_wide,fullfile(directories.analyses,'all_data_wide.csv'));
writetable(study_rt_data_wide,fullfile(directories.analyses,'rt_studyrt_wide.csv'));
writetable(conf_data,fullfile(directories.analyses,'rt_conf_data_long.csv'),'FileType','text','Delimiter','\t');


writetable(all_data_wide,fullfile(directories.analyses,'RT_trim_wide.csv'));
%% Step 8 get ROC values aggregated across participants and save data
% Fit with roc_solver
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
        'subID',participant, ...
        'modelID',modelID, ...
        'condLabels',condLabels, ...
        'ignoreConds',ignoreConds, ...
        'options', options, ...
        'saveFig', directories.par_analysis, ...
        'figTimeout', 1);
    
% Store aggregated across participants predicted values
%     save(fullfile(directories.par_analysis,'meta_roc_data.mat'),'roc_data');
meta_data = cell2table(  cell(0,4),...
    'VariableNames', {'meta' 'informed' 'uninformed' 'Fa_pred'});

hit_pred = array2table(roc_data.dpsd_model.predicted_rocs.roc.target',...
    'VariableNames',{'informed_pred' 'uninformed_pred'})

fa_pred = array2table(roc_data.dpsd_model.predicted_rocs.roc.lure(1,:)',...
    'VariableNames',{'lure_pred'})
meta_data = [hit_pred fa_pred]

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
    {1 'uninformed' roc_data.observed_data.target.cumulative(2,6) roc_data.observed_data.lure.cumulative(2,6) } )
     

% % save aggregate ROC values 
 writetable(meta_data,fullfile(directories.analyses,'rt_meta_person.csv'),'FileType','text','Delimiter',',');
 writetable(meta_cumulative_data,fullfile(directories.analyses,'rt_meta_average.csv'),'FileType','text','Delimiter',',');

