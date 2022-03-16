%% Data Analysis
% This script will take input from the data analyis folder and output excel
% files for memory, study RT's, and ROCs for Experiment 3. The ROC toolbox will be requied
% to compute recollection and familiarity estimates. 
% For additional information on ROC tool box see, https://pubmed.ncbi.nlm.nih.gov/27573007/

% Step 1: Gather Participant ID and make directories
% Step 2: Prepare Data for ROC Analysis
% Step 3: Fit with roc_solver
% Step 4: Organize and save memory data
% Step 5: Analysis of median RTs by cue condition and subsequent memory
% Step 6 collect aggregate data for ROC
% Step 7 Make each cell array a data table (in wide and long formats) and save data
% Step 8 get ROC values aggregated across participants
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
directories.analyses   = fullfile(directories.top, 'analyses');
directories.data_files = fullfile(directories.analyses, 'data_files');

%% Get participant list to analyze
% Read all in source data

% Read in participants.tsv file from data_files
par_log_file = fullfile(directories.data_files, 'participants.tsv');
par_log_opts = detectImportOptions(par_log_file, 'FileType', 'text' );
par_log      = readtable( par_log_file, par_log_opts );

%include all participants
participant_list = par_log.id;

%Get participants who have good data (passed quality control behavioral measures)
%participant_list = par_log.id(strcmpi(par_log.status,'good'));

% % Alternative method when you dont have participant log set up 
% participant_list = dir(fullfile(directories.raw,'sub-*'));
% participant_list = {participant_list.name};

% create tables (confidence, hits/fa, memory acc, studyrt) for data
conf_data   = cell2table( cell(0,5), ...
    'VariableNames',{'id' 'cue_condition' 'conf_bin' 'proportion' 'freq'} );

hit_fa_data = cell2table(  cell(0,6),...
'VariableNames', {'participant' 'status' 'study_cb' 'list' 'study_condition' 'proportion'});

memory_acc_data = cell2table(  cell(0,15),...
    'VariableNames', {'participant' 'status' 'study_cb' 'list'  'study_condition' 'auc' 'corrected_recognition' 'Ro' 'F' 'new_low_source' 'new_high_source' 'corrected_source' 'sourcePr' 'source_hit' 'source_dk'});

study_rt_data   = cell2table(  cell(0,7),...
    'VariableNames',{'participant' 'status' 'study_cb' 'list'  'study_condition' 'subsequent_memory' 'median_rt'});

study_acc_data = cell2table( cell(0,6),...
'VariableNames', {'participant' 'status' 'study_cb' 'list' 'study_condition' 'proportion'});


% pivot_table = array2table(zeros(0,27), 'VariableNames',{'id','list','test_cb','word','old_new',...
%     'study_judgment','cue_condition','item_resp','trial','item_rt','item_acc','old_new_resp','sm_resp',...
%     'sm_rt','sm_acc','test_good_trial','study_resp','study_rt','study_good_trial','study_iti',...
%     'manmade','shoebox','study_judgment_correct_resp','good_trial','status', 'stayswitch', 'stayswitch_run'});

pivot_table = array2table(zeros(0,27), 'VariableNames',{'id','study_cb','list','test_cb','word','old_new',...
'study_judgment','cue_condition','item_resp','item_rt','item_acc','old_new_resp','sm_resp',...
    'sm_rt','sm_acc','test_good_trial','study_resp','study_rt','study_good_trial',...
    'manmade','shoebox','study_judgment_correct_resp','stayswitch','stayswitch_run','good_trial','status','trial'})
% set up to collect aggregate ROC data of participants
 meta_targf = [0 0 0 0 0 0 ;0 0 0 0 0 0;0 0 0 0 0 0 ];
 meta_luref = [0 0 0 0 0 0 ;0 0 0 0 0 0;0 0 0 0 0 0 ];
 

%% Loop through participants
for pari = 1:length(participant_list)
    
    %% Step 1: Gather Participant ID and make directories
    % Convert participant to char type
    participant = sprintf('%03.0f',participant_list(pari));
