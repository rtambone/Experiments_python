import os 
from scipy.io import loadmat
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

plot_dir= r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\SocRecog\Plots'

total_pokes1= 120
total_pokes2= 76
total_investigation_time_pokes1= 66240
total_investigation_time_pokes2= 186758

odor_preference_index= (total_investigation_time_pokes1 - total_investigation_time_pokes2)/(total_investigation_time_pokes1 + total_investigation_time_pokes2)

mean_investigation_timexpoke1= total_investigation_time_pokes1/total_pokes1
mean_investigation_timexpoke2= total_investigation_time_pokes2/total_pokes2

# plotting
x_plots= ['Odor 1','Odor 2']
max= max(mean_investigation_timexpoke1,mean_investigation_timexpoke2)+100
min= min(mean_investigation_timexpoke1,mean_investigation_timexpoke2)-100

fig=make_subplots(rows=1, cols=3)

fig.add_trace(go.Bar(x=x_plots, y=[total_pokes1,total_pokes2], marker_color='blue', showlegend=False),
                    row=1,col=1)
fig.update_xaxes(showgrid=False, row=1, col=1)
fig.update_yaxes(title='Total number of pokes', title_font_size=14, title_standoff=0, row=1,col=1)

fig.add_trace(go.Bar(x=x_plots, y=[total_investigation_time_pokes1/1000,total_investigation_time_pokes2/1000], marker_color='blue', showlegend=False),
                    row=1,col=2)
fig.update_xaxes(showgrid=False, row=1,col=2)
fig.update_yaxes(title='Total time spent per odor (s)', title_font_size=14,title_standoff=0, row=1,col=2)

fig.add_trace(go.Scatter(x=x_plots, y=[mean_investigation_timexpoke1,mean_investigation_timexpoke2], mode='lines',
                         line_color='blue', showlegend=False),
                         row=1,col=3)
fig.update_xaxes(showgrid=False, row=1, col=3)
fig.update_yaxes(title='Mean investigation time per odor (ms)',title_font_size=14,title_standoff=0,  
                 range=[min,max],row=1,col=3)

fig.update_layout(title= dict(x=0.5,y=0.95, text='Odor Preferece Index='+str(round(odor_preference_index,2))),
                              margin=dict(l=50,r=50,t=60,b=45),
                              plot_bgcolor='rgba(0,0,0,0)', width=1000)
fig.update_xaxes(showline=True, linecolor='black', linewidth=1)
fig.update_yaxes(showline=True, linecolor='black', linewidth=1)
#fig.show()

os.chdir(plot_dir)
fig.write_image('4M\pre_test.svg')