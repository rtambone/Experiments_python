import os 
import glob 
from scipy.io import loadmat
import numpy as np
import pandas as pd
import matplotlib 
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
from spykes.plot.neurovis import NeuroVis

# setup and load data 
os.chdir(r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\4F\GNG_explorative_noTrialManager_2\Session Data')
data=[]
for file in glob.glob('*.mat'):
    data.append(loadmat(file, simplify_cells=True))
    
# preprocess data
days_list=[]
for day in range(0,len(data)):
    trial_types= data[day]['SessionData']['TrialTypes']
    trials_data= data[day]['SessionData']['RawEvents']['Trial']  # a list with every trial
    df= pd.DataFrame(columns=['events','condition'])
    timestamps=[]
    case=[]
    for trial in range(0, len(trials_data)):      
        if 'Port1In' in trials_data[trial]['Events'] and isinstance(trials_data[trial]['Events']['Port1In'],np.ndarray):    #if there was a PortIn 
        #port1in= trials_data1[i]['Events']['Port1In'] - 3
            for z in range(0,len(trials_data[trial]['Events']['Port1In'])):
                timestamps.append(trials_data[trial]['Events']['Port1In'][z])
                case.append(trial_types[trial])
    timestamps= np.array(timestamps) - 3
    case= np.array(case)    
    df['events']= timestamps
    df['condition']= case 
    days= NeuroVis(timestamps, name='day_'+str(day+1))
    days_list.append(days)
    
plt.figure()
psth= days_list[0].get_psth(event='events', df= df_days[0], conditions= 'condition',
                            window=[-3000, 18000], binsize=100)





'''
trial_types2= data2['SessionData']['TrialTypes']
number_of_trials2= data2['SessionData']['nTrials']
trials_data2= data2['SessionData']['RawEvents']['Trial']  # a list with every trial

trial_types3= data3['SessionData']['TrialTypes']
number_of_trials3= data3['SessionData']['nTrials']
trials_data3= data3['SessionData']['RawEvents']['Trial']  # a list with every trial

trial_types4= data4['SessionData']['TrialTypes']
number_of_trials4= data4['SessionData']['nTrials']
trials_data4= data4['SessionData']['RawEvents']['Trial']  # a list with every trial


1. align port1in with onset stimulus (n times= 300)
2. divide stimulus period T into N bins of size delta
3. count the number of spikes k from all n sequences that fall in the bin i
4. draw histohram w

event
condition

'''

# Data preprocessing 
# align port1in with deliver stimulus
df= pd.DataFrame(columns=['events','condition'])
timestamps=[]
case=[]


 
for i in range(0, number_of_trials1):      
    if 'Port1In' in trials_data1[i]['Events'] and isinstance(trials_data1[i]['Events']['Port1In'],np.ndarray):    #if there was a PortIn 
        #port1in= trials_data1[i]['Events']['Port1In'] - 3
        for z in range(0,len(trials_data1[i]['Events']['Port1In'])):
            timestamps.append(trials_data1[i]['Events']['Port1In'][z])
            case.append(trial_types1[i])
    
timestamps= np.array(timestamps) - 3
case= np.array(case)    
df['events']= timestamps
df['condition']= case 

day=[]
day.append(df)

from spykes import NeuroVis
plt.figure()
psth= day.get_psth()





for i in range(0, number_of_trials1):    
    if trial_types1[i]== 1:  #cs1+
        if 'Port1In' in trials_data1[i]['Events'] and isinstance(trials_data1[i]['Events']['Port1In'],np.ndarray):    #if there was a PortIn 
            timestamps.extend(trials_data1[i]['Events']['Port1In'])
            case.extend(trial_types1[i])
'''       
if isinstance(trials_data1[i]['Events']['Port1In'],np.ndarray):
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







        port1in= trials_data1[i]['Events']['Port1In'] - 0.5
        port1in_timestamps_aligned.append(port1in)
    else: 
        port1in= np.nan
        port1in_timestamps_aligned.append(port1in)        
cs1plus_port1in= []
cs1_port1in=[]
hist_cs1plus=[]

cs2plus_port1in=[]
cs2_port1in=[]
ns1_port1in=[]
ns2_port1in=[]
us_port1in=[]
for i in range(0, number_of_trials1):
    if trial_types1[i]== 1:  #cs1+
        if isinstance(port1in_timestamps_aligned[i],np.ndarray):
            cs1plus_port1in.append(port1in_timestamps_aligned[i])
            hist_cs1plus.append(np.histogram(cs1plus_port1in[i], bins=np.arange(0,18,0.1), density=False))

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




hist_cs1plus, bin_edges_cs1plus= np.histogram(cs1plus_port1in, bins=np.arange(0,18,0.1), density=False)
hist_cs1, bin_edges_cs1= np.histogram(cs1_port1in, bins=np.arange(0,18,0.1), density=False)


plt.plot(bin_edges_cs1plus[:-1], hist_cs1plus/61, label='cs1+')
plt.plot(bin_edges_cs1[:-1], hist_cs1/61, label='cs1')
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
'''