from data_statistics import voronoi_polygons
from adjust_data import clean_data
import matplotlib.pyplot as plt
from data_statistics.threat_Potential.threat_multipoints import create_multipoints
from data_statistics.threat_Potential.threat_calculation import Threat_evolution
import pandas as pd



def display_threat(df):
  #df= pd.read_csv('input_data/finalData32.csv')
  max_frame=clean_data.data_maxframe(df)
  first_frame=clean_data.first_frame(df)
  dfPlayers=clean_data.data_dfplayers(df)
  df=clean_data.data_df(df)
  
  dfxT,rgba_colors=create_multipoints(df)
  highlights,values=Threat_evolution(df,dfPlayers,max_frame,dfxT,first_frame)
  for h in highlights:
    voronoi_polygons.draw_voronoi(h)
    plt.title('Time: {} | Threat Potential: {}'.format(h, values[int(h)]))
    plt.scatter(dfxT['x'], dfxT['y'], c=rgba_colors)
    plt.savefig(f'output/Threat potential moment{h}.png')

