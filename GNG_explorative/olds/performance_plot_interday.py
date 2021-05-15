import os 
from scipy.io import loadmat
import numpy as np
import matplotlib 
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt

# setup and load data 
general_dir= r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2' ###
specific_dir= r'\4F\GNG_explorative_noTrialManager_2\Session Data' 
os.chdir(general_dir + specific_dir)
plot_title= '4F' ###

data1= loadmat('4F_GNG_explorative_noTrialManager_2_20210128_115711.mat', simplify_cells=True)
data2= loadmat('4F_GNG_explorative_noTrialManager_2_20210129_115353.mat', simplify_cells=True)
data3= loadmat('4F_GNG_explorative_noTrialManager_2_20210130_114129.mat', simplify_cells=True)
data4= loadmat('4F_GNG_explorative_noTrialManager_2_20210131_121208.mat', simplify_cells=True)


# Setting up data
trial_types1= data1['SessionData']['TrialTypes']
number_of_trials1= data1['SessionData']['nTrials']
trials_data1= data1['SessionData']['RawEvents']['Trial']  # a list with every trial

trial_types2= data2['SessionData']['TrialTypes']
number_of_trials2= data2['SessionData']['nTrials']
trials_data2= data2['SessionData']['RawEvents']['Trial']  # a list with every trial

trial_types3= data3['SessionData']['TrialTypes']
number_of_trials3= data3['SessionData']['nTrials']
trials_data3= data3['SessionData']['RawEvents']['Trial']  # a list with every trial

trial_types4= data4['SessionData']['TrialTypes']
number_of_trials4= data4['SessionData']['nTrials']
trials_data4= data4['SessionData']['RawEvents']['Trial']  # a list with every trial

# Preprocessing data
percent_hits= np.empty(8)
percent_corr_rejections= np.empty(8)

#day 1
hits1= np.empty(300)
hits1[:]= np.nan     # nan if it is not a rewarding trial, 0 if missed, 1 if rewarded
correct_rejections1= np.empty(300)
correct_rejections1[:]= np.nan
rewarding_trials1= np.zeros(300)
neutral_trials1= np.zeros(300)
for i in range(0, 300):                                                 # for each trial
    if trial_types1[i]== 1 or trial_types1[i]== 3:                        # if it's o1 or o2 rewarded
        rewarding_trials1[i]= 1                                          # store trial index
        if not np.isnan(trials_data1[i]['States']['Reward'][0]):         # if rewarded
            hits1[i]= 1
        else:  
            hits1[i]=0
    elif trial_types1[i]== 2 or trial_types1[i]== 4:                      # if it's o1 or o2 fake rewarded
        rewarding_trials1[i]= 1
        if not np.isnan(trials_data1[i]['States']['FakeReward'][0]):
            hits1[i]= 1
        else:  
            hits1[i]= 0
    elif trial_types1[i]== 5 or trial_types1[i]== 6:                      # if it's neural trials
        neutral_trials1[i]= 1
        if not np.isnan(trials_data1[i]['States']['TimeOut'][0]):
            correct_rejections1[i]= 0
        else:
            correct_rejections1[i]= 1
cum_hits1= np.nansum(hits1[:29])
cum_corr_rejections1= np.nansum(correct_rejections1[:29])
cum_rewarding1= np.nansum(rewarding_trials1[:29])
cum_neutral1= np.nansum(neutral_trials1[:29])
percent_hits[0]= (cum_hits1/cum_rewarding1)*100
percent_corr_rejections[0]= (cum_corr_rejections1/cum_neutral1)*100
tot_hits1= np.nansum(hits1)
tot_corr_rejections1= np.nansum(correct_rejections1)
tot_rewarding_trials1= np.nansum(rewarding_trials1)
tot_neutral_trials1= np.nansum(neutral_trials1)
percent_hits[1]= (tot_hits1/tot_rewarding_trials1)*100
percent_corr_rejections[1]= (tot_corr_rejections1/tot_neutral_trials1)*100


#day 2
hits2= np.empty(300)
hits2[:]= np.nan     # nan if it is not a rewarding trial, 0 if missed, 1 if rewarded
correct_rejections2= np.empty(300)
correct_rejections2[:]= np.nan
rewarding_trials2= np.zeros(300)
neutral_trials2= np.zeros(300)
for i in range(0, 300):                                                 # for each trial
    if trial_types2[i]== 1 or trial_types2[i]== 3:                        # if it's o1 or o2 rewarded
        rewarding_trials2[i]= 1                                          # store trial index
        if not np.isnan(trials_data2[i]['States']['Reward'][0]):         # if rewarded
            hits2[i]= 1
        else:  
            hits2[i]=0
    elif trial_types2[i]== 2 or trial_types2[i]== 4:                      # if it's o1 or o2 fake rewarded
        rewarding_trials2[i]= 1
        if not np.isnan(trials_data2[i]['States']['FakeReward'][0]):
            hits2[i]= 1
        else:  
            hits2[i]= 0
    elif trial_types2[i]== 5 or trial_types2[i]== 6:                      # if it's neural trials
        neutral_trials2[i]= 1
        if not np.isnan(trials_data2[i]['States']['TimeOut'][0]):
            correct_rejections2[i]= 0
        else:
            correct_rejections2[i]= 1
