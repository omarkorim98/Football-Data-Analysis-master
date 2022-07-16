import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.spatial import Voronoi
from shapely.geometry import Polygon
import drawing.draw_threat_frame as draw_threat_frame
import adjust_data.clean_data as clean_data

X_SIZE = 105.0
Y_SIZE = 68.0
SCALERS = np.array([X_SIZE/100, Y_SIZE/100])

def calculate_voronoi(dfFrame, dfPlayers):
    
    dfTemp = dfFrame.copy().drop(0, errors='ignore').join(dfPlayers, rsuffix='_dup')

    values = np.vstack((dfTemp[['X', 'Y']].values*SCALERS,
                        [-1000,-1000],
                        [+1000,+1000],
                        [+1000,-1000],
                        [-1000,+1000]
                       ))

    vor = Voronoi(values)

    dfTemp['region'] = vor.point_region[:-4]
    
    return vor, dfTemp

pitch = Polygon(((0,0), (0,100), (100,100), (100,0)))

def draw_voronoi(t):
    
    df= pd.read_csv('input_data/finaldata32.csv')
    dfPlayers=clean_data.data_dfplayers(df)
    
    fig, ax, dfFrame = draw_threat_frame.draw_frame(t)
    vor, dfVor = calculate_voronoi(dfFrame, dfPlayers)
    polygons = {}
    for index, region in enumerate(vor.regions):
        if not -1 in region:
            if len(region)>0:
                try:
                    pl = dfVor[dfVor['region']==index]
                    polygon = Polygon([vor.vertices[i] for i in region]/SCALERS).intersection(pitch)
                    color = pl['Color'].values[0]
                    x, y = polygon.exterior.xy
                    plt.fill(x, y, c=color, alpha=0.30)
                    polygons[pl.index[0]] = polygon
                except IndexError:
                    pass
                except AttributeError:
                    pass

        plt.scatter(dfVor['X'], dfVor['Y'], c=dfVor['Color'], alpha=0.2)
    return fig, ax, dfFrame, polygons