%     participant = participant_list(pari);
    
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
    good_trial = test_data.good_trial;
    old_trial  = ismember(test_data.old_new,'old');
    informed   = ismember(test_data.cue_condition,'informed');
    uninformed = ismember(test_data.cue_condition,'uninformed');
    uncued     = ismember(test_data.cue_condition,'uncued');
    % Get old trials
    targf = [];
    luref = [];
    c = 1; % counter
     for i = 6:-1:1
            targf(1,c) = sum( test_data.item_resp(old_trial & informed & good_trial) == i );
            targf(2,c) = sum( test_data.item_resp(old_trial & uninformed & good_trial) == i );
            targf(3,c) = sum( test_data.item_resp(old_trial & uncued & good_trial) == i );
            luref(1,c) = sum( test_data.item_resp(~old_trial & good_trial) == i );
            c = c+1;
     end
    luref = repmat(luref,size(targf,1),1); % Replicate this in a second row for ROC Toolbox use
    
    %% Step 3: Fit with roc_solver
    % Specify model design options
    model = 'dpsd';
    [nConds, nBins] = size(targf);
    parNames = {'Ro' 'F'};
    ignoreConds = 2:3; % Ignore fit values for 2nd and 3rd row in luref (3 old, 1 new design)
    fitStat = '-LL';
    
    % Specify other options for bookkeeping
    condLabels = {'Informed' 'Uninformed' 'Uncued'};
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
    save(fullfile(directories.par_analysis,'roc_data.mat'),'roc_data');
   

    %% Step 4 Organize and save memory data
    %Get values out for short-hand variable naming
    informed_hits        = roc_data.observed_data.accuracy_measures.HR(1);
    uninformed_hits      = roc_data.observed_data.accuracy_measures.HR(2);
    uncued_hits          = roc_data.observed_data.accuracy_measures.HR(3);
    informed_auc         = roc_data.observed_data.accuracy_measures.auc(1);
    uninformed_auc       = roc_data.observed_data.accuracy_measures.auc(2);
    uncued_auc           = roc_data.observed_data.accuracy_measures.auc(3);
    false_alarms         = roc_data.observed_data.accuracy_measures.FAR(1); % 2:3 is duplicate given design
    informed_cor_recog   = informed_hits - false_alarms;
    uninformed_cor_recog = uninformed_hits - false_alarms;
    uncued_cor_recog     = uncued_hits - false_alarms;
    informed_Ro          = roc_data.dpsd_model.parameters.Ro(1);
    uninformed_Ro        = roc_data.dpsd_model.parameters.Ro(2);
    uncued_Ro            = roc_data.dpsd_model.parameters.Ro(3);
    informed_F           = roc_data.dpsd_model.parameters.F(1);
    uninformed_F         = roc_data.dpsd_model.parameters.F(2);
    uncued_F             = roc_data.dpsd_model.parameters.F(3);

    % Get needed trial vectors for source pR
    old_resp     = ismember(test_data.item_resp,4:6); %old responses (4-guess old,5- maybe old,6 sure old) 
        
    % Code source accuracy as shoebox response (sm_resp==4) to a shoebox
    % item OR a manmande response (sm_resp==5) to a manmade item.
    source_cor = (test_data.sm_resp==4 & ismember(test_data.study_judgment,'shoebox')) | ...
        (test_data.sm_resp==5 & ismember(test_data.study_judgment,'manmade')) ;
    source_dk  = test_data.sm_resp==6;
    source_inc = (test_data.sm_resp==4 & ismember(test_data.study_judgment,'manmade')) |...
        (test_data.sm_resp==5 & ismember(test_data.study_judgment,'shoebox'));
    
    % Compute source pR for informed, uninformed, uncued (assuming an item hit). 
    % Informed
    p_shit_informed     = mean(source_cor(old_trial & old_resp & informed & good_trial));
    p_sdk_informed      = mean(source_dk(old_trial & old_resp & informed & good_trial));
    informed_sourcePR   = (p_shit_informed - .5*(1-p_sdk_informed)) / (1 - .5*(1-p_sdk_informed));
    % Uninformed
    p_shit_uninformed   = mean(source_cor(old_trial & old_resp & uninformed & good_trial));
    p_sdk_uninformed    = mean(source_dk(old_trial & old_resp & uninformed & good_trial));
    uninformed_sourcePR = (p_shit_uninformed - .5*(1-p_sdk_uninformed)) / (1 - .5*(1-p_sdk_uninformed));
    % Uncued
    p_shit_uncued       = mean(source_cor(old_trial & old_resp & uncued & good_trial));
    p_sdk_uncued    = mean(source_dk(old_trial & old_resp & uncued & good_trial));
    uncued_sourcePR = (p_shit_uncued - .5*(1-p_sdk_uncued)) / (1 - .5*(1-p_sdk_uncued));
   
    
    % Compute secondary measure of source memory performance (reviewer
    % suggestion)
    % Corrected source memory (hits-false alarms) as a function of
    % cue condition
    % hits = "manmade"|manmade + "shoebox"|shoebox
    %False alarm = "shoebox"|manmade + "manmade"|shoebox
    
    %False alarms 
    source_fa_informed      = mean(source_inc(old_trial & old_resp & informed & good_trial));
    source_fa_uninformed    = mean(source_inc(old_trial & old_resp & uninformed & good_trial));
    source_fa_uncued        = mean(source_inc(old_trial & old_resp & uncued & good_trial));
    %hits - FA
    cr_s_informed           = (p_shit_informed - source_fa_informed);
    cr_s_uninformed         = (p_shit_uninformed - source_fa_uninformed);
    cr_s_uncued             = (p_shit_uncued - source_fa_uncued);
    
     
    %compute new corrected source memory measrure for low (4/5 item response) and
    %high (6 item response) 
    old_low_resp        = ismember(test_data.item_resp,4:5); %old responses (4-guess old,5- maybe old,6 sure old) 
    old_high_resp       = ismember(test_data.item_resp,6); %old responses (4-guess old,5- maybe old,6 sure old) 
    % Calculate low confidence corrected source memory 
    % informed
    hit_s_low_informed          = mean(source_cor(old_trial & old_low_resp & informed & good_trial));
    source_fa_low_informed      = mean(source_inc(old_trial & old_low_resp & informed & good_trial));
    cr_s_low_informed           = (hit_s_low_informed - source_fa_low_informed);
    % uninformed
    hit_s_low_uninformed        = mean(source_cor(old_trial & old_low_resp & uninformed & good_trial));
    source_fa_low_uninformed    = mean(source_inc(old_trial & old_low_resp & uninformed & good_trial));
    cr_s_low_uninformed         = (hit_s_low_uninformed - source_fa_low_uninformed);
    % uncued
    hit_s_low_uncued            = mean(source_cor(old_trial & old_low_resp & uncued & good_trial));
    source_fa_low_uncued        = mean(source_inc(old_trial & old_low_resp & uncued & good_trial));
    cr_s_low_uncued             = (hit_s_low_uncued - source_fa_low_uncued);
    % calculate high confidence corrected source memory
    
    hit_s_high_informed          = mean(source_cor(old_trial & old_high_resp & informed & good_trial));
    source_fa_high_informed      = mean(source_inc(old_trial & old_high_resp & informed & good_trial));
    cr_s_high_informed           = (hit_s_high_informed - source_fa_high_informed);
    % uninformed
    hit_s_high_uninformed        = mean(source_cor(old_trial & old_high_resp & uninformed & good_trial));
    source_fa_high_uninformed    = mean(source_inc(old_trial & old_high_resp & uninformed & good_trial));
    cr_s_high_uninformed         = (hit_s_high_uninformed - source_fa_high_uninformed);
    % uncued
    hit_s_high_uncued            = mean(source_cor(old_trial & old_high_resp & uncued & good_trial));
    source_fa_high_uncued        = mean(source_inc(old_trial & old_high_resp & uncued & good_trial));
    cr_s_high_uncued             = (hit_s_high_uncued - source_fa_high_uncued);
 %% Check study judgment accuracy (reviewer comments)
    study_trial = ismember(test_data.old_new,'old');
    good_study_trial = test_data.study_good_trial;
    % 1 = yes, 2 = no
    study_hit = (ismember(test_data.study_resp,1) & ismember(test_data.study_judgment_correct_resp,1))|...
    (ismember(test_data.study_resp,2) & ismember(test_data.study_judgment_correct_resp,2));

    informed_study = mean(study_hit(old_trial & good_study_trial & informed));
    uninformed_study = mean(study_hit(old_trial & good_study_trial & uninformed));
    uncued_study = mean(study_hit(old_trial & good_study_trial & uncued));
    
    study_acc_data =  vertcat(study_acc_data, ...
        {participant status study_cb list 'informed' informed_study}, ...
        {participant status study_cb list 'uninformed' uninformed_study}, ...
        {participant status study_cb list 'uncued' uncued_study});
    
    
    % create pivot table
    % Add trial numbers
    for ii = 1:size(test_data,1)
        test_data.trial(ii) = ii;
    end
    pivot_table = vertcat(pivot_table,test_data);
    %% Store hit and FA data
    hit_fa_data = vertcat(hit_fa_data, ...
        {participant status study_cb list 'informed' informed_hits}, ...
        {participant status study_cb list 'uninformed' uninformed_hits}, ...
        {participant status study_cb list 'uncued' uncued_hits}, ...
        {participant status study_cb list 'new' false_alarms });
   
     memory_acc_data = vertcat(memory_acc_data, ...
        {participant status study_cb list 'informed' informed_auc informed_cor_recog informed_Ro informed_F cr_s_low_informed cr_s_high_informed cr_s_informed informed_sourcePR p_shit_informed p_sdk_informed}, ...
        {participant status study_cb list 'uninformed' uninformed_auc uninformed_cor_recog uninformed_Ro uninformed_F cr_s_low_uninformed cr_s_high_uninformed cr_s_uninformed uninformed_sourcePR p_shit_uninformed p_sdk_uninformed},...
        {participant status study_cb list 'uncued' uncued_auc uncued_cor_recog uncued_Ro uncued_F cr_s_low_uncued cr_s_high_uncued cr_s_uncued uncued_sourcePR p_shit_uncued p_sdk_uncued} );
 
    %% Step 5: Analysis of median RTs by cue condition and subsequent memory
    % Gather trials of use
    study_rts = test_data.study_rt; % Get out RTs now
    source_miss = source_dk | source_inc; % Create a source_miss bin
    
    % Get a median RT and store in study_rt_data
    study_rt_data = vertcat(study_rt_data, ...
        { participant status study_cb list 'informed'  'SC'   median(study_rts(informed & old_trial & old_resp & source_cor & good_trial)) }, ...
        { participant status study_cb list 'informed'  'SIDK' median(study_rts(informed & old_trial & old_resp & source_miss & good_trial)) }, ...
        { participant status study_cb list 'informed'  'Miss' median(study_rts(informed & old_trial & ~old_resp & good_trial)) }, ...
        { participant status study_cb list 'uninformed'  'SC'   median(study_rts(uninformed & old_trial & old_resp & source_cor & good_trial)) }, ...
        { participant status study_cb list 'uninformed'  'SIDK' median(study_rts(uninformed & old_trial & old_resp & source_miss & good_trial)) }, ...
        { participant status study_cb list 'uninformed'  'Miss' median(study_rts(uninformed & old_trial & ~old_resp & good_trial)) },...
        { participant status study_cb list 'uncued'  'SC'   median(study_rts(uncued & old_trial & old_resp & source_cor & good_trial)) }, ...
        { participant status study_cb list 'uncued'  'SIDK' median(study_rts(uncued & old_trial & old_resp & source_miss & good_trial)) }, ...
        { participant status study_cb list 'uncued'  'Miss' median(study_rts(uncued & old_trial & ~old_resp  & good_trial)) } );
        
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
        {participant 'uncued' 6 roc_data.observed_data.target.proportions(3,1) roc_data.observed_data.target.frequency(3,1)}, ...
        {participant 'uncued' 5 roc_data.observed_data.target.proportions(3,2) roc_data.observed_data.target.frequency(3,2)}, ...
        {participant 'uncued' 4 roc_data.observed_data.target.proportions(3,3) roc_data.observed_data.target.frequency(3,3)}, ...
        {participant 'uncued' 3 roc_data.observed_data.target.proportions(3,4) roc_data.observed_data.target.frequency(3,4)}, ...
        {participant 'uncued' 2 roc_data.observed_data.target.proportions(3,5) roc_data.observed_data.target.frequency(3,5)}, ...
        {participant 'uncued' 1 roc_data.observed_data.target.proportions(3,6) roc_data.observed_data.target.frequency(3,6)}, ...
        {participant 'new' 6 roc_data.observed_data.lure.proportions(1,1) roc_data.observed_data.lure.frequency(1,1)}, ...
        {participant 'new' 5 roc_data.observed_data.lure.proportions(1,2) roc_data.observed_data.lure.frequency(1,2)}, ...
        {participant 'new' 4 roc_data.observed_data.lure.proportions(1,3) roc_data.observed_data.lure.frequency(1,3)}, ...
        {participant 'new' 3 roc_data.observed_data.lure.proportions(1,4) roc_data.observed_data.lure.frequency(1,4)}, ...
        {participant 'new' 2 roc_data.observed_data.lure.proportions(1,5) roc_data.observed_data.lure.frequency(1,5)}, ...
        {participant 'new' 1 roc_data.observed_data.lure.proportions(1,6) roc_data.observed_data.lure.frequency(1,6)} ...
        );
    
   %% Step 6 collect aggregate data for ROC
    temp_targf = [];
    temp_luref = [];
        c = 1; % counter
     for i = 6:-1:1
            temp_targf(1,c) = sum( test_data.item_resp(old_trial & informed & good_trial) == i ) ;
            meta_targf(1,c) =  meta_targf(1,c) + temp_targf(1,c);
            
            temp_targf(2,c) = sum( test_data.item_resp(old_trial & uninformed & good_trial) == i ) ;
            meta_targf(2,c) = temp_targf(2,c)+ meta_targf(2,c);
            
            temp_targf(3,c) = sum( test_data.item_resp(old_trial & uncued & good_trial) == i ) ;
            meta_targf(3,c) = temp_targf(3,c)+ meta_targf(3,c);

            temp_luref(1,c) = sum( test_data.item_resp(~old_trial & good_trial) == i ) ;
            meta_luref(1,c) = temp_luref(1,c) + meta_luref(1,c);
            
            temp_luref(2,c) = temp_luref(1,c);
            meta_luref(2,c) = temp_luref(2,c) + meta_luref(2,c);
            
            temp_luref(3,c) = temp_luref(1,c);
            meta_luref(3,c) = temp_luref(3,c) + meta_luref(3,c);
            c = c+1;
     end

  
    
