import pandas as pd
import numpy as np

from matplotlib import pyplot as plt

from data_statistics.threat_Potential import threat_values 
from drawing.draw_pitch import draw_pitch


def offset_df(df, dx, dy):
    df = df.copy()
    df.x = df.x+dx
    df.y = df.y+dy  
    return df

def create_multipoints(df):
  xTvalues= threat_values.import_xtvalues()
  dfxT = df.from_records(xTvalues).unstack().reset_index()
  dfxT.columns = ['x', 'y', 'xT']

  #dfxT2= df.from_records(xTvalues).unstack().reset_index()
  #dfxT2.columns = ['x', 'y', 'xT']


  dfxT = pd.concat([offset_df(dfxT, dx, dy)
                    for dx, dy
                    in [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75)]
                  ])
  '''
  dfxT2= pd.concat([offset_df(dfxT2, dx, dy)
                    for dx, dy
                    in [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75)]
                  ])
  '''
  ny, nx = xTvalues.shape

  dfxT.x = dfxT.x*100/nx
  dfxT.y = dfxT.y*100/ny

  #only consider locations with better than median threat (i.e. ignore defensive positions)
  dfxT.xT = np.clip(dfxT.xT-dfxT.xT.median(), 0, 1)

  #flip axis if necessary (to align with attacking team)
  #dfxT.x = 100-dfxT.x
  #dfxT.y = 100-dfxT.y

  fig, ax = draw_pitch()

  #plotting pitch with probability
  rgba_colors = np.zeros((dfxT.shape[0],4))
  #rgba_colors = np.zeros((dfxT2.shape[0],4))
  rgba_colors[:,0] = 1.0
  rgba_colors[:,3] = dfxT.xT.values/dfxT.xT.max()
  #rgba_colors[:,3] = dfxT2.xT.values/dfxT2.xT.max()
  plt.scatter(dfxT['x'], dfxT['y'], c=rgba_colors)
  #plt.savefig('output/threat points.png')
  #plt.scatter(dfxT2['x'], dfxT2['y'], c=rgba_colors)
  
  return dfxT,rgba_colors
