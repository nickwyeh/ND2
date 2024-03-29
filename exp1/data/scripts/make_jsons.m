% ndg Exp 1
% create study and test json files
root_dir = 'C:\Users\nyeh\Desktop\fall_2021\NDG\exp1\data';

project_label = 'raw';
task_id = '';

task_json_name = fullfile(root_dir,project_label,...
    'task-study_description.json');
% Define JSON options
json_options.indent = '    ';    

% Make task-study_beh.json (UPDATE DIRECTORY)
study_json_file = fullfile(pwd,'task-study_beh.json');
study_json = struct();
study_json.task.Description = 'In this task participants viewed negative and neutral scenes and were instructed to either decrease their emotions or passively view the scenes. Note decrease instructions were only paired with negative scenes';
study_json.id.Description              = 'Participant id code';
study_json.arousal_resp_keys.Description = 'Arousal ratings from 1 = very calm to 6 = very intense';
study_json.arousal_resp_rt.Description = 'Arousal ratings reaction times';
study_json.study_success_resp_key.Description = 'Reappraisal success rates for decrease instructions (1= successful, 0 = unsuccessful, n/a = view trial';
study_json.study_success_rt.Description = 'Reappraisal success rates reaction times with -99 for view trials';
study_json.study_arousal_rating.Description = 'Arousal ratings from 1 = very calm to 6 = very intense';
study_json.study_arousal_rt.Description = 'Arousal ratings reaction times';
study_json.test_file.Description              = 'Test file counterbalance number: A, B, or C';
study_json.phase_name.Description              = 'Block phase coded as valence (negative, neutral), instruction (decrease1-6, view1-6), and listnumber (1-2; e.g., neutral_view1_study1). ';
study_json.phase_progress.Description              = 'Indicates practice or real phase';
study_json.image.Description                = 'Image presented. Note whole images were created by placing objects on backgrounds';
study_json.instruction.Description                = 'Study instructions: Decrease or View';
study_json.valence.Description                = 'Valence of image/scene: negativie, neutral';
study_json.sc_code.Description                = 'Unique id scene component code: 1-180';
study_json.success_resp_keys.Description               = 'Reappraisal success rates for decrease instructions (1= successful, 0 = unsuccessful, n/a = view trial';
study_json.success_resp_rt.Description                = 'Reappraisal success rates reaction times with -99 for view trials';
study_json.original_scene.Description              = 'Image presented. Note whole images were created by placing objects on backgrounds';
study_json.set.Description                = 'Image set list: 1-2, NAN for view trials';
study_json.cb.Description              = 'Counterbalance for instruction block presentation: A, B, C';
study_json.study_R_trial.Description                = 'Decrease/Reappraisal instructions are coded as 1 and view trials as 0';
study_json.study_success_rating.Description                = 'Reappraisal success ratings recoded as success, failure, and na for view trials';
jsonwrite(study_json_file,study_json,json_options);

% Make task-test_beh.json (UPDATE DIRECTORY)
project_label = 'raw';
task_id = '';

task_json_name = fullfile(root_dir,project_label,...
    'task-test_description.json');
% Define JSON options
json_options.indent = '    ';    
%  task-test information

test_json_file = fullfile(pwd,'task-test_beh.json');
test_json.task_test.Description = 'Participants completed an incidental recognition test. Participants were presented whole scenes from the study phase decomposed into objects and background scene components and lure scene components.  Note all backgrounds were neutral but were paired with negative or neutral objects.';
test_json.scene_type_resp_keys.Description = 'Participants memory response: 1 = old, 0 = new';
test_json.scene_type_resp_rt.Description = 'Participants memory response reaction times';
test_json.test_item_resp.Description = 'Participants memory response: 1 = old, 0 = new';
test_json.test_type_rt.Description  = 'Participants memory response reaction times';
test_json.old_new_resp.Description = 'Participants memory responses recoded as old or new';
test_json.item_acc.Description = 'Memory accuracy: 1 = hit (old-old, new-new), 0 miss (old-new, new-old)';
test_json.phase_name.Description =  'Test phase: _prac or _crit. Crit trials are the real experimental trials';
test_json.image.Description = 'Scene component (object or background) image name';
test_json.sc_image.Description = 'Scene component (object or background) image name';
test_json.sc_type.Description = 'Scene component type: object, background';
test_json.sc_valence.Description = 'Scene component valence: negative, neutral';
test_json.sc_code.Description = 'Scene component code that maps to unique whole scene id from study phase: 1-180, nan for foil images';
test_json.old_new.Description = 'Scene component memory type: old (previously seen), new (lure item)';
test_json.original_scene.Description = 'Original scenes that the objects and backgrounds were decomposed from. NaN for lure items';
test_json.scene_code.Description = 'Scene component code that maps to unique whole scene id from study phase: 1-180, nan for foil images';
test_json.scene_valence.Description = 'Original scene valence: negative, neutral, na for new/lure items. ';
test_json.date.Description = 'Participants task completion date';
test_json.cb.Description = 'Participants counterbalance: A, B, C';
test_json.id.Description = 'Participant ID';
test_json.test_resp_acc.Description = 'Numerically mark if trial is good (1) or bad (0) based on if participants test performance (item memory and using entire range of confidence scale), see prereg for more information ';
json_options.indent               = '    '; % this makes the json look prettier when opened in a txt editor
jsonwrite(test_json_file,test_json,json_options);
