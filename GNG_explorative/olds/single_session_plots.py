import os 
from scipy.io import loadmat
import numpy as np
import pandas as pd
import matplotlib 
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# setup and load data 
general_dir= r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Categorization_no_punishment\Data\2F' ###
specific_dir= r'\GNG_exporative_noTrialManager\Session Data' 
plot_dir= r'\GNG_exporative_noTrialManager\Plots'  
plot_name= '01.22.2020_proportion.png' ###
os.chdir(general_dir + specific_dir)
data= loadmat('2F_GNG_exporative_noTrialManager_20210122_125326.mat', simplify_cells=True)
mouse_id= 'Mouse 2' ###

data= data['SessionData']
trial_types= data['TrialTypes']
number_of_trials= data['nTrials']
trial_data= data['RawEvents']['Trial']  # a list with every trial

# If animal licked during response time for each trial 
lick_during_response_time= np.zeros(number_of_trials)
for trial in range(0, number_of_trials - 1):    #check all trials   
    if 'Port1In' in trial_data[trial]['Events']:    #if there was a PortIn then check when 
        if isinstance(trial_data[trial]['Events']['Port1In'], (list, tuple, np.ndarray)):    # check if it is a float or an array  
            port1in= np.zeros(len(trial_data[trial]['Events']['Port1In']))
            for i in range(0, len(port1in)): 
                if trial_data[trial]['Events']['Port1In'][i] >= trial_data[trial]['States']['TimeForResponse'][0] and trial_data[trial]['Events']['Port1In'][i] <= trial_data[trial]['States']['TimeForResponse'][1]:
                    port1in[i]= 1
            if np.any(port1in):
                lick_during_response_time[trial]= 1 
        else: 
            if trial_data[trial]['Events']['Port1In'] >= trial_data[trial]['States']['TimeForResponse'][0] and trial_data[trial]['Events']['Port1In'] <= trial_data[trial]['States']['TimeForResponse'][1]:
                lick_during_response_time[trial]= 1    
    else: 
        lick_during_response_time[trial]= 0 

# If animal licked after the stimulus presentation but before time for response window
anticipatory_licks= np.zeros(number_of_trials)
for trial in range(0, number_of_trials - 1):    # check all trials   
    if 'Port1In' in trial_data[trial]['Events']:    # if there was a PortIn then check when 
        if isinstance(trial_data[trial]['Events']['Port1In'], (list, tuple, np.ndarray)):    # check if it is a float or an array  
            port1in= np.zeros(len(trial_data[trial]['Events']['Port1In']))
            for i in range(0, len(port1in)): 
                if trial_data[trial]['Events']['Port1In'][i] >= trial_data[trial]['States']['DeliverStimulus'][0] and trial_data[trial]['Events']['Port1In'][i] <= trial_data[trial]['States']['DeliverStimulus'][1]:
                    port1in[i]= 1
            if np.any(port1in):
                anticipatory_licks[trial]= 1 
        else: 
            if trial_data[trial]['Events']['Port1In'] >= trial_data[trial]['States']['DeliverStimulus'][0] and trial_data[trial]['Events']['Port1In'] <= trial_data[trial]['States']['DeliverStimulus'][1]:
                anticipatory_licks[trial]= 1    
    else: 
        anticipatory_licks[trial]= 0 
# Substitute case code with odor code
trial_types_odor_based= np.zeros(len(trial_types))
for i in range(0, len(trial_types)):
    if trial_types[i] == 1 or trial_types[i] == 2:
        trial_types_odor_based[i]= 1
    elif trial_types[i] == 3 or trial_types[i] == 4:
        trial_types_odor_based[i]= 2
    elif trial_types[i] == 5:
        trial_types_odor_based[i]= 3
    elif trial_types[i] == 6:
        trial_types_odor_based[i]= 4
    elif trial_types[i] == 7:
        trial_types_odor_based[i]= 5


# Create df and useful variables for plotting
df= pd.DataFrame(((trial_types, trial_types_odor_based, anticipatory_licks, lick_during_response_time))).T 
df.columns= ['Trial types', 'Trial types odor', 'Anticipatory licks', 'Licks in response window']

anticipatory_licks_plot= []
anticipatory_licks_x= []
for i in range (0, len(trial_types)):
    if df['Anticipatory licks'][i] == 1:
        anticipatory_licks_plot.append(df['Trial types odor'][i])
        anticipatory_licks_x.append(i+1)

right_time_licks_plot= []
right_time_licks_x= []
for i in range (0, len(trial_types)):
    if df['Licks in response window'][i] == 1:
        right_time_licks_plot.append(df['Trial types odor'][i]) 
        right_time_licks_x.append(i+1)

count_ant_licks=[]
count_right_licks=[]
for i in range (1,6):
    count_ant_licks.append(anticipatory_licks_plot.count(i))
for i in range (1,6):
    count_right_licks.append(right_time_licks_plot.count(i))

proportion_ant_licks=[]
proportion_right_licks=[]
for i in range (0,5):
    proportion_ant_licks.append(count_ant_licks[i]/np.sum(trial_types== i+1))
for i in range (0,5):
    proportion_right_licks.append(count_right_licks[i]/np.sum(trial_types== i+1))

# Plots
fig= make_subplots(rows=1, cols=2, shared_yaxes=True,
                    horizontal_spacing=0.05, column_widths=[0.8,0.2])
fig.add_trace(go.Scatter(x=anticipatory_licks_x, y=anticipatory_licks_plot, 
                         mode='markers', name='Anticipatory licks'), row=1, col=1)
fig.add_trace(go.Scatter(x=right_time_licks_x, y=right_time_licks_plot,
                         mode='markers', name='Right-window licks'), row=1, col=1)

fig.add_trace(go.Bar(x=proportion_ant_licks, y=[1,2,3,4,5], orientation='h', marker_color='blue', showlegend=False), row=1,  col=2)
fig.add_trace(go.Bar(x=proportion_right_licks, y=[1,2,3,4,5], orientation='h', marker_color='red', showlegend=False), row=1, col=2)

fig.update_xaxes(title_text='Trials', showline=True, linecolor='black', linewidth=1, range=[0,170],
                 tickmode='linear', tick0=0, dtick=10, autorange=True,
                 row=1,col=1)
fig.update_yaxes(title_text= 'Odors', autorange=True, showline=True, linecolor='black', 
                linewidth=1, row=1,col=1)
fig.update_xaxes(autorange=True,
                 visible=False,  row=1,col=2)
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', 
                    legend=dict(orientation='h',
                                xanchor='center', x=0.5,
                                yanchor='top', y=-0.1),
                    autosize=False, width=1280, height=720,
                    title=mouse_id)
#fig.show(renderer='browser')

os.chdir(general_dir + plot_dir)
fig.write_image(plot_name)