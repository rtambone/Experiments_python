import os 
from scipy.io import loadmat
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio 
p

# setup and load data 
dir= r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\SocRecog\Data'
plot_dir= r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\SocRecog\Plots'
os.chdir(dir)
os.chdir(dir + '\\1M\\12.05.20')    # 
data= loadmat('1m_post-test.mat', simplify_cells=True)  #
figure_name= '4M\post_test.svg' #

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

# latency to first investigation
latency_stim1= df1_10min.onsets1[0]
latency_stim2= df2_10min.onsets2[0]

# ratio of investigation duration (familiar/novel)
total_investigation_time_pokes1= df1_10min['pokes1times'].sum()
total_investigation_time_pokes2= df2_10min['pokes2times'].sum()

ratio_investigation= total_investigation_time_pokes2/total_investigation_time_pokes1

# recognition index (new/(new+familiar))
recognition_index= total_investigation_time_pokes1/(total_investigation_time_pokes1 + total_investigation_time_pokes2)

# plotting 
x_plots= ['Novel','Familiar']
fig=make_subplots(rows=2, cols=2)

fig.add_trace(go.Bar(x=x_plots, y=[total_investigation_time_pokes1/1000,total_investigation_time_pokes2/1000], marker_color='blue', showlegend=False),
                    row=1,col=1)
fig.update_xaxes(showgrid=False, row=1, col=1)
fig.update_yaxes(title='Total investigation duration (s)', title_font_size=14, title_standoff=0, row=1,col=1)

fig.add_trace(go.Bar(x=x_plots, y=[latency_stim1, latency_stim2], marker_color='blue', showlegend=False),
                    row=1,col=2)
fig.update_xaxes(showgrid=False, row=1, col=2)
fig.update_yaxes(title='Latency to first investigation (ms)', title_font_size=14, title_standoff=0, row=1,col=2)

fig.add_trace(go.Bar(x=[''], y=[ratio_investigation], marker_color='blue', showlegend=False), row=2,col=1)
fig.add_shape(type='rect', xref='x', yref='y', x0= -0.5, x1=0.5, y0=0, y1= 1,fillcolor='grey', opacity=0.3, row=2, col=1) 
fig.update_xaxes(showgrid=False, row=2,col=1)
fig.update_yaxes(title='Ratio of investigation duration', title_font_size=14,title_standoff=0, range=[0,2], row=2,col=1)

fig.add_trace(go.Bar(x=[''], y=[recognition_index], marker_color='blue', showlegend=False), row=2, col=2)
fig.add_shape(type='rect', xref='x', yref='y', x0= -0.5, x1=0.5, y0=0.5, y1= 1, fillcolor='grey', opacity=0.3, row=2, col=2) 
fig.update_xaxes(showgrid=False, row=2, col=2)
fig.update_yaxes(title='Recognition index',title_font_size=14,title_standoff=0, range=[0,1],row=2,col=2)

fig.update_layout(title= dict(x=0.5,y=0.95, text='mouse 1'),
                              margin=dict(l=50,r=50,t=60,b=45),
                              plot_bgcolor='rgba(0,0,0,0)', width=1000)
fig.update_xaxes(showline=True, linecolor='black', linewidth=1)
fig.update_yaxes(showline=True, linecolor='black', linewidth=1)
fig.show()

os.chdir(plot_dir)
fig.write_image(figure_name)

#using matplotlib
import matplotlib.pyplot as plt
%matplotlib qt5

fig, ax= plt.subplots(nrows=2,ncols=2)
