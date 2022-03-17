## ND2 consisted of 4 pre-registered experiments that investigated the relationship between prestimulus cues and memory. For preregistrations see https://osf.io/ydmun/.

##### Across experiment findings:

##### Task overview:
* The tasks were built in psychopy (https://www.psychopy.org/) with Experiments 2-4 being host online (https://pavlovia.org/). Each experiment consisted of a study and test phase. 
* The study phase varied slightly across experiments, but the general design had individuals make one of two semantic judgments about a list of words in either a informed, uninformed or no cue condition. For details see readme files associated with each experiment.<p align = "center"> <img src="https://github.com/nickwyeh/ND2/blob/main/figures/nd2.png" height = "200" width="600"> </p> 
* The test phase consisted of a recognition memory test for words seen in the study phase (old) intermixed with foil words (new). Participants made confidence rating judgments for each word (1= sure new, 2 = guess new, 3 = maybe new, 4 = maybe old, 5 = guess old, 6 = sure old). In Experiments 2-4, participants made an additional source memory judgment for words that they responded as being previously seen during the study phase (old response; i.e., 4, 5, or 6 response). Specifically, the source judgment was if the word was paired with a shoebox or manmade judgment during the study phase (4 = shoebox, 5 = manmade, 6 = dont know). The data will be made available following publication of the findings.


 ##### Directory structure overview:
* An example of the directory/folder structure is depicted below. Note, this follows the principals from the brain imaging data structure (https://bids-specification.readthedocs.io/en/stable/). Briefly this repo contains materials for 4 experiments with the individual tasks and data files nested within each experiment. The psychopy task and required materials are located in the task directory. The scripts required to organize, clean, and analyze the data are in matlab and located in the scripts directory. Summary descriptives of interest are ouputed in csv format to the analyses directory.   <p align="center"> <img src="https://github.com/nickwyeh/ND2/blob/main/figures/data_structure.png" width="400">  </p>
 
 
