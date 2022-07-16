import json
from matplotlib import pyplot as plt
import numpy as np 
import pandas as pd
from drawing import draw_pitch

def import_xtvalues():
    with open('input_data/open_xt_12x8_v1.json', 'r') as f:
     xTvalues = np.array(json.load(f))
    return xTvalues

def offset_df(df, dx, dy):
    df = df.copy()
    df.x = df.x+dx
    df.y = df.y+dy  
    return df

def create_multipoints(df):
  dfxT = df.from_records(import_xtvalues()).unstack().reset_index()
  dfxT.columns = ['x', 'y', 'xT']

  dfxT2= df.from_records(import_xtvalues()).unstack().reset_index()
  dfxT2.columns = ['x', 'y', 'xT']

  dfxT = pd.concat([offset_df(dfxT, dx, dy)
                    for dx, dy
                    in [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75)]
                  ])
  dfxT2= pd.concat([offset_df(dfxT2, dx, dy)
                    for dx, dy
                    in [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75)]
                  ])

  ny, nx = import_xtvalues().shape

  dfxT.x = dfxT.x*100/nx
  dfxT.y = dfxT.y*100/ny

  #only consider locations with better than median threat (i.e. ignore defensive positions)
  dfxT.xT = np.clip(dfxT.xT-dfxT.xT.median(), 0, 1)

  #flip axis if necessary (to align with attacking team)
  dfxT2.x = 100-dfxT.x
  dfxT2.y = 100-dfxT.y

  fig, ax = draw_pitch()

  #plotting pitch with probability
  rgba_colors = np.zeros((dfxT.shape[0],4))
  rgba_colors = np.zeros((dfxT2.shape[0],4))
  rgba_colors[:,0] = 1.0
  rgba_colors[:,3] = dfxT.xT.values/dfxT.xT.max()
  rgba_colors[:,3] = dfxT2.xT.values/dfxT2.xT.max()
  plt.scatter(dfxT['x'], dfxT['y'], c=rgba_colors)
  plt.scatter(dfxT2['x'], dfxT2['y'], c=rgba_colors)
  
  return fig,dfxT,rgba_colors