cum_hits2= np.nansum(hits2[:29])
cum_corr_rejections2= np.nansum(correct_rejections2[:29])
cum_rewarding2= np.nansum(rewarding_trials2[:29])
cum_neutral2= np.nansum(neutral_trials2[:29])
percent_hits[2]= (cum_hits2/cum_rewarding2)*100
percent_corr_rejections[2]= (cum_corr_rejections2/cum_neutral2)*100
tot_hits2= np.nansum(hits2)
tot_corr_rejections2= np.nansum(correct_rejections2)
tot_rewarding_trials2= np.nansum(rewarding_trials2)
tot_neutral_trials2= np.nansum(neutral_trials2)
percent_hits[3]= (tot_hits2/tot_rewarding_trials2)*100
percent_corr_rejections[3]= (tot_corr_rejections2/tot_neutral_trials2)*100

#day 3
hits3= np.empty(300)
hits3[:]= np.nan     # nan if it is not a rewarding trial, 0 if missed, 1 if rewarded
correct_rejections3= np.empty(300)
correct_rejections3[:]= np.nan
rewarding_trials3= np.zeros(300)
neutral_trials3= np.zeros(300)
for i in range(0, 300):                                                 # for each trial
    if trial_types3[i]== 1 or trial_types3[i]== 3:                        # if it's o1 or o2 rewarded
        rewarding_trials3[i]= 1                                          # store trial index
        if not np.isnan(trials_data3[i]['States']['Reward'][0]):         # if rewarded
            hits3[i]= 1
        else:  
            hits3[i]=0
    elif trial_types3[i]== 2 or trial_types3[i]== 4:                      # if it's o1 or o2 fake rewarded
        rewarding_trials3[i]= 1
        if not np.isnan(trials_data3[i]['States']['FakeReward'][0]):
            hits3[i]= 1
        else:  
            hits3[i]= 0
    elif trial_types3[i]== 5 or trial_types3[i]== 6:                      # if it's neural trials
        neutral_trials3[i]= 1
        if not np.isnan(trials_data3[i]['States']['TimeOut'][0]):
            correct_rejections3[i]= 0
        else:
            correct_rejections3[i]= 1
cum_hits3= np.nansum(hits3[:29])
cum_corr_rejections3= np.nansum(correct_rejections3[:29])
cum_rewarding3= np.nansum(rewarding_trials3[:29])
cum_neutral3= np.nansum(neutral_trials3[:29])
percent_hits[4]= (cum_hits3/cum_rewarding3)*100
percent_corr_rejections[4]= (cum_corr_rejections3/cum_neutral3)*100
tot_hits3= np.nansum(hits3)
tot_corr_rejections3= np.nansum(correct_rejections3)
tot_rewarding_trials3= np.nansum(rewarding_trials3)
tot_neutral_trials3= np.nansum(neutral_trials3)
percent_hits[5]= (tot_hits3/tot_rewarding_trials3)*100
percent_corr_rejections[5]= (tot_corr_rejections3/tot_neutral_trials3)*100

#day 4
hits4= np.empty(300)
hits4[:]= np.nan     # nan if it is not a rewarding trial, 0 if missed, 1 if rewarded
correct_rejections4= np.empty(300)
correct_rejections4[:]= np.nan
rewarding_trials4= np.zeros(300)
neutral_trials4= np.zeros(300)
for i in range(0, 300):                                                 # for each trial
    if trial_types4[i]== 1 or trial_types4[i]== 3:                        # if it's o1 or o2 rewarded
        rewarding_trials4[i]= 1                                          # store trial index
        if not np.isnan(trials_data4[i]['States']['Reward'][0]):         # if rewarded
            hits4[i]= 1
        else:  
            hits4[i]=0
    elif trial_types4[i]== 2 or trial_types4[i]== 4:                      # if it's o1 or o2 fake rewarded
        rewarding_trials4[i]= 1
        if not np.isnan(trials_data4[i]['States']['FakeReward'][0]):
            hits4[i]= 1
        else:  
            hits4[i]= 0
    elif trial_types4[i]== 5 or trial_types4[i]== 6:                      # if it's neural trials
        neutral_trials4[i]= 1
        if not np.isnan(trials_data4[i]['States']['TimeOut'][0]):
            correct_rejections4[i]= 0
        else:
            correct_rejections4[i]= 1
cum_hits4= np.nansum(hits4[:29])
cum_corr_rejections4= np.nansum(correct_rejections4[:29])
cum_rewarding4= np.nansum(rewarding_trials4[:29])
cum_neutral4= np.nansum(neutral_trials4[:29])
percent_hits[6]= (cum_hits4/cum_rewarding4)*100
percent_corr_rejections[6]= (cum_corr_rejections4/cum_neutral4)*100
tot_hits4= np.nansum(hits4)
tot_corr_rejections4= np.nansum(correct_rejections4)
tot_rewarding_trials4= np.nansum(rewarding_trials4)
tot_neutral_trials4= np.nansum(neutral_trials4)
percent_hits[7]= (tot_hits4/tot_rewarding_trials4)*100
percent_corr_rejections[7]= (tot_corr_rejections4/tot_neutral_trials4)*100


# Plots 
from matplotlib.patches import Rectangle
fig,ax= plt.subplots(constrained_layout=True)   
fig.suptitle(plot_title)
x_axes= np.arange(1,9)
ax.plot(x_axes, percent_hits, 'b', label='Hits')
ax.plot(x_axes, percent_corr_rejections, 'r', label='Correct rejections')
ax.legend(loc='lower right')
ax.set_ylabel('%')
#ax.set_ylim([50,102])
ax.set_xlabel('Session')
ax.set_xticks([1.5, 3.5, 5.5, 7.5])
ax.set_xticklabels(['1', '2', '3', '4'])
for i in [1,3,5,7]:
    ax.add_patch(Rectangle((i,0,), 1, 100, alpha=0.5))
fig.show()