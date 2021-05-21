# -*- coding: utf-8 -*-
"""
Created on Tue May 18 18:42:20 2021

@author: ricca
"""
from IPython import get_ipython
get_ipython().magic('reset -sf')


import os 
import glob 
from scipy.io import loadmat
import numpy as np
import matplotlib 
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# List of dirs
# index        0       1       2      3       4       5      6      7     8       9
mouse_list= ['PV92','PV94','PV100','PV104','PV107','WT58','WT96','WT97','WT98','WT101']
mouse_name = mouse_list[0]  # CHANGE THIS
day= '0'                    # AND THIS
general_dir = r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Optoinhibition\optoinhibition\exp\discrimination'
mouse_dir= general_dir + '\\'+ mouse_name


# Load data 
os.chdir(mouse_dir)
data=[]
for file in glob.glob('*.mat'):
    data.append(loadmat(file, simplify_cells=True))

trial_types= data[int(day)]['SessionData']['TrialTypes']
trials_data= data[int(day)]['SessionData']['RawEvents']['Trial'] # a list with every trial
nTrials= len(trial_types)
nTrialPlus= len(np.where(trial_types==2)[0])
nTrialMinus= len(np.where(trial_types==1)[0])







def get_psth(data, sig, time_windows, error_type= 'bootstrap', adaptive_warp=False): 
    """
    Function to get psth with a Gaussian kernel, defined by sig
    It returns t (timeline for x axes) and R (counts of occurences)
    Data is a matrix with rows= trials and columns= licks
    """
    #time_windows= np.array(time_windows)   
    import math
    import numpy as np
    nTrials= len(data)      #NT
    #D= np.array(nTrials, )
    nLicks= 0       #N_tot
    ND= np.zeros(nTrials)
    for i in range(0, nTrials):
        if isinstance(data[i], float):
            ND[i]= 1
            nLicks= nLicks+1
        else: 
            nLicks= nLicks + len(data[i])
            ND[i]= len(data[i])      #ND
    #licksMax= max(ND)       #N_max
    
    # if kernel density is such that there are on avarage one or less spikes
    # under the kernel then the units are probably wrong 
    try:
        L= nLicks/(nTrials*(time_windows[1]-time_windows[0]))
        if 2*L*nTrials*sig < 1 or L < 0.1:
            print('timestamps very low density')
    except ZeroDivisionError:
        print('Zero Division Error occured')
        
    # smear each spike out 
    # std dev is sqrt(rate*(integral over kernel^2)/trials) 
    # for gaussian integral over kernel^2 is 1/(2*sig*sqrt(pi))
    N_pts= np.fix(5*(time_windows[1]-time_windows[0])/sig)
    t= np.linspace(time_windows[0], time_windows[1], int(N_pts))
    
    RR= np.zeros((nTrials, int(N_pts)))
    f= 1/(2*sig**2)
    for n in range(0,nTrials):
        for m in range(0, int(ND[n])):
            if not isinstance(data[n], float):
                RR[n,:]= RR[n,:] + np.exp(-f*np.power(t-data[n][m],2))
            else: 
                RR[n,:]= RR[n,:] + np.exp(-f*np.power(t-data[n],2))
    RR= RR*(1/np.sqrt(2*math.pi*sig**2))
    #if nTrials > 1:
    R= np.mean(RR, axis=0) 
    #else: 
    #   R= RR
    
    # compute error
    if error_type== 'poisson':
        E= np.sqrt(R/(2*nTrials*sig*np.sqrt(math.pi)))
    elif error_type== 'bootstrap':
        nboot= 10
        mE= 0
        sE= 0 
        for b in range(0,nboot):
            indx= nTrials*np.random.rand(1,nTrials)
            for l in range (0,len(indx[0])):
                indx[0,l]= math.floor(indx[0,l])+1
            mtmp= np.mean(RR[indx])
            mE= mE+mtmp
            sE= sE+mtmp**2
        E= np.sqrt(sE/nboot - mE**2/nboot**2)
    
    
    # adaptive warp sig, so that on avarage the number of spikes under the kernel
    # but regions where there is more data have a smaller kernel
    if adaptive_warp== True:
        sigt= np.mean(R)*sig/R
        RR= np.zeros(nTrials, N_pts)
        f= 1/(2*sigt**2)
        for n in range(0,nTrials):
            for m in range(0, int(ND[n])):
                RR[n,:]= RR[n,:] + np.exp(-f*np.power(t-data[n][m],2))
        RR= RR*(1/np.sqrt(2*math.pi*sig**2))
        if nTrials > 1:
            R= np.mean(RR, axis=0)
        else: 
            R= RR
    
    return R, t, E




colors= [31,120,180],[106,61,154],[227,26,28],[251,127,0],[82,82,82]
colors= np.divide(colors, 251)

fig, ax= plt.subplots(nrows=2, ncols=2,constrained_layout=True)
fig.suptitle(mouse_name)
for TrialType in range(1,3):
    licksXtrial=[]
    idxTrialType= np.array(np.where(trial_types== TrialType))
    for Trial in range(0, idxTrialType.size):
        if 'Port1In' in trials_data[idxTrialType[0][Trial]]['Events']:    #if there was a PortIn 
           licks_ts= trials_data[idxTrialType[0][Trial]]['Events']['Port1In']   # centered on valve opening
           licksXtrial.append(licks_ts)
    [R,t]= get_psth(licksXtrial, sig=0.1, time_windows= [-2, 26])
    if TrialType==1:    # valve click no odor
        ax.flat[0].plot(t, R, color= colors[4], linewidth=1.5, label='CS-')
    elif TrialType==2:
        ax.flat[0].plot(t, R, color= colors[2], linewidth=1.5, label='CS+')
    ax.flat[0].legend()
    ax.flat[0].set_title('')
    #ax.axvline(color='black', x=6)
    ax.flat[0].set_xlabel('Time (s)')
    ax.flat[0].set_ylabel('Hz')
ax.flat[0].add_patch(Rectangle((5,0), 
                       width= 2, height= abs(ax.flat[0].get_ylim()[1]),
                       alpha=0.5))
ax.flat[0].add_patch(Rectangle((10,0), 
                       width= 1, height= abs(ax.flat[0].get_ylim()[1]),
                              alpha=0.5, color= 'red'))

