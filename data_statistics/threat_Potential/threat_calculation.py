from matplotlib import pyplot as plt

import numpy as np

from shapely.geometry import Polygon, MultiPoint
from shapely.ops import cascaded_union

from data_statistics import voronoi_fig
from data_statistics.threat_Potential.threat_values import create_multipoints
from data_statistics import voronoi_polygons

fig, ax, dfFrame, polygons=voronoi_polygons.draw_voronoi(t=1) 

X_SIZE = 105.0
Y_SIZE = 68.0
SCALERS = np.array([X_SIZE/100, Y_SIZE/100])
pitch = Polygon(((0,0), (0,100), (100,100), (100,0)))
    
def area_values(dfxT,dfPlayers):
  points = MultiPoint(list(zip(dfxT['x'], dfxT['y'])))
  dfValues = dfxT.set_index(['x', 'y'])
  player_values = {}
  attack_polygon = cascaded_union([polygon for player,polygon in polygons.items() if dfPlayers.loc[player]['Position']=='Attack'])
  values = [dfValues.loc[p.x,p.y].values[0] for p in attack_polygon.intersection(points)]
  area_value = np.mean(values)*attack_polygon.area
  return points,dfValues,player_values,attack_polygon,values,area_value

def calculate_value(df, dfPlayers, t, max_frame,dfxT,first_frame):
    points,dfValues,player_values,attack_polygon,values,area_value = area_values(dfxT,dfPlayers)
    if t == 0:
       t=1
    f = int(t*6)
    if f > max_frame :
       f=max_frame
    else:
       f=f
    dfFrame = df.loc[f]

    vor, dfVor = voronoi_fig.calculate_voronoi(dfFrame, dfPlayers)
    polygons = {}
    for index, region in enumerate(vor.regions):
        if not -1 in region:
            if len(region)>0:
                try:
                    pl = dfVor[dfVor['region']==index]
                    polygon = Polygon([vor.vertices[i] for i in region]/SCALERS).intersection(pitch)
                    polygons[pl.index[0]] = polygon
                except IndexError:
                    pass
                except AttributeError:
                    pass
    
    attack_polygon = cascaded_union([polygon for player,polygon in polygons.items() if dfPlayers.loc[player]['Position']=='Attack'])
    values = [dfValues.loc[p.x,p.y].values[0] for p in attack_polygon.intersection(points)]
    area_value = np.mean(values)*attack_polygon.area
    return area_value

def Threat_evolution(df,dfPlayers,max_frame,dfxT,first_frame): 
  points,dfValues,player_values,attack_polygon,values,area_value = area_values(dfxT,dfPlayers)
  values = [calculate_value(df, dfPlayers, t=t, max_frame=max_frame,dfxT=dfxT,first_frame=first_frame) for t in range(int(max_frame/first_frame))]
  plt.figure()
  plt.style.use('ggplot')
  plt.plot(values, )

  highlights = [16,32,48 ]

  for h in highlights:
      plt.axvline(h, c='blue')
 
  plt.xlabel('Time (s)')
  plt.xticks(np.arange(0, 100,10))
  plt.ylabel('Threat Potential')
  plt.savefig('output/threat chart.png')
  return highlights,values