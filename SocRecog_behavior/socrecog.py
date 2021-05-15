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
os.chdir(dir + '\\4M\\12.12.20')    # 
data= loadmat('4m_post-test.mat', simplify_cells=True)  #
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

# re-processing
timeline= np.zeros(duration, dtype= np.int8)
for i in range(0,df1_10min['onsets1'].size):
    starting= df1_10min.onsets1[i]
    lasting= df1_10min.pokes1times[i]
    timeline[int(starting):int(starting+lasting)]=1
for i in range(0,df2_10min['onsets2'].size):
    starting= df2_10min.onsets2[i]
    lasting= df2_10min.pokes2times[i]
    timeline[int(starting):int(starting+lasting)]=-1

# analysis 
total_pokes1= df1_10min.onsets1.size
total_pokes2= df2_10min.onsets2.size
total_investigation_time_pokes1= df1_10min['pokes1times'].sum()
total_investigation_time_pokes2= df2_10min['pokes2times'].sum()

odor_preference_index= (total_investigation_time_pokes1 - total_investigation_time_pokes2)/(total_investigation_time_pokes1 + total_investigation_time_pokes2)

mean_investigation_timexpoke1= df1_10min['pokes1times'].mean()
std_investigation_timexpoke1= df1_10min['pokes1times'].std()
mean_investigation_timexpoke2= df2_10min['pokes2times'].mean()
std_investigation_timexpoke2= df2_10min['pokes2times'].std()

# plotting 
x_timeline= np.arange(0,timeline.size/1000,0.001)
x_plots= ['Odor 1','Odor 2']
max= max(mean_investigation_timexpoke1,mean_investigation_timexpoke2)+100
min= min(mean_investigation_timexpoke1,mean_investigation_timexpoke2)-100

fig=make_subplots(rows=2, cols=3,specs=[[{'colspan':3},None,None],
                                        [{},{},{}]],
                  horizontal_spacing=0.1, vertical_spacing=0.2,
                  row_heights=[0.4,0.6])

fig.add_trace(go.Scatter(x=x_timeline, y=timeline, mode='lines', line_color='red', showlegend=False),
                        row=1,col=1)
fig.update_xaxes(title_text='Time (s)', showgrid=False, row=1, col=1)
fig.update_yaxes(tickmode='array',tickvals=[-1,0,1], ticktext=['Odor 2', '','Odor 1'], showgrid=False, row=1,col=1)

fig.add_trace(go.Bar(x=x_plots, y=[total_pokes1,total_pokes2], marker_color='blue', showlegend=False),
                    row=2,col=1)
fig.update_xaxes(showgrid=False, row=2, col=1)
fig.update_yaxes(title='Total number of pokes', title_font_size=10, title_standoff=0, row=2,col=1)

fig.add_trace(go.Bar(x=x_plots, y=[total_investigation_time_pokes1/1000,total_investigation_time_pokes2/1000], marker_color='blue', showlegend=False),
                    row=2,col=2)
fig.update_xaxes(showgrid=False, row=2,col=2)
fig.update_yaxes(title='Total time spent per odor (s)', title_font_size=10,title_standoff=0, row=2,col=2)

fig.add_trace(go.Scatter(x=x_plots, y=[mean_investigation_timexpoke1,mean_investigation_timexpoke2], mode='lines',
                         error_y=dict(type='sqrt', array=[std_investigation_timexpoke1/total_pokes1,std_investigation_timexpoke2/total_pokes2]),
                         line_color='blue', showlegend=False),
                         row=2,col=3)
fig.update_xaxes(showgrid=False, row=2, col=3)
fig.update_yaxes(title='Mean investigation time per odor (ms)',title_font_size=10,title_standoff=0,  
                 range=[min,max],row=2,col=3)

fig.update_layout(title= dict(x=0.5,y=0.95, text='Odor Preferece Index='+str(round(odor_preference_index,2))),
                              margin=dict(l=60,r=60,t=12,b=45),
                              plot_bgcolor='rgba(0,0,0,0)')
fig.update_xaxes(showline=True, linecolor='black', linewidth=1)
fig.update_yaxes(showline=True, linecolor='black', linewidth=1)
#fig.show()

os.chdir(plot_dir)
fig.write_image(figure_name)

#using matplotlib
%matplotlib qt5
plt.plot(x_timeline, timeline)