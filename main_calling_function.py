import pandas as pd

df= pd.read_csv('input_data/calma_df_mapped_final.csv')

'''
Now funcition is waiting you to send the data to save it in input data folder
'''
def all_statistics(df):
   df=df
   df.to_csv('input_data/finaldata32.csv') 
   '''
   !!!Can not import without saving data :(
   '''
   from video_creation.create_video import video_creation, video_voronoi_creation
   from data_statistics.threat_Potential import threat_image     
   #video_creation()
   #video_voronoi_creation()
   threat_image.display_threat(df)
   
all_statistics(df)


