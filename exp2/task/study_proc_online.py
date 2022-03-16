#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v3.2.4),
    on April 03, 2020, at 08:14
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

import psychopy
psychopy.useVersion('latest')


from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '3.2.4'
expName = 'study_proc'  # from the Builder filename that created this script
expInfo = {'id': '', 'study_cb': ['A', 'B']}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'archive/%s_%s_%s' % (expInfo['id'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\Nick\\Desktop\\nick\\nd002\\exp2\\task\\study_proc_online.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=[1536, 864], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=True, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "experiment_setup"
experiment_setupClock = core.Clock()
#code subject ID in correct format

expInfo['id'] = 'sub-p2e2s'+ expInfo['id']

if expInfo['study_cb'] == 'A':
    phase_file = 'study_cbA_phases.csv'
else:
    phase_file = 'study_cbB_phases.csv'
# study set up scale responses for pleasantness judgement
study_scale = {
        'j':1,
        'k':2,
        'l':3,
        'na':-99
        }
# test scale set up
item_scale = {
        's':1,
        'd':2,
        'f':3,
        'j':4,
        'k':5,
        'l':6,
        None :-99,
        '':-99
        }
        
source_scale = {
        'j':'manmade',
        'k':'shoebox',
        'l':'dk',
        None:'n/a',
        '':'n/a'
        }
# Print framerate
print(expInfo['frameRate'])

# Study set up
#frames
vis_cue_dur = round( .5 / frameDur ) # Length of cue in frames
vis_cue_fix_dur = round( .5 / frameDur ) # Length of the cue-target interval after cue offset
vis_word_dur = round( .5 / frameDur ) # Average of auditory file lengths
vis_word_fix_dur = round( 1.5 / frameDur )


# test set up
initial_delay_frames = round( 0.250 / frameDur ) # 250 millisecond initial fixation
word_duration_frames = round( 0.500 / frameDur ) # 500 millisecond 
test_delay_frames = round(5.00/frameDur)
test_maxtime_frames = round(10.00/frameDur)
test_iti_frames = round(.5/frameDur)
sm_kb_wait_frames = round(.2/frameDur) # allow for a short delay in KB press from item to source memory

# Initialize components for Routine "phase_setup"
phase_setupClock = core.Clock()

# Initialize components for Routine "instructions"
instructionsClock = core.Clock()
instructions_image = visual.ImageStim(
    win=win,
    name='instructions_image', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=[1.2,.8],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
instructions_resp = keyboard.Keyboard()

# Initialize components for Routine "pause_routine"
pause_routineClock = core.Clock()
pause_text = visual.TextStim(win=win, name='pause_text',
    text='+',
    font='Arial',
    pos=(0, 0), height=.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "visual_cue_routine"
visual_cue_routineClock = core.Clock()
visual_cue_rect = visual.Rect(
    win=win, name='visual_cue_rect',
    width=[.07,.07][0], height=[.07,.07][1],
    ori=0, pos=(0,0),
    lineWidth=1, lineColor=1.0, lineColorSpace='rgb',
    fillColor=1.0, fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
visual_cue_fixation = visual.TextStim(win=win, name='visual_cue_fixation',
    text='+',
    font='Arial',
    pos=(0, 0), height=.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "visual_word_routine"
visual_word_routineClock = core.Clock()
uninformed_cue_box = visual.Rect(
    win=win, name='uninformed_cue_box',
    width=[.3,.15][0], height=[.3,.15][1],
    ori=0, pos=(0, 0),
    lineWidth=6, lineColor=1.0, lineColorSpace='rgb',
    fillColor=None, fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
visual_word_text = visual.TextStim(win=win, name='visual_word_text',
    text='default text',
    font='Arial',
    pos=(0, 0), height=.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
visual_word_fixation = visual.TextStim(win=win, name='visual_word_fixation',
    text='+',
    font='Arial',
    pos=(0, 0), height=.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);
visual_resp = keyboard.Keyboard()

# Initialize components for Routine "code_study_resp"
code_study_respClock = core.Clock()

# Initialize components for Routine "pause_routine"
pause_routineClock = core.Clock()
pause_text = visual.TextStim(win=win, name='pause_text',
    text='+',
    font='Arial',
    pos=(0, 0), height=.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "study_complete"
study_completeClock = core.Clock()
study_complete_text = visual.TextStim(win=win, name='study_complete_text',
    text='This phase is complete.\n\nPlease wait for futher instructions.',
    font='Arial',
    pos=(0, 0), height=.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "test_phase_setup"
test_phase_setupClock = core.Clock()

# Initialize components for Routine "test_instructions"
test_instructionsClock = core.Clock()
test_instructions_image = visual.ImageStim(
    win=win,
    name='test_instructions_image', 
    image='test_instructions.png', mask=None,
    ori=0, pos=(0, 0), size=[1.2,.8],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
test_instr_resp = keyboard.Keyboard()

# Initialize components for Routine "warn_prac_or_crit"
warn_prac_or_critClock = core.Clock()
warning_text = visual.TextStim(win=win, name='warning_text',
    text='default text',
    font='Arial',
    pos=(0, 0), height=.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
warning_key_resp = keyboard.Keyboard()

# Initialize components for Routine "test_break"
test_breakClock = core.Clock()
break_n = 80
draw_test_break = visual.TextStim(win=win, name='draw_test_break',
    text='Take a break to relax\n\nPress b to begin ',
    font='Arial',
    pos=(0, 0), height=.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
draw_test_break_key_resp = keyboard.Keyboard()

# Initialize components for Routine "test_delay"
test_delayClock = core.Clock()
test_delay_text = visual.TextStim(win=win, name='test_delay_text',
    text='+',
    font='Arial',
    pos=(0, 0), height=.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "item_memory"
item_memoryClock = core.Clock()
item_scale_image = visual.ImageStim(
    win=win,
    name='item_scale_image', 
    image='item_scale.png', mask=None,
    ori=0, pos=(0, -.2), size=[1,.2],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
item_stimuli = visual.TextStim(win=win, name='item_stimuli',
    text='default text',
    font='Arial',
    pos=(0, 0), height=.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
item_key_resp = keyboard.Keyboard()

# Initialize components for Routine "source_memory"
source_memoryClock = core.Clock()
source_scale_image = visual.ImageStim(
    win=win,
    name='source_scale_image', 
    image='source_scale.png', mask=None,
    ori=0, pos=(0, -.2), size=[.9,.2],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
item_stimuli_text = visual.TextStim(win=win, name='item_stimuli_text',
    text='default text',
    font='Arial',
    pos=(0, 0), height=.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);
source_key_resp = keyboard.Keyboard()

# Initialize components for Routine "test_iti"
test_itiClock = core.Clock()
test_iti_text = visual.TextStim(win=win, name='test_iti_text',
    text='+',
    font='Arial',
    pos=(0, 0), height=.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "code_test_resp"
code_test_respClock = core.Clock()

# Initialize components for Routine "test_complete"
test_completeClock = core.Clock()
test_complete_text = visual.TextStim(win=win, name='test_complete_text',
    text='This phase is now complete.',
    font='Arial',
    pos=(0, 0), height=.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "experiment_setup"-------
# update component parameters for each repeat
# keep track of which components have finished
experiment_setupComponents = []
for thisComponent in experiment_setupComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
experiment_setupClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1
continueRoutine = True

# -------Run Routine "experiment_setup"-------
while continueRoutine:
    # get current time
    t = experiment_setupClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=experiment_setupClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in experiment_setupComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "experiment_setup"-------
for thisComponent in experiment_setupComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "experiment_setup" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
phases = data.TrialHandler(nReps=0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(phase_file),
    seed=None, name='phases')
thisExp.addLoop(phases)  # add the loop to the experiment
thisPhase = phases.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisPhase.rgb)
if thisPhase != None:
    for paramName in thisPhase:
        exec('{} = thisPhase[paramName]'.format(paramName))

for thisPhase in phases:
    currentLoop = phases
    # abbreviate parameter names if possible (e.g. rgb = thisPhase.rgb)
    if thisPhase != None:
        for paramName in thisPhase:
            exec('{} = thisPhase[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "phase_setup"-------
    # update component parameters for each repeat
    #select practice or test file (define first then add path if not practice)
    stim_file = phase_name +'.csv'
    print(stim_file)
    if phase_name == 'informed_prac'or phase_name == 'informed1_study' or phase_name =='informed2_study':
        instruction_img_file = 'informed_instructions_square.png'
    else:
        instruction_img_file = 'uninformed_instructions.png'
        
    # Create the data file name for saving this list
    
    #Create data file to save to
    
    #suffix = expInfo['id'] +'_task-study_run-'+ phase_name
    #save_file = os.path.join(save_dir, suffix)
    
    # Print info
    #print(phase_name)
    #print(stim_file)
    # keep track of which components have finished
    phase_setupComponents = []
    for thisComponent in phase_setupComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    phase_setupClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    continueRoutine = True
    
    # -------Run Routine "phase_setup"-------
    while continueRoutine:
        # get current time
        t = phase_setupClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=phase_setupClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in phase_setupComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "phase_setup"-------
    for thisComponent in phase_setupComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "phase_setup" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "instructions"-------
    # update component parameters for each repeat
    instructions_image.setImage(instruction_img_file)
    instructions_resp.keys = []
    instructions_resp.rt = []
    # keep track of which components have finished
    instructionsComponents = [instructions_image, instructions_resp]
    for thisComponent in instructionsComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    instructionsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    continueRoutine = True
    
    # -------Run Routine "instructions"-------
    while continueRoutine:
        # get current time
        t = instructionsClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=instructionsClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instructions_image* updates
        if instructions_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instructions_image.frameNStart = frameN  # exact frame index
            instructions_image.tStart = t  # local t and not account for scr refresh
            instructions_image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instructions_image, 'tStartRefresh')  # time at next scr refresh
            instructions_image.setAutoDraw(True)
        
        # *instructions_resp* updates
        waitOnFlip = False
        if instructions_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instructions_resp.frameNStart = frameN  # exact frame index
            instructions_resp.tStart = t  # local t and not account for scr refresh
            instructions_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instructions_resp, 'tStartRefresh')  # time at next scr refresh
            instructions_resp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(instructions_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if instructions_resp.status == STARTED and not waitOnFlip:
            theseKeys = instructions_resp.getKeys(keyList=['space'], waitRelease=False)
            if len(theseKeys):
                theseKeys = theseKeys[0]  # at least one key was pressed
                
                # check for quit:
                if "escape" == theseKeys:
                    endExpNow = True
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in instructionsComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "instructions"-------
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    phases.addData('instructions_image.started', instructions_image.tStartRefresh)
    phases.addData('instructions_image.stopped', instructions_image.tStopRefresh)
    # the Routine "instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "pause_routine"-------
    routineTimer.add(3.000000)
    # update component parameters for each repeat
    # keep track of which components have finished
    pause_routineComponents = [pause_text]
    for thisComponent in pause_routineComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    pause_routineClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    continueRoutine = True
    
    # -------Run Routine "pause_routine"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = pause_routineClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=pause_routineClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *pause_text* updates
        if pause_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            pause_text.frameNStart = frameN  # exact frame index
            pause_text.tStart = t  # local t and not account for scr refresh
            pause_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(pause_text, 'tStartRefresh')  # time at next scr refresh
            pause_text.setAutoDraw(True)
        if pause_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > pause_text.tStartRefresh + 3-frameTolerance:
                # keep track of stop time/frame for later
                pause_text.tStop = t  # not accounting for scr refresh
                pause_text.frameNStop = frameN  # exact frame index
                win.timeOnFlip(pause_text, 'tStopRefresh')  # time at next scr refresh
                pause_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in pause_routineComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "pause_routine"-------
    for thisComponent in pause_routineComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    phases.addData('pause_text.started', pause_text.tStartRefresh)
    phases.addData('pause_text.stopped', pause_text.tStopRefresh)
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=1, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(stim_file),
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))
    
    for thisTrial in trials:
        currentLoop = trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                exec('{} = thisTrial[paramName]'.format(paramName))
        
        # set up handler to look after randomisation of conditions etc
        vis_cue_loop = data.TrialHandler(nReps=show_cue, method='sequential', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='vis_cue_loop')
        thisExp.addLoop(vis_cue_loop)  # add the loop to the experiment
        thisVis_cue_loop = vis_cue_loop.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisVis_cue_loop.rgb)
        if thisVis_cue_loop != None:
            for paramName in thisVis_cue_loop:
                exec('{} = thisVis_cue_loop[paramName]'.format(paramName))
        
        for thisVis_cue_loop in vis_cue_loop:
            currentLoop = vis_cue_loop
            # abbreviate parameter names if possible (e.g. rgb = thisVis_cue_loop.rgb)
            if thisVis_cue_loop != None:
                for paramName in thisVis_cue_loop:
                    exec('{} = thisVis_cue_loop[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "visual_cue_routine"-------
            # update component parameters for each repeat
            visual_cue_rect.setFillColor(cue_color)
            visual_cue_rect.setLineColor(cue_color)
            # keep track of which components have finished
            visual_cue_routineComponents = [visual_cue_rect, visual_cue_fixation]
            for thisComponent in visual_cue_routineComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            visual_cue_routineClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            continueRoutine = True
            
            # -------Run Routine "visual_cue_routine"-------
            while continueRoutine:
                # get current time
                t = visual_cue_routineClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=visual_cue_routineClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *visual_cue_rect* updates
                if visual_cue_rect.status == NOT_STARTED and frameN >= 0:
                    # keep track of start time/frame for later
                    visual_cue_rect.frameNStart = frameN  # exact frame index
                    visual_cue_rect.tStart = t  # local t and not account for scr refresh
                    visual_cue_rect.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(visual_cue_rect, 'tStartRefresh')  # time at next scr refresh
                    visual_cue_rect.setAutoDraw(True)
                if visual_cue_rect.status == STARTED:
                    if frameN >= (visual_cue_rect.frameNStart + vis_cue_dur):
                        # keep track of stop time/frame for later
                        visual_cue_rect.tStop = t  # not accounting for scr refresh
                        visual_cue_rect.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(visual_cue_rect, 'tStopRefresh')  # time at next scr refresh
                        visual_cue_rect.setAutoDraw(False)
                
                # *visual_cue_fixation* updates
                if visual_cue_fixation.status == NOT_STARTED and frameN >= vis_cue_dur:
                    # keep track of start time/frame for later
                    visual_cue_fixation.frameNStart = frameN  # exact frame index
                    visual_cue_fixation.tStart = t  # local t and not account for scr refresh
                    visual_cue_fixation.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(visual_cue_fixation, 'tStartRefresh')  # time at next scr refresh
                    visual_cue_fixation.setAutoDraw(True)
                if visual_cue_fixation.status == STARTED:
                    if frameN >= (visual_cue_fixation.frameNStart + vis_cue_fix_dur):
                        # keep track of stop time/frame for later
                        visual_cue_fixation.tStop = t  # not accounting for scr refresh
                        visual_cue_fixation.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(visual_cue_fixation, 'tStopRefresh')  # time at next scr refresh
                        visual_cue_fixation.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in visual_cue_routineComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "visual_cue_routine"-------
            for thisComponent in visual_cue_routineComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            vis_cue_loop.addData('visual_cue_rect.started', visual_cue_rect.tStartRefresh)
            vis_cue_loop.addData('visual_cue_rect.stopped', visual_cue_rect.tStopRefresh)
            vis_cue_loop.addData('visual_cue_fixation.started', visual_cue_fixation.tStartRefresh)
            vis_cue_loop.addData('visual_cue_fixation.stopped', visual_cue_fixation.tStopRefresh)
            # the Routine "visual_cue_routine" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
        # completed show_cue repeats of 'vis_cue_loop'
        
        
        # ------Prepare to start Routine "visual_word_routine"-------
        # update component parameters for each repeat
        uninformed_cue_box.setLineColor(box_color)
        visual_word_text.setText(word)
        visual_resp.keys = []
        visual_resp.rt = []
        # keep track of which components have finished
        visual_word_routineComponents = [uninformed_cue_box, visual_word_text, visual_word_fixation, visual_resp]
        for thisComponent in visual_word_routineComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        visual_word_routineClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True
        
        # -------Run Routine "visual_word_routine"-------
        while continueRoutine:
            # get current time
            t = visual_word_routineClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=visual_word_routineClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *uninformed_cue_box* updates
            if uninformed_cue_box.status == NOT_STARTED and frameN >= 0:
                # keep track of start time/frame for later
                uninformed_cue_box.frameNStart = frameN  # exact frame index
                uninformed_cue_box.tStart = t  # local t and not account for scr refresh
                uninformed_cue_box.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(uninformed_cue_box, 'tStartRefresh')  # time at next scr refresh
                uninformed_cue_box.setAutoDraw(True)
            if uninformed_cue_box.status == STARTED:
                if frameN >= (uninformed_cue_box.frameNStart + vis_word_dur):
                    # keep track of stop time/frame for later
                    uninformed_cue_box.tStop = t  # not accounting for scr refresh
                    uninformed_cue_box.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(uninformed_cue_box, 'tStopRefresh')  # time at next scr refresh
                    uninformed_cue_box.setAutoDraw(False)
            
            # *visual_word_text* updates
            if visual_word_text.status == NOT_STARTED and frameN >= 0:
                # keep track of start time/frame for later
                visual_word_text.frameNStart = frameN  # exact frame index
                visual_word_text.tStart = t  # local t and not account for scr refresh
                visual_word_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(visual_word_text, 'tStartRefresh')  # time at next scr refresh
                visual_word_text.setAutoDraw(True)
            if visual_word_text.status == STARTED:
                if frameN >= (visual_word_text.frameNStart + vis_word_dur):
                    # keep track of stop time/frame for later
                    visual_word_text.tStop = t  # not accounting for scr refresh
                    visual_word_text.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(visual_word_text, 'tStopRefresh')  # time at next scr refresh
                    visual_word_text.setAutoDraw(False)
            
            # *visual_word_fixation* updates
            if visual_word_fixation.status == NOT_STARTED and frameN >= vis_word_dur:
                # keep track of start time/frame for later
                visual_word_fixation.frameNStart = frameN  # exact frame index
                visual_word_fixation.tStart = t  # local t and not account for scr refresh
                visual_word_fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(visual_word_fixation, 'tStartRefresh')  # time at next scr refresh
                visual_word_fixation.setAutoDraw(True)
            if visual_word_fixation.status == STARTED:
                if frameN >= (visual_word_fixation.frameNStart + vis_word_fix_dur):
                    # keep track of stop time/frame for later
                    visual_word_fixation.tStop = t  # not accounting for scr refresh
                    visual_word_fixation.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(visual_word_fixation, 'tStopRefresh')  # time at next scr refresh
                    visual_word_fixation.setAutoDraw(False)
            
            # *visual_resp* updates
            waitOnFlip = False
            if visual_resp.status == NOT_STARTED and frameN >= 0:
                # keep track of start time/frame for later
                visual_resp.frameNStart = frameN  # exact frame index
                visual_resp.tStart = t  # local t and not account for scr refresh
                visual_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(visual_resp, 'tStartRefresh')  # time at next scr refresh
                visual_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(visual_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(visual_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if visual_resp.status == STARTED:
                if frameN >= (visual_resp.frameNStart + vis_word_dur + vis_word_fix_dur):
                    # keep track of stop time/frame for later
                    visual_resp.tStop = t  # not accounting for scr refresh
                    visual_resp.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(visual_resp, 'tStopRefresh')  # time at next scr refresh
                    visual_resp.status = FINISHED
            if visual_resp.status == STARTED and not waitOnFlip:
                theseKeys = visual_resp.getKeys(keyList=['j', 'k'], waitRelease=False)
                if len(theseKeys):
                    theseKeys = theseKeys[0]  # at least one key was pressed
                    
                    # check for quit:
                    if "escape" == theseKeys:
                        endExpNow = True
                    if visual_resp.keys == []:  # then this was the first keypress
                        visual_resp.keys = theseKeys.name  # just the first key pressed
                        visual_resp.rt = theseKeys.rt
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in visual_word_routineComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "visual_word_routine"-------
        for thisComponent in visual_word_routineComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trials.addData('uninformed_cue_box.started', uninformed_cue_box.tStartRefresh)
        trials.addData('uninformed_cue_box.stopped', uninformed_cue_box.tStopRefresh)
        trials.addData('visual_word_text.started', visual_word_text.tStartRefresh)
        trials.addData('visual_word_text.stopped', visual_word_text.tStopRefresh)
        trials.addData('visual_word_fixation.started', visual_word_fixation.tStartRefresh)
        trials.addData('visual_word_fixation.stopped', visual_word_fixation.tStopRefresh)
        # check responses
        if visual_resp.keys in ['', [], None]:  # No response was made
            visual_resp.keys = None
        trials.addData('visual_resp.keys',visual_resp.keys)
        if visual_resp.keys != None:  # we had a response
            trials.addData('visual_resp.rt', visual_resp.rt)
        trials.addData('visual_resp.started', visual_resp.tStartRefresh)
        trials.addData('visual_resp.stopped', visual_resp.tStopRefresh)
        # the Routine "visual_word_routine" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "code_study_resp"-------
        # update component parameters for each repeat
        # Extract the appropriate response from the correct object
        
        study_resp_key = visual_resp.keys
        study_rt   = visual_resp.rt
        
        # Update response if necessary
        if study_resp_key == None or study_resp_key =='':
            study_resp_key = 'na'
            study_rt = -99
        else:
            study_resp_key = study_resp_key
            study_rt = study_rt
        
        # Code study response
        study_resp = study_scale[study_resp_key]
        
        # Debugging information
        #print('{}, {}, {}'.format(study_resp_key,study_resp,study_rt))
        
        # Store in trials object
        trials.addData('study_resp_key',study_resp_key)
        trials.addData('study_resp',study_resp)
        trials.addData('study_rt',study_rt)
        
        
        
        
        
        # keep track of which components have finished
        code_study_respComponents = []
        for thisComponent in code_study_respComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        code_study_respClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True
        
        # -------Run Routine "code_study_resp"-------
        while continueRoutine:
            # get current time
            t = code_study_respClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=code_study_respClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in code_study_respComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "code_study_resp"-------
        for thisComponent in code_study_respComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # the Routine "code_study_resp" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1 repeats of 'trials'
    
    
    # ------Prepare to start Routine "pause_routine"-------
    routineTimer.add(3.000000)
    # update component parameters for each repeat
    # keep track of which components have finished
    pause_routineComponents = [pause_text]
    for thisComponent in pause_routineComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    pause_routineClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    continueRoutine = True
    
    # -------Run Routine "pause_routine"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = pause_routineClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=pause_routineClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *pause_text* updates
        if pause_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            pause_text.frameNStart = frameN  # exact frame index
            pause_text.tStart = t  # local t and not account for scr refresh
            pause_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(pause_text, 'tStartRefresh')  # time at next scr refresh
            pause_text.setAutoDraw(True)
        if pause_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > pause_text.tStartRefresh + 3-frameTolerance:
                # keep track of stop time/frame for later
                pause_text.tStop = t  # not accounting for scr refresh
                pause_text.frameNStop = frameN  # exact frame index
                win.timeOnFlip(pause_text, 'tStopRefresh')  # time at next scr refresh
                pause_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in pause_routineComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "pause_routine"-------
    for thisComponent in pause_routineComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    phases.addData('pause_text.started', pause_text.tStartRefresh)
    phases.addData('pause_text.stopped', pause_text.tStopRefresh)
# completed 0 repeats of 'phases'


# ------Prepare to start Routine "study_complete"-------
routineTimer.add(5.000000)
# update component parameters for each repeat
# keep track of which components have finished
study_completeComponents = [study_complete_text]
for thisComponent in study_completeComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
study_completeClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1
continueRoutine = True

# -------Run Routine "study_complete"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = study_completeClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=study_completeClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *study_complete_text* updates
    if study_complete_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        study_complete_text.frameNStart = frameN  # exact frame index
        study_complete_text.tStart = t  # local t and not account for scr refresh
        study_complete_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(study_complete_text, 'tStartRefresh')  # time at next scr refresh
        study_complete_text.setAutoDraw(True)
    if study_complete_text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > study_complete_text.tStartRefresh + 5-frameTolerance:
            # keep track of stop time/frame for later
            study_complete_text.tStop = t  # not accounting for scr refresh
            study_complete_text.frameNStop = frameN  # exact frame index
            win.timeOnFlip(study_complete_text, 'tStopRefresh')  # time at next scr refresh
            study_complete_text.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in study_completeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "study_complete"-------
for thisComponent in study_completeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('study_complete_text.started', study_complete_text.tStartRefresh)
thisExp.addData('study_complete_text.stopped', study_complete_text.tStopRefresh)

# set up handler to look after randomisation of conditions etc
test_phase = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('test_phase_names.csv'),
    seed=None, name='test_phase')
thisExp.addLoop(test_phase)  # add the loop to the experiment
thisTest_phase = test_phase.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTest_phase.rgb)
if thisTest_phase != None:
    for paramName in thisTest_phase:
        exec('{} = thisTest_phase[paramName]'.format(paramName))

for thisTest_phase in test_phase:
    currentLoop = test_phase
    # abbreviate parameter names if possible (e.g. rgb = thisTest_phase.rgb)
    if thisTest_phase != None:
        for paramName in thisTest_phase:
            exec('{} = thisTest_phase[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "test_phase_setup"-------
    # update component parameters for each repeat
    #select practice or test file
    if phase_name == '_prac':
        test_task = 'practest'
        stim_file_test = 'prac_test.csv'
    else:
        test_task = 'test'
        stim_file_test = 'test.csv'
    # keep track of which components have finished
    test_phase_setupComponents = []
    for thisComponent in test_phase_setupComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    test_phase_setupClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    continueRoutine = True
    
    # -------Run Routine "test_phase_setup"-------
    while continueRoutine:
        # get current time
        t = test_phase_setupClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=test_phase_setupClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in test_phase_setupComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "test_phase_setup"-------
    for thisComponent in test_phase_setupComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "test_phase_setup" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "test_instructions"-------
    # update component parameters for each repeat
    test_instr_resp.keys = []
    test_instr_resp.rt = []
    # keep track of which components have finished
    test_instructionsComponents = [test_instructions_image, test_instr_resp]
    for thisComponent in test_instructionsComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    test_instructionsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    continueRoutine = True
    
    # -------Run Routine "test_instructions"-------
    while continueRoutine:
        # get current time
        t = test_instructionsClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=test_instructionsClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *test_instructions_image* updates
        if test_instructions_image.status == NOT_STARTED and frameN >= 0.0:
            # keep track of start time/frame for later
            test_instructions_image.frameNStart = frameN  # exact frame index
            test_instructions_image.tStart = t  # local t and not account for scr refresh
            test_instructions_image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(test_instructions_image, 'tStartRefresh')  # time at next scr refresh
            test_instructions_image.setAutoDraw(True)
        
        # *test_instr_resp* updates
        waitOnFlip = False
        if test_instr_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            test_instr_resp.frameNStart = frameN  # exact frame index
            test_instr_resp.tStart = t  # local t and not account for scr refresh
            test_instr_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(test_instr_resp, 'tStartRefresh')  # time at next scr refresh
            test_instr_resp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(test_instr_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if test_instr_resp.status == STARTED and not waitOnFlip:
            theseKeys = test_instr_resp.getKeys(keyList=['space'], waitRelease=False)
            if len(theseKeys):
                theseKeys = theseKeys[0]  # at least one key was pressed
                
                # check for quit:
                if "escape" == theseKeys:
                    endExpNow = True
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in test_instructionsComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "test_instructions"-------
    for thisComponent in test_instructionsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    test_phase.addData('test_instructions_image.started', test_instructions_image.tStartRefresh)
    test_phase.addData('test_instructions_image.stopped', test_instructions_image.tStopRefresh)
    # the Routine "test_instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "warn_prac_or_crit"-------
    # update component parameters for each repeat
    warning_text.setText(test_instructions)
    warning_key_resp.keys = []
    warning_key_resp.rt = []
    # keep track of which components have finished
    warn_prac_or_critComponents = [warning_text, warning_key_resp]
    for thisComponent in warn_prac_or_critComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    warn_prac_or_critClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    continueRoutine = True
    
    # -------Run Routine "warn_prac_or_crit"-------
    while continueRoutine:
        # get current time
        t = warn_prac_or_critClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=warn_prac_or_critClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *warning_text* updates
        if warning_text.status == NOT_STARTED and frameN >= 0.0:
            # keep track of start time/frame for later
            warning_text.frameNStart = frameN  # exact frame index
            warning_text.tStart = t  # local t and not account for scr refresh
            warning_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(warning_text, 'tStartRefresh')  # time at next scr refresh
            warning_text.setAutoDraw(True)
        
        # *warning_key_resp* updates
        waitOnFlip = False
        if warning_key_resp.status == NOT_STARTED and frameN >= 0.0:
            # keep track of start time/frame for later
            warning_key_resp.frameNStart = frameN  # exact frame index
            warning_key_resp.tStart = t  # local t and not account for scr refresh
            warning_key_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(warning_key_resp, 'tStartRefresh')  # time at next scr refresh
            warning_key_resp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(warning_key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if warning_key_resp.status == STARTED and not waitOnFlip:
            theseKeys = warning_key_resp.getKeys(keyList=['space'], waitRelease=False)
            if len(theseKeys):
                theseKeys = theseKeys[0]  # at least one key was pressed
                
                # check for quit:
                if "escape" == theseKeys:
                    endExpNow = True
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in warn_prac_or_critComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "warn_prac_or_crit"-------
    for thisComponent in warn_prac_or_critComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    test_phase.addData('warning_text.started', warning_text.tStartRefresh)
    test_phase.addData('warning_text.stopped', warning_text.tStopRefresh)
    # the Routine "warn_prac_or_crit" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    test_trials = data.TrialHandler(nReps=1, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(stim_file_test),
        seed=None, name='test_trials')
    thisExp.addLoop(test_trials)  # add the loop to the experiment
    thisTest_trial = test_trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTest_trial.rgb)
    if thisTest_trial != None:
        for paramName in thisTest_trial:
            exec('{} = thisTest_trial[paramName]'.format(paramName))
    
    for thisTest_trial in test_trials:
        currentLoop = test_trials
        # abbreviate parameter names if possible (e.g. rgb = thisTest_trial.rgb)
        if thisTest_trial != None:
            for paramName in thisTest_trial:
                exec('{} = thisTest_trial[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "test_break"-------
        # update component parameters for each repeat
        if test_trials.thisN == 0:
            continueRoutine = False
            show_break = True
        elif test_trials.thisN % break_n != 0:
            continueRoutine = False
            show_break = False
        else:
            continueRoutine = True 
            show_break = True 
        draw_test_break_key_resp.keys = []
        draw_test_break_key_resp.rt = []
        # keep track of which components have finished
        test_breakComponents = [draw_test_break, draw_test_break_key_resp]
        for thisComponent in test_breakComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        test_breakClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True
        
        # -------Run Routine "test_break"-------
        while continueRoutine:
            # get current time
            t = test_breakClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=test_breakClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            if test_trials.thisN == 0:
                continueRoutine = False
                show_break = True
            elif test_trials.thisN % break_n != 0:
                continueRoutine = False
                show_break = False
            else:
                continueRoutine = True 
                show_break = True 
            
            # *draw_test_break* updates
            if draw_test_break.status == NOT_STARTED and frameN >= 0.0:
                # keep track of start time/frame for later
                draw_test_break.frameNStart = frameN  # exact frame index
                draw_test_break.tStart = t  # local t and not account for scr refresh
                draw_test_break.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(draw_test_break, 'tStartRefresh')  # time at next scr refresh
                draw_test_break.setAutoDraw(True)
            
            # *draw_test_break_key_resp* updates
            waitOnFlip = False
            if draw_test_break_key_resp.status == NOT_STARTED and frameN >= 0.0:
                # keep track of start time/frame for later
                draw_test_break_key_resp.frameNStart = frameN  # exact frame index
                draw_test_break_key_resp.tStart = t  # local t and not account for scr refresh
                draw_test_break_key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(draw_test_break_key_resp, 'tStartRefresh')  # time at next scr refresh
                draw_test_break_key_resp.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(draw_test_break_key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if draw_test_break_key_resp.status == STARTED and not waitOnFlip:
                theseKeys = draw_test_break_key_resp.getKeys(keyList=['b'], waitRelease=False)
                if len(theseKeys):
                    theseKeys = theseKeys[0]  # at least one key was pressed
                    
                    # check for quit:
                    if "escape" == theseKeys:
                        endExpNow = True
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in test_breakComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "test_break"-------
        for thisComponent in test_breakComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        test_trials.addData('draw_test_break.started', draw_test_break.tStartRefresh)
        test_trials.addData('draw_test_break.stopped', draw_test_break.tStopRefresh)
        # the Routine "test_break" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "test_delay"-------
        # update component parameters for each repeat
        if test_trials.thisN == 0:
            continueRoutine = True
        else:
            continueRoutine = show_break
        # keep track of which components have finished
        test_delayComponents = [test_delay_text]
        for thisComponent in test_delayComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        test_delayClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True
        
        # -------Run Routine "test_delay"-------
        while continueRoutine:
            # get current time
            t = test_delayClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=test_delayClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            if test_trials.thisN == 0:
                continueRoutine = True
            else:
                continueRoutine = show_break
            
            # *test_delay_text* updates
            if test_delay_text.status == NOT_STARTED and frameN >= 0.0:
                # keep track of start time/frame for later
                test_delay_text.frameNStart = frameN  # exact frame index
                test_delay_text.tStart = t  # local t and not account for scr refresh
                test_delay_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(test_delay_text, 'tStartRefresh')  # time at next scr refresh
                test_delay_text.setAutoDraw(True)
            if test_delay_text.status == STARTED:
                if frameN >= (test_delay_text.frameNStart + test_delay_frames):
                    # keep track of stop time/frame for later
                    test_delay_text.tStop = t  # not accounting for scr refresh
                    test_delay_text.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(test_delay_text, 'tStopRefresh')  # time at next scr refresh
                    test_delay_text.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in test_delayComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "test_delay"-------
        for thisComponent in test_delayComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        test_trials.addData('test_delay_text.started', test_delay_text.tStartRefresh)
        test_trials.addData('test_delay_text.stopped', test_delay_text.tStopRefresh)
        # the Routine "test_delay" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "item_memory"-------
        # update component parameters for each repeat
        item_stimuli.setText(word)
        item_key_resp.keys = []
        item_key_resp.rt = []
        # keep track of which components have finished
        item_memoryComponents = [item_scale_image, item_stimuli, item_key_resp]
        for thisComponent in item_memoryComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        item_memoryClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True
        
        # -------Run Routine "item_memory"-------
        while continueRoutine:
            # get current time
            t = item_memoryClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=item_memoryClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *item_scale_image* updates
            if item_scale_image.status == NOT_STARTED and frameN >= 0.0:
                # keep track of start time/frame for later
                item_scale_image.frameNStart = frameN  # exact frame index
                item_scale_image.tStart = t  # local t and not account for scr refresh
                item_scale_image.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(item_scale_image, 'tStartRefresh')  # time at next scr refresh
                item_scale_image.setAutoDraw(True)
            if item_scale_image.status == STARTED:
                if frameN >= (item_scale_image.frameNStart + test_maxtime_frames):
                    # keep track of stop time/frame for later
                    item_scale_image.tStop = t  # not accounting for scr refresh
                    item_scale_image.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(item_scale_image, 'tStopRefresh')  # time at next scr refresh
                    item_scale_image.setAutoDraw(False)
            
            # *item_stimuli* updates
            if item_stimuli.status == NOT_STARTED and frameN >= 0.0:
                # keep track of start time/frame for later
                item_stimuli.frameNStart = frameN  # exact frame index
                item_stimuli.tStart = t  # local t and not account for scr refresh
                item_stimuli.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(item_stimuli, 'tStartRefresh')  # time at next scr refresh
                item_stimuli.setAutoDraw(True)
            if item_stimuli.status == STARTED:
                if frameN >= (item_stimuli.frameNStart + test_maxtime_frames):
                    # keep track of stop time/frame for later
                    item_stimuli.tStop = t  # not accounting for scr refresh
                    item_stimuli.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(item_stimuli, 'tStopRefresh')  # time at next scr refresh
                    item_stimuli.setAutoDraw(False)
            
            # *item_key_resp* updates
            waitOnFlip = False
            if item_key_resp.status == NOT_STARTED and frameN >= 0.0:
                # keep track of start time/frame for later
                item_key_resp.frameNStart = frameN  # exact frame index
                item_key_resp.tStart = t  # local t and not account for scr refresh
                item_key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(item_key_resp, 'tStartRefresh')  # time at next scr refresh
                item_key_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(item_key_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(item_key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if item_key_resp.status == STARTED:
                if frameN >= (item_key_resp.frameNStart + test_maxtime_frames):
                    # keep track of stop time/frame for later
                    item_key_resp.tStop = t  # not accounting for scr refresh
                    item_key_resp.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(item_key_resp, 'tStopRefresh')  # time at next scr refresh
                    item_key_resp.status = FINISHED
            if item_key_resp.status == STARTED and not waitOnFlip:
                theseKeys = item_key_resp.getKeys(keyList=['s', 'd', 'f', 'j', 'k', 'l'], waitRelease=False)
                if len(theseKeys):
                    theseKeys = theseKeys[0]  # at least one key was pressed
                    
                    # check for quit:
                    if "escape" == theseKeys:
                        endExpNow = True
                    item_key_resp.keys = theseKeys.name  # just the last key pressed
                    item_key_resp.rt = theseKeys.rt
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in item_memoryComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "item_memory"-------
        for thisComponent in item_memoryComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        test_trials.addData('item_scale_image.started', item_scale_image.tStartRefresh)
        test_trials.addData('item_scale_image.stopped', item_scale_image.tStopRefresh)
        test_trials.addData('item_stimuli.started', item_stimuli.tStartRefresh)
        test_trials.addData('item_stimuli.stopped', item_stimuli.tStopRefresh)
        # check responses
        if item_key_resp.keys in ['', [], None]:  # No response was made
            item_key_resp.keys = None
        test_trials.addData('item_key_resp.keys',item_key_resp.keys)
        if item_key_resp.keys != None:  # we had a response
            test_trials.addData('item_key_resp.rt', item_key_resp.rt)
        test_trials.addData('item_key_resp.started', item_key_resp.tStartRefresh)
        test_trials.addData('item_key_resp.stopped', item_key_resp.tStopRefresh)
        # the Routine "item_memory" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "source_memory"-------
        # update component parameters for each repeat
        if item_key_resp.keys == 'j'or item_key_resp.keys== 'k'or item_key_resp.keys=='l':
            continueRoutine = True
        else:
            continueRoutine = False 
        item_stimuli_text.setText(word)
        source_key_resp.keys = []
        source_key_resp.rt = []
        # keep track of which components have finished
        source_memoryComponents = [source_scale_image, item_stimuli_text, source_key_resp]
        for thisComponent in source_memoryComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        source_memoryClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True
        
        # -------Run Routine "source_memory"-------
        while continueRoutine:
            # get current time
            t = source_memoryClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=source_memoryClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            if item_key_resp.keys == 'j'or item_key_resp.keys== 'k'or item_key_resp.keys=='l':
                continueRoutine = True
            else:
                continueRoutine = False 
            
            # *source_scale_image* updates
            if source_scale_image.status == NOT_STARTED and frameN >= 0.0:
                # keep track of start time/frame for later
                source_scale_image.frameNStart = frameN  # exact frame index
                source_scale_image.tStart = t  # local t and not account for scr refresh
                source_scale_image.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(source_scale_image, 'tStartRefresh')  # time at next scr refresh
                source_scale_image.setAutoDraw(True)
            if source_scale_image.status == STARTED:
                if frameN >= (source_scale_image.frameNStart + test_maxtime_frames):
                    # keep track of stop time/frame for later
                    source_scale_image.tStop = t  # not accounting for scr refresh
                    source_scale_image.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(source_scale_image, 'tStopRefresh')  # time at next scr refresh
                    source_scale_image.setAutoDraw(False)
            
            # *item_stimuli_text* updates
            if item_stimuli_text.status == NOT_STARTED and frameN >= 0.0:
                # keep track of start time/frame for later
                item_stimuli_text.frameNStart = frameN  # exact frame index
                item_stimuli_text.tStart = t  # local t and not account for scr refresh
                item_stimuli_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(item_stimuli_text, 'tStartRefresh')  # time at next scr refresh
                item_stimuli_text.setAutoDraw(True)
            if item_stimuli_text.status == STARTED:
                if frameN >= (item_stimuli_text.frameNStart + test_maxtime_frames):
                    # keep track of stop time/frame for later
                    item_stimuli_text.tStop = t  # not accounting for scr refresh
                    item_stimuli_text.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(item_stimuli_text, 'tStopRefresh')  # time at next scr refresh
                    item_stimuli_text.setAutoDraw(False)
            
            # *source_key_resp* updates
            waitOnFlip = False
            if source_key_resp.status == NOT_STARTED and frameN >= 0:
                # keep track of start time/frame for later
                source_key_resp.frameNStart = frameN  # exact frame index
                source_key_resp.tStart = t  # local t and not account for scr refresh
                source_key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(source_key_resp, 'tStartRefresh')  # time at next scr refresh
                source_key_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(source_key_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(source_key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if source_key_resp.status == STARTED:
                if frameN >= (source_key_resp.frameNStart + test_maxtime_frames):
                    # keep track of stop time/frame for later
                    source_key_resp.tStop = t  # not accounting for scr refresh
                    source_key_resp.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(source_key_resp, 'tStopRefresh')  # time at next scr refresh
                    source_key_resp.status = FINISHED
            if source_key_resp.status == STARTED and not waitOnFlip:
                theseKeys = source_key_resp.getKeys(keyList=['j', 'k', 'l'], waitRelease=False)
                if len(theseKeys):
                    theseKeys = theseKeys[0]  # at least one key was pressed
                    
                    # check for quit:
                    if "escape" == theseKeys:
                        endExpNow = True
                    source_key_resp.keys = theseKeys.name  # just the last key pressed
                    source_key_resp.rt = theseKeys.rt
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in source_memoryComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "source_memory"-------
        for thisComponent in source_memoryComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        test_trials.addData('source_scale_image.started', source_scale_image.tStartRefresh)
        test_trials.addData('source_scale_image.stopped', source_scale_image.tStopRefresh)
        test_trials.addData('item_stimuli_text.started', item_stimuli_text.tStartRefresh)
        test_trials.addData('item_stimuli_text.stopped', item_stimuli_text.tStopRefresh)
        # check responses
        if source_key_resp.keys in ['', [], None]:  # No response was made
            source_key_resp.keys = None
        test_trials.addData('source_key_resp.keys',source_key_resp.keys)
        if source_key_resp.keys != None:  # we had a response
            test_trials.addData('source_key_resp.rt', source_key_resp.rt)
        test_trials.addData('source_key_resp.started', source_key_resp.tStartRefresh)
        test_trials.addData('source_key_resp.stopped', source_key_resp.tStopRefresh)
        # the Routine "source_memory" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "test_iti"-------
        # update component parameters for each repeat
        # keep track of which components have finished
        test_itiComponents = [test_iti_text]
        for thisComponent in test_itiComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        test_itiClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True
        
        # -------Run Routine "test_iti"-------
        while continueRoutine:
            # get current time
            t = test_itiClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=test_itiClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *test_iti_text* updates
            if test_iti_text.status == NOT_STARTED and frameN >= 0.0:
                # keep track of start time/frame for later
                test_iti_text.frameNStart = frameN  # exact frame index
                test_iti_text.tStart = t  # local t and not account for scr refresh
                test_iti_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(test_iti_text, 'tStartRefresh')  # time at next scr refresh
                test_iti_text.setAutoDraw(True)
            if test_iti_text.status == STARTED:
                if frameN >= (test_iti_text.frameNStart + test_iti_frames):
                    # keep track of stop time/frame for later
                    test_iti_text.tStop = t  # not accounting for scr refresh
                    test_iti_text.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(test_iti_text, 'tStopRefresh')  # time at next scr refresh
                    test_iti_text.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in test_itiComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "test_iti"-------
        for thisComponent in test_itiComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        test_trials.addData('test_iti_text.started', test_iti_text.tStartRefresh)
        test_trials.addData('test_iti_text.stopped', test_iti_text.tStopRefresh)
        # the Routine "test_iti" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "code_test_resp"-------
        # update component parameters for each repeat
        # Extract the appropriate response from the correct object
        item_resp = item_scale[item_key_resp.keys]
        item_rt   = item_key_resp.rt
        
        # Update response if necessary
        if item_resp == None or item_resp == '':
            item_resp = 'na'
            item_rt = -99
            old_resp = -99
            item_acc = -99
            sm_acc = -99
            bad_trial = 1
        else:
            bad_trial = 0
            # Code item memory accuracy
            if item_resp == 4 or item_resp == 5 or item_resp == 6 :
                
                # Handle item response
                old_resp = 1
                if old_new == 'old':
                    item_acc = 1
                else:
                    item_acc = 0
            else: # Must be a new response
                old_resp = 0
                if old_new == 'new':
                    item_acc = 1
                else:
                    item_acc = 0
        
        #code source memory response and Rts
        # old = 4,5,6
        if item_resp == 4 or item_resp == 5 or item_resp == 6 :
            sm_resp = source_key_resp.keys
            sm_resp_coded = source_scale[sm_resp]
            sm_rt = source_key_resp.rt
            bad_trial = 0
            if sm_resp_coded == 'shoebox' and study_judgment == 'shoebox':
                sm_acc = 1
            elif sm_resp_coded == 'manmade' and study_judgment == 'manmade':
                sm_acc = 1
            elif sm_resp_coded == 'shoebox' and study_judgment == 'manmade':
                sm_acc = 0
            elif sm_resp_coded == 'manmade' and study_judgment == 'shoebox':
                sm_acc = 0
            elif sm_resp_coded == 'dk':
                sm_acc = 0
            else:
                sm_acc = -99
        else:
            sm_resp = -99
            sm_rt  = -99
            sm_acc = -99
        
        # Store in trials object
        test_trials.addData('item_resp',item_resp)
        test_trials.addData('item_rt',item_rt)
        test_trials.addData('item_acc',item_acc)
        test_trials.addData('old_new_resp',old_resp)
        
        test_trials.addData('sm_resp',sm_resp)
        test_trials.addData('sm_rt',sm_rt)
        
        
        test_trials.addData('sm_acc',sm_acc)
        
        test_trials.addData('trial_type',bad_trial)
        # keep track of which components have finished
        code_test_respComponents = []
        for thisComponent in code_test_respComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        code_test_respClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True
        
        # -------Run Routine "code_test_resp"-------
        while continueRoutine:
            # get current time
            t = code_test_respClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=code_test_respClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in code_test_respComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "code_test_resp"-------
        for thisComponent in code_test_respComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # the Routine "code_test_resp" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1 repeats of 'test_trials'
    
# completed 1 repeats of 'test_phase'


# ------Prepare to start Routine "test_complete"-------
routineTimer.add(5.000000)
# update component parameters for each repeat
# keep track of which components have finished
test_completeComponents = [test_complete_text]
for thisComponent in test_completeComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
test_completeClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1
continueRoutine = True

# -------Run Routine "test_complete"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = test_completeClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=test_completeClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *test_complete_text* updates
    if test_complete_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        test_complete_text.frameNStart = frameN  # exact frame index
        test_complete_text.tStart = t  # local t and not account for scr refresh
        test_complete_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(test_complete_text, 'tStartRefresh')  # time at next scr refresh
        test_complete_text.setAutoDraw(True)
    if test_complete_text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > test_complete_text.tStartRefresh + 5-frameTolerance:
            # keep track of stop time/frame for later
            test_complete_text.tStop = t  # not accounting for scr refresh
            test_complete_text.frameNStop = frameN  # exact frame index
            win.timeOnFlip(test_complete_text, 'tStopRefresh')  # time at next scr refresh
            test_complete_text.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in test_completeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "test_complete"-------
for thisComponent in test_completeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('test_complete_text.started', test_complete_text.tStartRefresh)
thisExp.addData('test_complete_text.stopped', test_complete_text.tStopRefresh)

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
