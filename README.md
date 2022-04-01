## ND2 consisted of 4 pre-registered experiments that investigated the relationship between prestimulus cues and memory.
##### Open science framework: https://osf.io/ydmun/.

##### Across experiment findings:
* Broadly, prestimulus encoding cues benefitted memory performance and the pattern of memory enhancement varied with how memory was assessed. Dual signal process detection (DSPD) estimates of familiarity demonstrated a graded pattern with the informativeness of the prestimulus cues (i.e., informative > uninformative > no cues). In addition, both informative and uninformative prestimulus cues compared to no prestimulus cues enhanced subsequent source memory accuracy. 

##### Task overview:
* Each experiment was comprised a study and test phase and which was built in psychopy (https://www.psychopy.org/) with Experiments 2-4 being host online (https://pavlovia.org/). Note, Experiment 2 also had data collected in-person but it is not currently available in this repo.
* The study phase varied slightly across experiments, but the general design had individuals make one of two semantic judgments (manmade, shoebox) about a list of words (nouns) in either a informed, uninformed or no cue condition. For details see readme files associated with each experiment.<p align = "center"> <img src="https://github.com/nickwyeh/ND2/blob/main/figures/nd2.png" height = "200" width="600"> </p> 
* The test phase consisted of a recognition memory test for words seen in the study phase (old) intermixed with foil words (new). Participants made confidence rating judgments for each word (1= sure new, 2 = guess new, 3 = maybe new, 4 = maybe old, 5 = guess old, 6 = sure old). In Experiments 2-4, participants made an additional source memory judgment for words that they responded as being previously seen during the study phase (old response; i.e., 4, 5, or 6 response). Specifically, the source judgment was if the word was paired with a shoebox or manmade judgment during the study phase (4 = shoebox, 5 = manmade, 6 = dont know). The data will be made available following publication of the findings.


 ##### Directory structure overview:
* An example of the directory/folder structure is depicted below. Note, this follows the principals from the brain imaging data structure (https://bids-specification.readthedocs.io/en/stable/). Briefly this repo contains materials for 4 experiments with the individual tasks and data files nested within each experiment. The psychopy task and required materials are located in the task directory. 
* `scripts` directory contains matlab and R code. All organization, cleaning, and analyses were done with matlab scripts. Data visualzation was done in R. 
* `source data` directory contains the original psychopy format behavioral files for each participants. 
* `raw data` directory contains cleaned behavioral data for each participant with a json file to explain the data. 
* `data files` directroy contains cleaned data and additional analyses (ROCs) for each participant.
* `analyses` directory contains summary descriptives of interest.  
* <p align="center"> <img src="https://github.com/nickwyeh/ND2/blob/main/figures/data_structure.png" width="400">  </p>
 
 