end

%% Step 7 Make each cell array a data table (in wide and long formats) and save data
study_acc_data_wide = unstack(study_acc_data,{'proportion'},'study_condition');
study_acc_data_wide = movevars(study_acc_data_wide,{'uncued'},'After','uninformed');

% Hit and FA data
hit_fa_data_wide = unstack(hit_fa_data,'proportion','study_condition', ...
    'NewDataVariableNames',{'informed_hits','false_alarms','uncued_hits','uninformed_hits'});
hit_fa_data_wide = movevars(hit_fa_data_wide,{'uninformed_hits','uncued_hits'},'After','informed_hits');

% Accuracy Measure Data
memory_acc_data_wide = unstack(memory_acc_data,{'auc' 'corrected_recognition','Ro','F','new_low_source','new_high_source','corrected_source','sourcePr' 'source_hit' 'source_dk'},'study_condition');
memory_acc_data_wide = movevars(memory_acc_data_wide,{'corrected_recognition_uncued'},'After','corrected_recognition_uninformed');
memory_acc_data_wide = movevars(memory_acc_data_wide,{'Ro_uncued'},'After','Ro_uninformed');
memory_acc_data_wide = movevars(memory_acc_data_wide,{'F_uncued'},'After','F_uninformed');
memory_acc_data_wide = movevars(memory_acc_data_wide,{'sourcePr_uncued'},'After','sourcePr_uninformed');
memory_acc_data_wide = movevars(memory_acc_data_wide,{'auc_uncued'},'After','auc_uninformed');
memory_acc_data_wide = movevars(memory_acc_data_wide,{'corrected_source_uncued'},'After','corrected_source_uninformed');
memory_acc_data_wide = movevars(memory_acc_data_wide,{'new_low_source_uncued'},'After','new_low_source_uninformed');
memory_acc_data_wide = movevars(memory_acc_data_wide,{'new_high_source_uncued'},'After','new_high_source_uninformed');


