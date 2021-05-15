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
plot_title= '4F'

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

'''
1. align port1in with onset stimulus (n times= 300)
2. divide stimulus period T into N bins of size delta
3. count the number of spikes k from all n sequences that fall in the bin i
4. draw histohram w
'''

# Data preprocessing 
# align port1in with deliver stimulus
port1in_timestamps_aligned=[]   # 
for i in range(0, number_of_trials1):      
    if 'Port1In' in trials_data1[i]['Events']:    #if there was a PortIn 
        port1in= trials_data1[i]['Events']['Port1In'] - 3
        port1in_timestamps_aligned.append(port1in)
    else: 
        port1in= np.nan
        port1in_timestamps_aligned.append(port1in)        
cs1plus_port1in= []
cs1_port1in=[]
cs2plus_port1in=[]
cs2_port1in=[]
ns1_port1in=[]
ns2_port1in=[]
us_port1in=[]
for i in range(0, len(port1in_timestamps_aligned)):
    if trial_types1[i]== 1:  #cs1+
        if isinstance(port1in_timestamps_aligned[i],np.ndarray):
            cs1plus_port1in.extend(port1in_timestamps_aligned[i])
    elif trial_types1[i]== 2:
        if isinstance(port1in_timestamps_aligned[i],np.ndarray):
            cs1_port1in.extend(port1in_timestamps_aligned[i])
    elif trial_types1[i]== 3:
        if isinstance(port1in_timestamps_aligned[i],np.ndarray):
            cs2plus_port1in.extend(port1in_timestamps_aligned[i])
    elif trial_types1[i]== 4:
        if isinstance(port1in_timestamps_aligned[i],np.ndarray):
            cs2_port1in.extend(port1in_timestamps_aligned[i])
    elif trial_types1[i]== 5:
        if isinstance(port1in_timestamps_aligned[i],np.ndarray):
            ns1_port1in.extend(port1in_timestamps_aligned[i])
    elif trial_types1[i]== 6:
        if isinstance(port1in_timestamps_aligned[i],np.ndarray):
            ns2_port1in.extend(port1in_timestamps_aligned[i])
    elif trial_types1[i]== 7:
        if isinstance(port1in_timestamps_aligned[i],np.ndarray):
            us_port1in.extend(port1in_timestamps_aligned[i])

# create bin and assing data to bins
bins= np.linspace(0,36,37)      # 2 hz
bin_idx_cs1plus=np.digitize(cs1plus_port1in, bins, right=False)
count_cs1plus= np.bincount(bin_idx_cs1plus, minlength=37)

bin_idx_cs1=np.digitize(cs1_port1in, bins, right=False)
count_cs1= np.bincount(bin_idx_cs1, minlength=37)

bin_idx_cs2plus=np.digitize(cs2plus_port1in, bins, right=False)
count_cs2plus= np.bincount(bin_idx_cs2plus, minlength=37)

bin_idx_cs2=np.digitize(cs2_port1in, bins, right=False)
count_cs2= np.bincount(bin_idx_cs2, minlength=37)

bin_idx_ns1=np.digitize(ns1_port1in, bins, right=False)
count_ns1= np.bincount(bin_idx_ns1, minlength=37)

bin_idx_ns2=np.digitize(ns2_port1in, bins, right=False)
count_ns2= np.bincount(bin_idx_ns2, minlength=37)

bin_idx_us=np.digitize(us_port1in, bins, right=False)
count_us= np.bincount(bin_idx_us, minlength=37)




bins= bins/2
plt.plot(bins, count_cs1plus/61, label='cs1+')
plt.plot(bins, count_cs1/7, label='cs1')
plt.plot(bins, count_cs2plus/61, label='cs2+')
plt.plot(bins, count_cs2/7, label='cs2')
plt.plot(bins, count_ns1/67, label='ns1')
plt.plot(bins, count_ns2/67, label='ns2')
plt.plot(bins, count_us/30, label='us')
plt.legend()
plt.show()       
    
# Plots
fig, axes= plt.subplots(constrained_layout=True)  # default dpi 
fig.suptitle(plot_title)
# rewarding trials
for i in range(0,len(rewarding_ntrials)):
    if not isinstance(port1in_timestamps_aligned[i], np.float):
        yaxes= np.array([rewarding_ntrials[i]]*len(port1in_timestamps[i]))
        axes.plot(port1in_timestamps_aligned[i], yaxes, 'bo')  
axes.axvline(color='red')
axes.set_xlabel('Time (s)')
axes.set_ylabel('Trials')
#axes[0].set_title('Rewarding trials')
#fig.tight_layout()
fig.show()
#plt.savefig(fname=general_dir+plot_dir+plot_name)