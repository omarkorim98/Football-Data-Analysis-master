import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Ellipse

# importing movie py libraries
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
import drawing.draw_pitch as draw_pitch
import adjust_data.clean_data as clean_data

X_SIZE = 105.0
Y_SIZE = 68.0

def draw_frame(t):
    df=pd.read_csv('input_data/finaldata32.csv') 
    first_frame=clean_data.first_frame(df)
    max_frame=clean_data.data_maxframe(df)
    dfPlayers=clean_data.data_dfplayers(df)
    df=clean_data.data_df(df)   
    
    colors = {'attack': 'white',
       'defense': 'blue'}
    
    
    if t == 0:
      t= 1 
    else:
      t=t
    
    f = int(t*first_frame)
    fig, ax = draw_pitch.draw_pitch()
    
    
    if f > max_frame:
      f=max_frame

    dfFrame = df.loc[f] 
    
    for pid in dfFrame.index:
        if dfPlayers.loc[pid]['Position'] == 'Ball':
            size = 0.6
            color='black'
            edge='black'
        else:
            size = 3
            color='white'
            if dfPlayers.loc[pid]['Position'] == 'Attack':
                color= dfPlayers.loc[pid]['Color']                        
            else:
                color=color= dfPlayers.loc[pid]['Color']
                
        ax.add_artist(Ellipse((dfFrame.loc[pid]['X'],
                               dfFrame.loc[pid]['Y']),
                              size/X_SIZE*100, size/Y_SIZE*100,
                              edgecolor=color,
                              linewidth=2,
                              facecolor=color,
                              alpha=1,
                              zorder=20))
        #if display_num:
        # plt.text(dfFrame.loc[pid]['X']-1,dfFrame.loc[pid]['Y']-1.3,str(pid),fontsize=8, color='black', zorder=30)

    return fig, ax, dfFrame