% Study RT Data
study_rt_data_wide = unstack(study_rt_data,'median_rt','study_condition');
study_rt_data_wide = unstack(study_rt_data_wide,{'informed' 'uncued' 'uninformed'},'subsequent_memory');
study_rt_data_wide.Properties.VariableNames(5:end) = ...
    cellfun(@(x) strcat(x,'_median_studyrt'), study_rt_data_wide.Properties.VariableNames(5:end), 'UniformOutput', false);
study_rt_data_wide = movevars(study_rt_data_wide,{'uninformed_Miss_median_studyrt'},'After','informed_SIDK_median_studyrt');
study_rt_data_wide = movevars(study_rt_data_wide,{'uninformed_SC_median_studyrt'},'After','uninformed_Miss_median_studyrt');
study_rt_data_wide = movevars(study_rt_data_wide,{ 'uninformed_SIDK_median_studyrt'},'After','uninformed_SC_median_studyrt');


% Join the three wide data tables
all_data_wide = join(hit_fa_data_wide,memory_acc_data_wide);
all_data_wide = join(all_data_wide,study_rt_data_wide);


% Write ALL data tables to file
writetable(study_acc_data_wide,fullfile(directories.analyses,'study_acc_data_wide.csv'));

writetable(hit_fa_data,fullfile(directories.analyses,'hit_fa_data_long.csv'));
writetable(memory_acc_data,fullfile(directories.analyses,'memory_measures_data_long.csv'));
writetable(study_rt_data,fullfile(directories.analyses,'study_rt_data_long.csv'));
writetable(all_data_wide,fullfile(directories.analyses,'all_data_wide.csv'));
writetable(conf_data,fullfile(directories.analyses,'conf_data_long.csv'),'FileType','text','Delimiter','\t');
writetable(study_rt_data_wide,fullfile(directories.analyses,'studyrt_wide.csv'));
writetable(pivot_table,fullfile(directories.analyses,'pivot_table.csv'));


