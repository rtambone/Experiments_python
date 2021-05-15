import os 
from scipy.io import loadmat
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# setup and load data 
dir= r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\SocRecog\Data'
plot_dir= r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\SocRecog\Plots'
os.chdir(dir)
os.chdir(dir + '\\3M\\12.12.20')    # 
data= loadmat('3m_post-test.mat', simplify_cells=True)  #
figure_name= '3M\odor_preference_time.svg'  #

# preprocess data 
npokes1= data['log']['numberOfPokes']['stimulus1']
npokes2= data['log']['numberOfPokes']['stimulus2']
onsets1= data['log']['onsets']['stimulus1'].reshape(npokes1,)
onsets2= data['log']['onsets']['stimulus2'].reshape(npokes2,)
elapsedtime1= data['log']['logStimuliElapsedTimes']['stimulus_1'][:npokes1].reshape(npokes1,)
elapsedtime2= data['log']['logStimuliElapsedTimes']['stimulus_2'][:npokes2].reshape(npokes2,)
d1= dict(onsets1= onsets1,
        pokes1times= elapsedtime1)
d2= dict(onsets2= onsets2,
        pokes2times= elapsedtime2)
df1= pd.DataFrame(d1)   # now there is a df for each stimulus with onset and duration of poke
df2= pd.DataFrame(d2)

# extract first 10 min (600000 ms)
duration= 600000
df1_10min= df1[(df1.onsets1 <= duration)]
df2_10min= df2[(df2.onsets2 <= duration)]

# get odor preferences every 30 secs
bins= np.arange(0,(duration)+30000, 30000)
investigation_time_poke1=[]
investigation_time_poke2=[]
odor_preference_index=[0]   # place 0 at the beginning 
for b in range(0,bins.size-1):
    partial_time_poke1= df1_10min.pokes1times[(df1_10min.onsets1 < bins[b+1])].sum()
    partial_time_poke2= df2_10min.pokes2times[(df2_10min.onsets2 < bins[b+1])].sum()
    partial_odor_indices= (partial_time_poke1 - partial_time_poke2)/(partial_time_poke1 + partial_time_poke2)
    investigation_time_poke1=np.append(investigation_time_poke1, partial_time_poke1)
    investigation_time_poke2=np.append(investigation_time_poke2, partial_time_poke2)
    odor_preference_index= np.append(odor_preference_index, partial_odor_indices)

# plotting 
x_timeline= np.arange(0,(duration/1000)+30,30)

fig= go.Figure()
fig.add_trace(go.Scatter(x=x_timeline, y=odor_preference_index, mode='lines', line_color='red', showlegend=False))
fig.update_xaxes(title_text='Time (s)', showgrid=False, showline=True, linecolor='black', linewidth=1, range=[0,600],
                 tickmode='linear', tick0=0, dtick=30)
fig.update_yaxes(range=[-1,1], showgrid=False, showline=True, linecolor='black', linewidth=1,
                 zeroline=True, zerolinecolor='black', zerolinewidth=1)
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
#fig.show()

os.chdir(plot_dir)
fig.write_image(figure_name)