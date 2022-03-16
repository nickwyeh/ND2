#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v3.2.2),
    on July 31, 2020, at 14:11
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

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
psychopyVersion = '3.2.2'
expName = 'study_test_proc'  # from the Builder filename that created this script
expInfo = {'id': '', 'stim_set': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'archive/%s_%s_%s' % (expInfo['id'], 'archive', expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='X:\\EXPT\\nd002\\exp1\\task\\study_test_proc.py',
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
    size=[2048, 1152], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=True, allowStencil=False,
    monitor='testMonitor', color=[-0.6,-0.6,-0.6], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='degFlat')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "setup_routine"
setup_routineClock = core.Clock()
# Update expInfo ID
expInfo['id'] = expInfo['id']

# Save directory
save_dir = os.path.join('data', 'sub-{}'.format(expInfo['id']))
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)
    
# Initialize color lists
cueColor = [-1.0,-1.0,-1.0] # Default to black (cue)
wordColor = [-1.0,-1.0,-1.0] # Default to black (word)

# Get the stimulus directory
expInfo['stim_set'] = 'set' + str(expInfo['stim_set'])
stim_dir = os.path.join('stim_files', expInfo['stim_set'])
if not os.path.isdir(stim_dir):
    raise Exception('Stim directory does not exist!!!!')


## USEFUL FUNCTIONS ##
# Define function for determining study condition
def get_study_cond(a,b):
    '''
    this function takes as input the study condition (a)
    and the study judgment (b) and computes a number for the condition.
    Four conditions:
    Condition 1 = Shoebox - Informed (red cue, black word)
    Condition 2 = Manmade - Informed (blue cue, black word)
    Condition 3 = Shoebox - Uninformed (black cue, red word)
    Condition 4 = Manmade - Uninformed (black cue, blue word)
    '''
    if a == 'informed' and b == 'shoebox':
        cond = 1
    elif a == 'informed' and b == 'manmade':
        cond = 2
    elif a == 'uninformed' and b == 'shoebox':
        cond = 3
    elif a == 'uninformed' and b == 'manmade':
        cond = 4

    return(cond)

# Determine study response hand accuracy
def study_resp_acc(resp,task,correct):
    '''
    This determines in the study hand is correct or incorrect. 
    Shoebox is left hand, manmade is right hand.
    This also returns response accuracy.
    Inputs are:
        resp - subjects response from keypress
        task - manmade or shoebox
        correct - correct response (either y or n)
    A tuple is returned with 3 values:
        coded_resp = either y, n, wh (wrong hand), or nr (no response)
        hand_acc = 1 or 0 (1 = correct, 0 = incorrect)
        resp_acc = 1 or 0 (1 = correct, 0 = incorrect resp)
    The resp_acc is also coded 0 if there is an incorrect hand button press.
    '''

    # Initialize outputs
    coded_resp = ''
    hand_acc = []
    resp_acc = []

    # Spot check correct input
    if correct not in ('y','n'):
        raise ValueError('the correct input must be y or n.')

    # Define yes/no responses
    yesResp = ('f','1','j','3')
    noResp = ('d','2','k','4')

    # Define correct response and cor_hand
    if task == 'shoebox':
        cor_hand = ('d','f','1','2')
    else:
        cor_hand = ('j','k','3','4')

    # Get three outputs
    if not resp: # Empty response
        coded_resp = 'nr'
        hand_acc = 0
        resp_acc = 0
    elif resp in cor_hand: # Correct hand response
        hand_acc = 1
        if correct == 'y':
            if resp in yesResp: # Correct yes response
                resp_acc = 1
                coded_resp = 'y'
            else:
                resp_acc = 0
                coded_resp = 'n'
        else:
            if resp in noResp: # Correct no response
                resp_acc = 1
                coded_resp = 'n'
            else:
                resp_acc = 0
                coded_resp = 'y'
    else: # Incorrect hand response
        coded_resp = 'wh'
        hand_acc = 0
        resp_acc = 0

    # Return values
    return(coded_resp,hand_acc,resp_acc)