%% Step 8 get ROC values aggregated across participants
% Fit with roc_solver
    % Specify model design options
    model = 'dpsd';
    [nConds, nBins] = size(meta_targf);
    parNames = {'Ro' 'F'};
    ignoreConds = 2:3; % Ignore fit values for 2nd and 3rd rows in luref (3 old, 1 new design)
    fitStat = '-LL';
    
    % Specify other options for bookkeeping
    condLabels = {'Informed' 'Uninformed' 'Uncued'};
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
    save(fullfile(directories.par_analysis,'meta_roc_data.mat'),'roc_data');
meta_data = cell2table(  cell(0,5),...
    'VariableNames', {'meta' 'informed' 'uninformed' 'uncued' 'Fa_pred'});

hit_pred = array2table(roc_data.dpsd_model.predicted_rocs.roc.target',...
    'VariableNames',{'informed_pred' 'uninformed_pred' 'uncued_pred'});

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
    {1 'uninformed' roc_data.observed_data.target.cumulative(2,6) roc_data.observed_data.lure.cumulative(2,6) },...
    {6 'uncued' roc_data.observed_data.target.cumulative(3,1) roc_data.observed_data.lure.cumulative(3,1) }, ...
    {5 'uncued' roc_data.observed_data.target.cumulative(3,2) roc_data.observed_data.lure.cumulative(3,2) }, ...
    {4 'uncued' roc_data.observed_data.target.cumulative(3,3) roc_data.observed_data.lure.cumulative(3,3) }, ...
    {3 'uncued' roc_data.observed_data.target.cumulative(3,4) roc_data.observed_data.lure.cumulative(3,4) }, ...
    {2 'uncued' roc_data.observed_data.target.cumulative(3,5) roc_data.observed_data.lure.cumulative(3,5) }, ...
    {1 'uncued' roc_data.observed_data.target.cumulative(3,6) roc_data.observed_data.lure.cumulative(3,6) });
     

% save aggregate ROC values 
writetable(meta_data,fullfile(directories.analyses,'meta_person.csv'),'FileType','text','Delimiter',',');
writetable(meta_cumulative_data,fullfile(directories.analyses,'meta_average.csv'),'FileType','text','Delimiter',',');

