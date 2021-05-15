import os 
import numpy as np
import matplotlib 
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt

# setup and load data 
general_dir= r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2' ###
specific_dir= r'\1F\GNG_explorative_noTrialManager_2\Session Data' 
plot_dir= r'\1F\Plots'  
plot_title= '1F - Day 1' ###
os.chdir(general_dir + specific_dir)

import pickle 
with open('data_dict', 'rb') as data_dict_fil:
    data_1f= pickle.load(data_dict_fil)

# Setting up data
trial_types= data_1f['TrialTypes']
number_of_trials= data_1f['nTrials']
trials_data= data_1f['RawEvents']  # a list with every trial

# Preprocessing data (states-based)
hits= np.empty(300)
hits[:]= np.nan     # nan if it is not a rewarding trial, 0 if missed, 1 if rewarded
correct_rejections= np.empty(300)
correct_rejections[:]= np.nan
rewarding_trials= np.zeros(300)
neutral_trials= np.zeros(300)

for i in range(0, 300):                                                 # for each trial
    if trial_types[i]== 1 or trial_types[i]== 3:                        # if it's o1 or o2 rewarded
        rewarding_trials[i]= 1                                 # store trial index
        if not np.isnan(trials_data[i]['States']['Reward'][0]):         # if rewarded
            hits[i]= 1
        else:  
            hits[i]=0
    elif trial_types[i]== 2 or trial_types[i]== 4:                      # if it's o1 or o2 fake rewarded
        rewarding_trials[i]= 1
        if not np.isnan(trials_data[i]['States']['FakeReward'][0]):
            hits[i]= 1
        else:  
            hits[i]= 0
    elif trial_types[i]== 5 or trial_types[i]== 6:                      # if it's neural trials
        neutral_trials[i]= 1
        if np.isnan(trials_data[i]['States']['TimeOut'][0]):
            correct_rejections[i]= 1
        else:
            correct_rejections[i]= 0

cum_hits= np.empty(30)
cum_corr_rejections= np.empty(30)
cum_rewarding= np.empty(30)
cum_neutral= np.empty(30)
for i,c in zip(range(0,300,10),range(31)):
    cum_rewarding[c]= np.nansum(rewarding_trials[:i+9])
    cum_neutral[c]= np.nansum(neutral_trials[:i+9])
    cum_hits[c]=np.nansum(hits[:i+9])
    cum_corr_rejections[c]=np.nansum(correct_rejections[:i+9])

cum_percent_hits= (cum_hits/cum_rewarding)*100
cum_percent_corr_rejection= (cum_corr_rejections/cum_neutral)*100

'''
## Preprocessing data (anticipatory licks-based)
aLicks_hits= np.empty(300)
aLicks_hits[:]= np.nan     # nan if it is not a rewarding trial, 0 if missed, 1 if rewarded
aLicks_correct_rejections= np.empty(300)
aLicks_correct_rejections[:]= np.nan

for i in range(0, 300):                                                 # for each trial
    if trial_types[i]== 1 or trial_types[i]== 3:                        # if it's o1 or o2 rewarded  
        if not np.isnan(trials_data[i]['States']['Reward'][0]):         # if rewarded
            for portIn in range(len(trials_data[i]['Events']['Port1In'])): # for each portIn timestamps check if at least one happend in deliverStimulusLate
                if trials_data[i]['Events']['Port1In'][portIn]>= trials_data[i]['States']['DeliverStimulusLate'][0] and trials_data[i]['Events']['Port1In'][portIn]<= trials_data[i]['States']['DeliverStimulusLate'][1]:
                    aLicks_hits[i]=1
                else:  
                    aLicks_hits[i]=0
    elif trial_types[i]== 2 or trial_types[i]== 4:                      # if it's o1 or o2 fake rewarded
        if not np.isnan(trials_data[i]['States']['FakeReward'][0]):
            for portIn in range(len(trials_data[i]['Events']['Port1In'])): # for each portIn timestamps check if at least one happend in deliverStimulusLate
                if trials_data[i]['Events']['Port1In'][portIn]>= trials_data[i]['States']['DeliverStimulusLate'][0] and trials_data[i]['Events']['Port1In'][portIn]<= trials_data[i]['States']['DeliverStimulusLate'][1]:
                    aLicks_hits[i]=1
                else:  
                    aLicks_hits[i]=0
#    elif trial_types[i]== 5 or trial_types[i]== 6:                      # if it's neural trials
#        if not np.isnan(trials_data[i]['States']['TimeOut'][0]):
#            for portIn in range(len(trials_data[i]['Events']['Port1In'])): # for each portIn timestamps check if at least one happend in deliverStimulusLate
#                if trials_data[i]['Event']['Port1In'][portIn]>= trials_data[i]['States']['DeliverStimulusLate'][0] and trials_data[i]['Event']['Port1In'][portIn]<= trials_data[i]['States']['DeliverStimulusLate'][1]:
#                    aLicks_correct_rejections[i]= 1
#                else:
#                    aLicks_correct_rejections[i]= 0

cum_aLicks_hits= np.empty(30)
#cum_aLicks_corr_rejections= np.empty(30)
#cum_rewarding= np.empty(30) già calcolati prima
#cum_neutral= np.empty(30)
for i,c in zip(range(0,300,10),range(31)):
    cum_aLicks_hits[c]=np.nansum(hits[:i+9])
    #cum_aLicks_corr_rejections[c]=np.nansum(correct_rejections[:i+9])

cum_percent_aLicks_hits= (cum_aLicks_hits/cum_rewarding)*100
#cum_percent_corr_rejection= (cum_corr_rejections/cum_neutral)*100
'''

# Plots 
fig, axes= plt.subplots()  # default dpi 
fig.suptitle(plot_title)
x_axes= np.arange(10,310,10)
axes.plot(x_axes, cum_percent_hits, 'b', label='Hits')
axes.plot(x_axes, cum_percent_corr_rejection, 'r', label='Correct rejections')
axes.legend(loc='lower right')
axes.set_ylabel('%')
axes.set_ylim([0,100])
axes.set_xlabel('Trials')
fig.tight_layout()
fig.show()









'''
# Data preprocessing
licked_trials_timestamps=[] # port1in timestamps
licked_trials_types=[]      # types of trials
licked_trials=[]            # trial number  
for trial in range(0, number_of_trials):    #check all trials   
    if 'Port1In' in trials_data[trial]['Events']:    #if there was a PortIn 
        port1in_timestamps= np.array([trials_data[trial]['Events']['Port1In']])
        licked_trials_timestamps.append(port1in_timestamps)    
        licked_trials_types.append(trial_types[trial])
        licked_trials.append(trial)



        
reward_opening_time=[]        
for i in range(0, number_of_trials):
    if trial_types[i]== 1 or trial_types[i]== 2:
        reward_opening_time.append(trials_data[i]['States']['Reward'][0])
    elif trial_types[i]== 3 or trial_types[i]== 4:

for i in range(0, len(rewarding_trials)):
    rewarding_trials[i]= rewarding_trials[i] - reward_opening_time[i]
'''