# Initialize components for Routine "study_instructions"
study_instructionsClock = core.Clock()
study_instructions_image = visual.ImageStim(
    win=win,
    name='study_instructions_image', 
    image='images\\study_summary_instructions.png', mask=None,
    ori=0, pos=(0, 0), size=(40.0,22.5),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
study_instructions_wait = keyboard.Keyboard()

# Initialize components for Routine "study_break"
study_breakClock = core.Clock()
# Define number of trials between rests
rest_n = 64

study_break_text = visual.TextStim(win=win, name='study_break_text',
    text='Take a break\n\nPress the space bar when ready to continue',
    font='Helvetica',
    pos=(0, 0), height=1.5, wrapWidth=50, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
study_break_ready = keyboard.Keyboard()

# Initialize components for Routine "study_delay"
study_delayClock = core.Clock()
study_delay_text = visual.TextStim(win=win, name='study_delay_text',
    text='+',
    font='Helvetica',
    pos=(0, 0), height=1.5, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "cue_trial"
cue_trialClock = core.Clock()
# Main Timing variables
get_ready_time = .35
cue_time = .5
cue_interval_time = 1.25

# Do some math on timings
cue_start = get_ready_time
cue_interval_start = cue_time + get_ready_time


# Define possible jitters
jitters = [.5,.75,1.0,1.25,1.5]

get_ready_text = visual.TextStim(win=win, name='get_ready_text',
    text='!!',
    font='Helvetica',
    pos=(0, 0), height=1.5, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
cue_circle = visual.Polygon(
    win=win, name='cue_circle',
    edges=180, size=(1.5,1.5),
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=1.0, lineColorSpace='rgb',
    fillColor=1.0, fillColorSpace='rgb',
    opacity=1, depth=-2.0, interpolate=True)
cue_interval_fix = visual.TextStim(win=win, name='cue_interval_fix',
    text='+',
    font='Helvetica',
    pos=(0, 0), height=1.5, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-3.0);

# Initialize components for Routine "study_trial"
study_trialClock = core.Clock()
study_text = visual.TextStim(win=win, name='study_text',
    text='default text',
    font='Helvetica',
    pos=(0, 0), height=1.5, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
study_interval_fix = visual.TextStim(win=win, name='study_interval_fix',
    text='+',
    font='Helvetica',
    pos=(0, 0), height=1.5, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
jitter_text = visual.TextStim(win=win, name='jitter_text',
    text='+',
    font='Helvetica',
    pos=(0, 0), height=1.5, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);
study_resp = keyboard.Keyboard()

# Initialize components for Routine "prac1_pause"
prac1_pauseClock = core.Clock()
pause_fixation = visual.TextStim(win=win, name='pause_fixation',
    text='+',
    font='Helvetica',
    pos=(0, 0), height=1.5, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "study_save_trials"
study_save_trialsClock = core.Clock()

# Initialize components for Routine "study_delay"
study_delayClock = core.Clock()
study_delay_text = visual.TextStim(win=win, name='study_delay_text',
    text='+',
    font='Helvetica',
    pos=(0, 0), height=1.5, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "phase_complete"
phase_completeClock = core.Clock()
phase_completed_text = visual.TextStim(win=win, name='phase_completed_text',
    text='Phase completed',
    font='Helvetica',
    pos=(0, 0), height=1.5, wrapWidth=50, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "long_pause"
long_pauseClock = core.Clock()
long_pause_text = visual.TextStim(win=win, name='long_pause_text',
    text='Take a break and wait for further instructions from the experimenter.',
    font='Helvetica',
    pos=(0, 0), height=1.5, wrapWidth=50, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
long_pause_key = keyboard.Keyboard()

# Initialize components for Routine "test_instructions"
test_instructionsClock = core.Clock()
test_instructions_image = visual.ImageStim(
    win=win,
    name='test_instructions_image', 
    image='images\\test_summary_instructions.png', mask=None,
    ori=0, pos=(0, 0), size=(40.0,22.5),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
test_instructions_wait = keyboard.Keyboard()

# Initialize components for Routine "test_break"
test_breakClock = core.Clock()
# Define number of trials between rests
rest_n = 64
test_break_text = visual.TextStim(win=win, name='test_break_text',
    text='Take a break\n\nPress the space bar when ready to continue',
    font='Helvetica',
    pos=(0, 0), height=1.5, wrapWidth=50, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
test_break_ready = keyboard.Keyboard()

# Initialize components for Routine "test_delay"
test_delayClock = core.Clock()
test_delay_text = visual.TextStim(win=win, name='test_delay_text',
    text='+',
    font='Helvetica',
    pos=(0, 0), height=1.5, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "test_trial"
test_trialClock = core.Clock()
# Labels for Slider
so='\n   6\r\nSure\r\n Old'
mo='\n    5\r\nMaybe\r\n  Old'
go='\n    4\r\nGuess\r\n  Old'
gn='\n    3\r\nGuess\r\n New'
mn='\n    2\r\nMaybe\r\n New'
sn='\n   1\r\nSure\r\nNew'
test_word = visual.TextStim(win=win, name='test_word',
    text='default text',
    font='Helvetica',
    pos=(0, 0), height=1.5, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
test_resp = visual.RatingScale(win=win, name='test_resp', marker='circle',
markerColor=[-0.6,-0.6,-0.6],
stretch=1.6,
pos=[0.0,-0.2],
low=1,
high=6,
tickMarks=[1,2,3,4,5,6],
labels=[sn,mn,gn,go,mo,so],
disappear=False,
singleClick=True,
textSize=.8,
textFont='Helvetica',
showAccept=False,
respKeys=['s','d','f','j','k','l'],
noMouse=True)

# Initialize components for Routine "iti"
itiClock = core.Clock()
iti_text = visual.TextStim(win=win, name='iti_text',
    text='+',
    font='Helvetica',
    pos=(0, 0), height=1.5, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "test_save_trials"
test_save_trialsClock = core.Clock()

# Initialize components for Routine "study_delay"
study_delayClock = core.Clock()
study_delay_text = visual.TextStim(win=win, name='study_delay_text',
    text='+',
    font='Helvetica',
    pos=(0, 0), height=1.5, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "phase_complete"
phase_completeClock = core.Clock()
phase_completed_text = visual.TextStim(win=win, name='phase_completed_text',
    text='Phase completed',
    font='Helvetica',
    pos=(0, 0), height=1.5, wrapWidth=50, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "setup_routine"-------
# update component parameters for each repeat
# keep track of which components have finished
setup_routineComponents = []
for thisComponent in setup_routineComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
setup_routineClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1
continueRoutine = True

# -------Run Routine "setup_routine"-------
while continueRoutine:
    # get current time
    t = setup_routineClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=setup_routineClock)
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
    for thisComponent in setup_routineComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "setup_routine"-------
for thisComponent in setup_routineComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "setup_routine" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
study_phases = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('study_phases.csv'),
    seed=None, name='study_phases')
thisExp.addLoop(study_phases)  # add the loop to the experiment
thisStudy_phase = study_phases.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisStudy_phase.rgb)
if thisStudy_phase != None:
    for paramName in thisStudy_phase:
        exec('{} = thisStudy_phase[paramName]'.format(paramName))

for thisStudy_phase in study_phases:
    currentLoop = study_phases
    # abbreviate parameter names if possible (e.g. rgb = thisStudy_phase.rgb)
    if thisStudy_phase != None:
        for paramName in thisStudy_phase:
            exec('{} = thisStudy_phase[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "study_instructions"-------
    # update component parameters for each repeat
    stim_file = os.path.join(stim_dir, expInfo['stim_set'] + '_' + study_phase + '.csv')
    
    study_instructions_wait.keys = []
    study_instructions_wait.rt = []
    # keep track of which components have finished
    study_instructionsComponents = [study_instructions_image, study_instructions_wait]
    for thisComponent in study_instructionsComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    study_instructionsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    continueRoutine = True
    
    # -------Run Routine "study_instructions"-------
    while continueRoutine:
        # get current time
        t = study_instructionsClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=study_instructionsClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *study_instructions_image* updates
        if study_instructions_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            study_instructions_image.frameNStart = frameN  # exact frame index
            study_instructions_image.tStart = t  # local t and not account for scr refresh
            study_instructions_image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(study_instructions_image, 'tStartRefresh')  # time at next scr refresh
            study_instructions_image.setAutoDraw(True)
        
        # *study_instructions_wait* updates
        if study_instructions_wait.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            study_instructions_wait.frameNStart = frameN  # exact frame index
            study_instructions_wait.tStart = t  # local t and not account for scr refresh
            study_instructions_wait.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(study_instructions_wait, 'tStartRefresh')  # time at next scr refresh
            study_instructions_wait.status = STARTED
            # keyboard checking is just starting
            study_instructions_wait.clearEvents(eventType='keyboard')
        if study_instructions_wait.status == STARTED:
            theseKeys = study_instructions_wait.getKeys(keyList=['space', 'lctrl', 'rctrl'], waitRelease=False)
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
        for thisComponent in study_instructionsComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "study_instructions"-------
    for thisComponent in study_instructionsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    study_phases.addData('study_instructions_image.started', study_instructions_image.tStartRefresh)
    study_phases.addData('study_instructions_image.stopped', study_instructions_image.tStopRefresh)
    # the Routine "study_instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    study_trials = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(stim_file),
        seed=None, name='study_trials')
    thisExp.addLoop(study_trials)  # add the loop to the experiment
    thisStudy_trial = study_trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisStudy_trial.rgb)
    if thisStudy_trial != None:
        for paramName in thisStudy_trial:
            exec('{} = thisStudy_trial[paramName]'.format(paramName))
    
    for thisStudy_trial in study_trials:
        currentLoop = study_trials
        # abbreviate parameter names if possible (e.g. rgb = thisStudy_trial.rgb)
        if thisStudy_trial != None:
            for paramName in thisStudy_trial:
                exec('{} = thisStudy_trial[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "study_break"-------
        # update component parameters for each repeat
        if study_trials.thisN == 0:
            continueRoutine = False
        elif study_trials.thisN % rest_n != 0:
            continueRoutine = False
        else:
            continueRoutine = True 
            
        # Control delay
        draw_delay = continueRoutine
        study_break_ready.keys = []
        study_break_ready.rt = []
        # keep track of which components have finished
        study_breakComponents = [study_break_text, study_break_ready]
        for thisComponent in study_breakComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        study_breakClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True
        
        # -------Run Routine "study_break"-------
        while continueRoutine:
            # get current time
            t = study_breakClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=study_breakClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *study_break_text* updates
            if study_break_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                study_break_text.frameNStart = frameN  # exact frame index
                study_break_text.tStart = t  # local t and not account for scr refresh
                study_break_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(study_break_text, 'tStartRefresh')  # time at next scr refresh
                study_break_text.setAutoDraw(True)
            
            # *study_break_ready* updates
            if study_break_ready.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                study_break_ready.frameNStart = frameN  # exact frame index
                study_break_ready.tStart = t  # local t and not account for scr refresh
                study_break_ready.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(study_break_ready, 'tStartRefresh')  # time at next scr refresh
                study_break_ready.status = STARTED
                # keyboard checking is just starting
                study_break_ready.clearEvents(eventType='keyboard')
            if study_break_ready.status == STARTED:
                theseKeys = study_break_ready.getKeys(keyList=['space', 'lctrl', 'rctrl'], waitRelease=False)
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
            for thisComponent in study_breakComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "study_break"-------
        for thisComponent in study_breakComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        study_trials.addData('study_break_text.started', study_break_text.tStartRefresh)
        study_trials.addData('study_break_text.stopped', study_break_text.tStopRefresh)
        # the Routine "study_break" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "study_delay"-------
        routineTimer.add(5.000000)
        # update component parameters for each repeat
        if study_trials.thisN == 0:
            continueRoutine = True
        else:
            continueRoutine = draw_delay
        # keep track of which components have finished
        study_delayComponents = [study_delay_text]
        for thisComponent in study_delayComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        study_delayClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True
        
        # -------Run Routine "study_delay"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = study_delayClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=study_delayClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *study_delay_text* updates
            if study_delay_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                study_delay_text.frameNStart = frameN  # exact frame index
                study_delay_text.tStart = t  # local t and not account for scr refresh
                study_delay_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(study_delay_text, 'tStartRefresh')  # time at next scr refresh
                study_delay_text.setAutoDraw(True)
            if study_delay_text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > study_delay_text.tStartRefresh + 5.0-frameTolerance:
                    # keep track of stop time/frame for later
                    study_delay_text.tStop = t  # not accounting for scr refresh
                    study_delay_text.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(study_delay_text, 'tStopRefresh')  # time at next scr refresh
                    study_delay_text.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in study_delayComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "study_delay"-------
        for thisComponent in study_delayComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        study_trials.addData('study_delay_text.started', study_delay_text.tStartRefresh)
        study_trials.addData('study_delay_text.stopped', study_delay_text.tStopRefresh)
        
        # ------Prepare to start Routine "cue_trial"-------
        # update component parameters for each repeat
        # Define condition
        cond = get_study_cond(study_condition, study_judgment)
        
        # Select condition
        if cond == 1:
            cueColor = [1.0,-1.0,-1.0]  # Cue to Red
            wordColor = [1.0,1.0,1.0] # Default to white (word)
        elif cond == 2:
            cueColor = [-1.0,1.0,1.0]  # Cue to Blue
            wordColor = [1.0,1.0,1.0] # Default to white (word)
        elif cond == 3:
            cueColor = [1.0,1.0,1.0]  # white cue
            wordColor = [1.0,-1.0,-1.0] # Word to Red
        elif cond == 4:
            cueColor = [1.0,1.0,1.0]  # white cue
            wordColor = [-1.0,1.0,1.0] # Word to Blue
        
        # Determine word time
        if study_phase == 'prac1_study':
            word_time = 60.0
            word_interval_time = 0.0
            resp_time = 60.0
            jitter = 0.0
        else:
            word_time = .5
            word_interval_time = 1.5
            shuffle(jitters)
            jitter = jitters[0]
            resp_time = jitter + word_time + word_interval_time
        
        # Do some math on timing
        word_interval_start = word_time
        jitter_start = word_time + word_interval_time
        cue_circle.setFillColor(cueColor)
        cue_circle.setLineColor(cueColor)
        # keep track of which components have finished
        cue_trialComponents = [get_ready_text, cue_circle, cue_interval_fix]
        for thisComponent in cue_trialComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        cue_trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True
        
        # -------Run Routine "cue_trial"-------
        while continueRoutine:
            # get current time
            t = cue_trialClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=cue_trialClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *get_ready_text* updates
            if get_ready_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                get_ready_text.frameNStart = frameN  # exact frame index
                get_ready_text.tStart = t  # local t and not account for scr refresh
                get_ready_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(get_ready_text, 'tStartRefresh')  # time at next scr refresh
                get_ready_text.setAutoDraw(True)
            if get_ready_text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > get_ready_text.tStartRefresh + get_ready_time-frameTolerance:
                    # keep track of stop time/frame for later
                    get_ready_text.tStop = t  # not accounting for scr refresh
                    get_ready_text.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(get_ready_text, 'tStopRefresh')  # time at next scr refresh
                    get_ready_text.setAutoDraw(False)
            
            # *cue_circle* updates
            if cue_circle.status == NOT_STARTED and tThisFlip >= cue_start-frameTolerance:
                # keep track of start time/frame for later
                cue_circle.frameNStart = frameN  # exact frame index
                cue_circle.tStart = t  # local t and not account for scr refresh
                cue_circle.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(cue_circle, 'tStartRefresh')  # time at next scr refresh
                cue_circle.setAutoDraw(True)
            if cue_circle.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > cue_circle.tStartRefresh + cue_time-frameTolerance:
                    # keep track of stop time/frame for later
                    cue_circle.tStop = t  # not accounting for scr refresh
                    cue_circle.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(cue_circle, 'tStopRefresh')  # time at next scr refresh
                    cue_circle.setAutoDraw(False)
            
            # *cue_interval_fix* updates
            if cue_interval_fix.status == NOT_STARTED and tThisFlip >= cue_interval_start-frameTolerance:
                # keep track of start time/frame for later
                cue_interval_fix.frameNStart = frameN  # exact frame index
                cue_interval_fix.tStart = t  # local t and not account for scr refresh
                cue_interval_fix.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(cue_interval_fix, 'tStartRefresh')  # time at next scr refresh
                cue_interval_fix.setAutoDraw(True)
            if cue_interval_fix.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > cue_interval_fix.tStartRefresh + cue_interval_time-frameTolerance:
                    # keep track of stop time/frame for later
                    cue_interval_fix.tStop = t  # not accounting for scr refresh
                    cue_interval_fix.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(cue_interval_fix, 'tStopRefresh')  # time at next scr refresh
                    cue_interval_fix.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in cue_trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "cue_trial"-------
        for thisComponent in cue_trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        study_trials.addData('get_ready_text.started', get_ready_text.tStartRefresh)
        study_trials.addData('get_ready_text.stopped', get_ready_text.tStopRefresh)
        study_trials.addData('cue_circle.started', cue_circle.tStartRefresh)
        study_trials.addData('cue_circle.stopped', cue_circle.tStopRefresh)
        study_trials.addData('cue_interval_fix.started', cue_interval_fix.tStartRefresh)
        study_trials.addData('cue_interval_fix.stopped', cue_interval_fix.tStopRefresh)
        # the Routine "cue_trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "study_trial"-------
        # update component parameters for each repeat
        study_text.setColor(wordColor, colorSpace='rgb')
        study_text.setText(word)
        study_resp.keys = []
        study_resp.rt = []
        # keep track of which components have finished
        study_trialComponents = [study_text, study_interval_fix, jitter_text, study_resp]
        for thisComponent in study_trialComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        study_trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True
        
        # -------Run Routine "study_trial"-------
        while continueRoutine:
            # get current time
            t = study_trialClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=study_trialClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *study_text* updates
            if study_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                study_text.frameNStart = frameN  # exact frame index
                study_text.tStart = t  # local t and not account for scr refresh
                study_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(study_text, 'tStartRefresh')  # time at next scr refresh
                study_text.setAutoDraw(True)
            if study_text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > study_text.tStartRefresh + word_time-frameTolerance:
                    # keep track of stop time/frame for later
                    study_text.tStop = t  # not accounting for scr refresh
                    study_text.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(study_text, 'tStopRefresh')  # time at next scr refresh
                    study_text.setAutoDraw(False)
            
            # *study_interval_fix* updates
            if study_interval_fix.status == NOT_STARTED and tThisFlip >= word_interval_start-frameTolerance:
                # keep track of start time/frame for later
                study_interval_fix.frameNStart = frameN  # exact frame index
                study_interval_fix.tStart = t  # local t and not account for scr refresh
                study_interval_fix.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(study_interval_fix, 'tStartRefresh')  # time at next scr refresh
                study_interval_fix.setAutoDraw(True)
            if study_interval_fix.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > study_interval_fix.tStartRefresh + word_interval_time-frameTolerance:
                    # keep track of stop time/frame for later
                    study_interval_fix.tStop = t  # not accounting for scr refresh
                    study_interval_fix.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(study_interval_fix, 'tStopRefresh')  # time at next scr refresh
                    study_interval_fix.setAutoDraw(False)
            
            # *jitter_text* updates
            if jitter_text.status == NOT_STARTED and tThisFlip >= jitter_start-frameTolerance:
                # keep track of start time/frame for later
                jitter_text.frameNStart = frameN  # exact frame index
                jitter_text.tStart = t  # local t and not account for scr refresh
                jitter_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(jitter_text, 'tStartRefresh')  # time at next scr refresh
                jitter_text.setAutoDraw(True)
            if jitter_text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > jitter_text.tStartRefresh + jitter-frameTolerance:
                    # keep track of stop time/frame for later
                    jitter_text.tStop = t  # not accounting for scr refresh
                    jitter_text.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(jitter_text, 'tStopRefresh')  # time at next scr refresh
                    jitter_text.setAutoDraw(False)
            
            # *study_resp* updates
            waitOnFlip = False
            if study_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                study_resp.frameNStart = frameN  # exact frame index
                study_resp.tStart = t  # local t and not account for scr refresh
                study_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(study_resp, 'tStartRefresh')  # time at next scr refresh
                study_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(study_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(study_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if study_resp.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > study_resp.tStartRefresh + resp_time-frameTolerance:
                    # keep track of stop time/frame for later
                    study_resp.tStop = t  # not accounting for scr refresh
                    study_resp.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(study_resp, 'tStopRefresh')  # time at next scr refresh
                    study_resp.status = FINISHED
            if study_resp.status == STARTED and not waitOnFlip:
                theseKeys = study_resp.getKeys(keyList=['f', 'j', 'd', 'k'], waitRelease=False)
                if len(theseKeys):
                    theseKeys = theseKeys[0]  # at least one key was pressed
                    
                    # check for quit:
                    if "escape" == theseKeys:
                        endExpNow = True
                    study_resp.keys = theseKeys.name  # just the last key pressed
                    study_resp.rt = theseKeys.rt
            if study_phase == 'prac1_study':
                if study_resp.keys in ['', [], None]:
                    continueRoutine = True
                else:
                    continueRoutine = False 
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in study_trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "study_trial"-------
        for thisComponent in study_trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        study_trials.addData('study_text.started', study_text.tStartRefresh)
        study_trials.addData('study_text.stopped', study_text.tStopRefresh)
        study_trials.addData('study_interval_fix.started', study_interval_fix.tStartRefresh)
        study_trials.addData('study_interval_fix.stopped', study_interval_fix.tStopRefresh)
        study_trials.addData('jitter_text.started', jitter_text.tStartRefresh)
        study_trials.addData('jitter_text.stopped', jitter_text.tStopRefresh)
        # check responses
        if study_resp.keys in ['', [], None]:  # No response was made
            study_resp.keys = None
        study_trials.addData('study_resp.keys',study_resp.keys)
        if study_resp.keys != None:  # we had a response
            study_trials.addData('study_resp.rt', study_resp.rt)
        study_trials.addData('study_resp.started', study_resp.tStartRefresh)
        study_trials.addData('study_resp.stopped', study_resp.tStopRefresh)
        # the Routine "study_trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "prac1_pause"-------
        routineTimer.add(1.000000)
        # update component parameters for each repeat
        if study_phase == 'prac1_study':
            continueRoutine = True
        else:
            continueRoutine = False
        
        # keep track of which components have finished
        prac1_pauseComponents = [pause_fixation]
        for thisComponent in prac1_pauseComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        prac1_pauseClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True
        
        # -------Run Routine "prac1_pause"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = prac1_pauseClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=prac1_pauseClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *pause_fixation* updates
            if pause_fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                pause_fixation.frameNStart = frameN  # exact frame index
                pause_fixation.tStart = t  # local t and not account for scr refresh
                pause_fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(pause_fixation, 'tStartRefresh')  # time at next scr refresh
                pause_fixation.setAutoDraw(True)
            if pause_fixation.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > pause_fixation.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    pause_fixation.tStop = t  # not accounting for scr refresh
                    pause_fixation.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(pause_fixation, 'tStopRefresh')  # time at next scr refresh
                    pause_fixation.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in prac1_pauseComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "prac1_pause"-------
        for thisComponent in prac1_pauseComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        study_trials.addData('pause_fixation.started', pause_fixation.tStartRefresh)
        study_trials.addData('pause_fixation.stopped', pause_fixation.tStopRefresh)
        thisExp.nextEntry()
        
    # completed 1 repeats of 'study_trials'
    
    # get names of stimulus parameters
    if study_trials.trialList in ([], [None], None):
        params = []
    else:
        params = study_trials.trialList[0].keys()
    # save data for this loop
    study_trials.saveAsExcel(filename + '.xlsx', sheetName='study_trials',
        stimOut=params,
        dataOut=['n','all_mean','all_std', 'all_raw'])
    
    # ------Prepare to start Routine "study_save_trials"-------
    # update component parameters for each repeat
    # Update the task text for saving
    if study_phase == 'prac1_study':
        task='pracstudy1'
    elif study_phase == 'prac2_study':
        task='pracstudy2'
    else:
        task='study'
    
    # Make the save file name (This should have accurate id as it is reading from it)
    suffix = 'sub-{}_task-{}_beh'.format(expInfo['id'], task)
    save_file = os.path.join(save_dir, suffix)
    
    # Save it many different ways
    study_trials.saveAsWideText(save_file + '.tsv')
    study_trials.saveAsWideText(save_file + '.csv')
    study_trials.saveAsPickle(save_file)
    
    # keep track of which components have finished
    study_save_trialsComponents = []
    for thisComponent in study_save_trialsComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    study_save_trialsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    continueRoutine = True
    
    # -------Run Routine "study_save_trials"-------
    while continueRoutine:
        # get current time
        t = study_save_trialsClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=study_save_trialsClock)
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
        for thisComponent in study_save_trialsComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "study_save_trials"-------
    for thisComponent in study_save_trialsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "study_save_trials" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "study_delay"-------
    routineTimer.add(5.000000)
    # update component parameters for each repeat
    if study_trials.thisN == 0:
        continueRoutine = True
    else:
        continueRoutine = draw_delay
    # keep track of which components have finished
    study_delayComponents = [study_delay_text]
    for thisComponent in study_delayComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    study_delayClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    continueRoutine = True
    
    # -------Run Routine "study_delay"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = study_delayClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=study_delayClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *study_delay_text* updates
        if study_delay_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            study_delay_text.frameNStart = frameN  # exact frame index
            study_delay_text.tStart = t  # local t and not account for scr refresh
            study_delay_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(study_delay_text, 'tStartRefresh')  # time at next scr refresh
            study_delay_text.setAutoDraw(True)
        if study_delay_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > study_delay_text.tStartRefresh + 5.0-frameTolerance:
                # keep track of stop time/frame for later
                study_delay_text.tStop = t  # not accounting for scr refresh
                study_delay_text.frameNStop = frameN  # exact frame index
                win.timeOnFlip(study_delay_text, 'tStopRefresh')  # time at next scr refresh
                study_delay_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in study_delayComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "study_delay"-------
    for thisComponent in study_delayComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    study_phases.addData('study_delay_text.started', study_delay_text.tStartRefresh)
    study_phases.addData('study_delay_text.stopped', study_delay_text.tStopRefresh)
    
    # ------Prepare to start Routine "phase_complete"-------
    routineTimer.add(2.000000)
    # update component parameters for each repeat
    # keep track of which components have finished
    phase_completeComponents = [phase_completed_text]
    for thisComponent in phase_completeComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    phase_completeClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    continueRoutine = True
    
    # -------Run Routine "phase_complete"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = phase_completeClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=phase_completeClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *phase_completed_text* updates
        if phase_completed_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            phase_completed_text.frameNStart = frameN  # exact frame index
            phase_completed_text.tStart = t  # local t and not account for scr refresh
            phase_completed_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(phase_completed_text, 'tStartRefresh')  # time at next scr refresh
            phase_completed_text.setAutoDraw(True)
        if phase_completed_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > phase_completed_text.tStartRefresh + 2.0-frameTolerance:
                # keep track of stop time/frame for later
                phase_completed_text.tStop = t  # not accounting for scr refresh
                phase_completed_text.frameNStop = frameN  # exact frame index
                win.timeOnFlip(phase_completed_text, 'tStopRefresh')  # time at next scr refresh
                phase_completed_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in phase_completeComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "phase_complete"-------
    for thisComponent in phase_completeComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    study_phases.addData('phase_completed_text.started', phase_completed_text.tStartRefresh)
    study_phases.addData('phase_completed_text.stopped', phase_completed_text.tStopRefresh)
# completed 1 repeats of 'study_phases'


# ------Prepare to start Routine "long_pause"-------
# update component parameters for each repeat
long_pause_key.keys = []
long_pause_key.rt = []
# keep track of which components have finished
long_pauseComponents = [long_pause_text, long_pause_key]
for thisComponent in long_pauseComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
long_pauseClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1
continueRoutine = True

# -------Run Routine "long_pause"-------
while continueRoutine:
    # get current time
    t = long_pauseClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=long_pauseClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *long_pause_text* updates
    if long_pause_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        long_pause_text.frameNStart = frameN  # exact frame index
        long_pause_text.tStart = t  # local t and not account for scr refresh
        long_pause_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(long_pause_text, 'tStartRefresh')  # time at next scr refresh
        long_pause_text.setAutoDraw(True)
    
    # *long_pause_key* updates
    waitOnFlip = False
    if long_pause_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        long_pause_key.frameNStart = frameN  # exact frame index
        long_pause_key.tStart = t  # local t and not account for scr refresh
        long_pause_key.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(long_pause_key, 'tStartRefresh')  # time at next scr refresh
        long_pause_key.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(long_pause_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if long_pause_key.status == STARTED and not waitOnFlip:
        theseKeys = long_pause_key.getKeys(keyList=['space'], waitRelease=False)
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
    for thisComponent in long_pauseComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "long_pause"-------
for thisComponent in long_pauseComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('long_pause_text.started', long_pause_text.tStartRefresh)
thisExp.addData('long_pause_text.stopped', long_pause_text.tStopRefresh)
# the Routine "long_pause" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
test_phases = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('test_phases.csv'),
    seed=None, name='test_phases')
thisExp.addLoop(test_phases)  # add the loop to the experiment
thisTest_phase = test_phases.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTest_phase.rgb)
if thisTest_phase != None:
    for paramName in thisTest_phase:
        exec('{} = thisTest_phase[paramName]'.format(paramName))

for thisTest_phase in test_phases:
    currentLoop = test_phases
    # abbreviate parameter names if possible (e.g. rgb = thisTest_phase.rgb)
    if thisTest_phase != None:
        for paramName in thisTest_phase:
            exec('{} = thisTest_phase[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "test_instructions"-------
    # update component parameters for each repeat
    stim_file = os.path.join(stim_dir, expInfo['stim_set'] + '_' + test_phase + '.csv')
    
    test_instructions_wait.keys = []
    test_instructions_wait.rt = []
    # keep track of which components have finished
    test_instructionsComponents = [test_instructions_image, test_instructions_wait]
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
        if test_instructions_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            test_instructions_image.frameNStart = frameN  # exact frame index
            test_instructions_image.tStart = t  # local t and not account for scr refresh
            test_instructions_image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(test_instructions_image, 'tStartRefresh')  # time at next scr refresh
            test_instructions_image.setAutoDraw(True)
        
        # *test_instructions_wait* updates
        if test_instructions_wait.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            test_instructions_wait.frameNStart = frameN  # exact frame index
            test_instructions_wait.tStart = t  # local t and not account for scr refresh
            test_instructions_wait.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(test_instructions_wait, 'tStartRefresh')  # time at next scr refresh
            test_instructions_wait.status = STARTED
            # keyboard checking is just starting
            test_instructions_wait.clearEvents(eventType='keyboard')
        if test_instructions_wait.status == STARTED:
            theseKeys = test_instructions_wait.getKeys(keyList=['space', 'lctrl', 'rctrl'], waitRelease=False)
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
    test_phases.addData('test_instructions_image.started', test_instructions_image.tStartRefresh)
    test_phases.addData('test_instructions_image.stopped', test_instructions_image.tStopRefresh)
    # the Routine "test_instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    test_trials = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(stim_file),
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
        elif test_trials.thisN % rest_n != 0:
            continueRoutine = False
        else:
            continueRoutine = True 
            
        # Control delay
        draw_delay = continueRoutine
        test_break_ready.keys = []
        test_break_ready.rt = []
        # keep track of which components have finished
        test_breakComponents = [test_break_text, test_break_ready]
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
            
            # *test_break_text* updates
            if test_break_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                test_break_text.frameNStart = frameN  # exact frame index
                test_break_text.tStart = t  # local t and not account for scr refresh
                test_break_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(test_break_text, 'tStartRefresh')  # time at next scr refresh
                test_break_text.setAutoDraw(True)
            
            # *test_break_ready* updates
            if test_break_ready.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                test_break_ready.frameNStart = frameN  # exact frame index
                test_break_ready.tStart = t  # local t and not account for scr refresh
                test_break_ready.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(test_break_ready, 'tStartRefresh')  # time at next scr refresh
                test_break_ready.status = STARTED
                # keyboard checking is just starting
                test_break_ready.clearEvents(eventType='keyboard')
            if test_break_ready.status == STARTED:
                theseKeys = test_break_ready.getKeys(keyList=['space', 'lctrl', 'rctrl'], waitRelease=False)
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
        test_trials.addData('test_break_text.started', test_break_text.tStartRefresh)
        test_trials.addData('test_break_text.stopped', test_break_text.tStopRefresh)
        # the Routine "test_break" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "test_delay"-------
        routineTimer.add(5.000000)
        # update component parameters for each repeat
        if test_trials.thisN == 0:
            continueRoutine = True
        else:
            continueRoutine = draw_delay
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
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = test_delayClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=test_delayClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *test_delay_text* updates
            if test_delay_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                test_delay_text.frameNStart = frameN  # exact frame index
                test_delay_text.tStart = t  # local t and not account for scr refresh
                test_delay_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(test_delay_text, 'tStartRefresh')  # time at next scr refresh
                test_delay_text.setAutoDraw(True)
            if test_delay_text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > test_delay_text.tStartRefresh + 5.0-frameTolerance:
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
        
        # ------Prepare to start Routine "test_trial"-------
        # update component parameters for each repeat
        test_word.setText(word)
        test_resp.reset()
        # keep track of which components have finished
        test_trialComponents = [test_word, test_resp]
        for thisComponent in test_trialComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        test_trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True
        
        # -------Run Routine "test_trial"-------
        while continueRoutine:
            # get current time
            t = test_trialClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=test_trialClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *test_word* updates
            if test_word.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                test_word.frameNStart = frameN  # exact frame index
                test_word.tStart = t  # local t and not account for scr refresh
                test_word.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(test_word, 'tStartRefresh')  # time at next scr refresh
                test_word.setAutoDraw(True)
            # *test_resp* updates
            if test_resp.status == NOT_STARTED and t >= 0-frameTolerance:
                # keep track of start time/frame for later
                test_resp.frameNStart = frameN  # exact frame index
                test_resp.tStart = t  # local t and not account for scr refresh
                test_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(test_resp, 'tStartRefresh')  # time at next scr refresh
                test_resp.setAutoDraw(True)
            continueRoutine &= test_resp.noResponse  # a response ends the trial
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in test_trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "test_trial"-------
        for thisComponent in test_trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        test_trials.addData('test_word.started', test_word.tStartRefresh)
        test_trials.addData('test_word.stopped', test_word.tStopRefresh)
        # store data for test_trials (TrialHandler)
        test_trials.addData('test_resp.response', test_resp.getRating())
        test_trials.addData('test_resp.rt', test_resp.getRT())
        test_trials.addData('test_resp.started', test_resp.tStart)
        test_trials.addData('test_resp.stopped', test_resp.tStop)
        # the Routine "test_trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "iti"-------
        routineTimer.add(0.500000)
        # update component parameters for each repeat
        # keep track of which components have finished
        itiComponents = [iti_text]
        for thisComponent in itiComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        itiClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True
        
        # -------Run Routine "iti"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = itiClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=itiClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *iti_text* updates
            if iti_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                iti_text.frameNStart = frameN  # exact frame index
                iti_text.tStart = t  # local t and not account for scr refresh
                iti_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(iti_text, 'tStartRefresh')  # time at next scr refresh
                iti_text.setAutoDraw(True)
            if iti_text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > iti_text.tStartRefresh + .5-frameTolerance:
                    # keep track of stop time/frame for later
                    iti_text.tStop = t  # not accounting for scr refresh
                    iti_text.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(iti_text, 'tStopRefresh')  # time at next scr refresh
                    iti_text.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in itiComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "iti"-------
        for thisComponent in itiComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        test_trials.addData('iti_text.started', iti_text.tStartRefresh)
        test_trials.addData('iti_text.stopped', iti_text.tStopRefresh)
        thisExp.nextEntry()
        
    # completed 1 repeats of 'test_trials'
    
    # get names of stimulus parameters
    if test_trials.trialList in ([], [None], None):
        params = []
    else:
        params = test_trials.trialList[0].keys()
    # save data for this loop
    test_trials.saveAsExcel(filename + '.xlsx', sheetName='test_trials',
        stimOut=params,
        dataOut=['n','all_mean','all_std', 'all_raw'])
    
    # ------Prepare to start Routine "test_save_trials"-------
    # update component parameters for each repeat
    # Update the test_phase text for saving
    if test_phase == 'prac_test':
        task='practest'
    else:
        task='test'
        
    # Make the save file name (This should have accurate id as it is reading from it)
    suffix = 'sub-{}_task-{}_beh'.format(expInfo['id'], task)
    save_file = os.path.join(save_dir, suffix)
    
    # Save it many different ways
    test_trials.saveAsWideText(save_file + '.tsv')
    test_trials.saveAsWideText(save_file + '.csv')
    test_trials.saveAsPickle(save_file)
    
    # keep track of which components have finished
    test_save_trialsComponents = []
    for thisComponent in test_save_trialsComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    test_save_trialsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    continueRoutine = True
    
    # -------Run Routine "test_save_trials"-------
    while continueRoutine:
        # get current time
        t = test_save_trialsClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=test_save_trialsClock)
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
        for thisComponent in test_save_trialsComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "test_save_trials"-------
    for thisComponent in test_save_trialsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "test_save_trials" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "study_delay"-------
    routineTimer.add(5.000000)
    # update component parameters for each repeat
    if study_trials.thisN == 0:
        continueRoutine = True
    else:
        continueRoutine = draw_delay
    # keep track of which components have finished
    study_delayComponents = [study_delay_text]
    for thisComponent in study_delayComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    study_delayClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    continueRoutine = True
    
    # -------Run Routine "study_delay"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = study_delayClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=study_delayClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *study_delay_text* updates
        if study_delay_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            study_delay_text.frameNStart = frameN  # exact frame index
            study_delay_text.tStart = t  # local t and not account for scr refresh
            study_delay_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(study_delay_text, 'tStartRefresh')  # time at next scr refresh
            study_delay_text.setAutoDraw(True)
        if study_delay_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > study_delay_text.tStartRefresh + 5.0-frameTolerance:
                # keep track of stop time/frame for later
                study_delay_text.tStop = t  # not accounting for scr refresh
                study_delay_text.frameNStop = frameN  # exact frame index
                win.timeOnFlip(study_delay_text, 'tStopRefresh')  # time at next scr refresh
                study_delay_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in study_delayComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "study_delay"-------
    for thisComponent in study_delayComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    test_phases.addData('study_delay_text.started', study_delay_text.tStartRefresh)
    test_phases.addData('study_delay_text.stopped', study_delay_text.tStopRefresh)
    
    # ------Prepare to start Routine "phase_complete"-------
    routineTimer.add(2.000000)
    # update component parameters for each repeat
    # keep track of which components have finished
    phase_completeComponents = [phase_completed_text]
    for thisComponent in phase_completeComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    phase_completeClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    continueRoutine = True
    
    # -------Run Routine "phase_complete"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = phase_completeClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=phase_completeClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *phase_completed_text* updates
        if phase_completed_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            phase_completed_text.frameNStart = frameN  # exact frame index
            phase_completed_text.tStart = t  # local t and not account for scr refresh
            phase_completed_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(phase_completed_text, 'tStartRefresh')  # time at next scr refresh
            phase_completed_text.setAutoDraw(True)
        if phase_completed_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > phase_completed_text.tStartRefresh + 2.0-frameTolerance:
                # keep track of stop time/frame for later
                phase_completed_text.tStop = t  # not accounting for scr refresh
                phase_completed_text.frameNStop = frameN  # exact frame index
                win.timeOnFlip(phase_completed_text, 'tStopRefresh')  # time at next scr refresh
                phase_completed_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in phase_completeComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "phase_complete"-------
    for thisComponent in phase_completeComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    test_phases.addData('phase_completed_text.started', phase_completed_text.tStartRefresh)
    test_phases.addData('phase_completed_text.stopped', phase_completed_text.tStopRefresh)
# completed 1 repeats of 'test_phases'

thisExp.saveAsPickle(filename)
thisExp.saveAsWideText(filename + '.csv')
thisExp.saveAsWideText(filename + '.tsv')


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
