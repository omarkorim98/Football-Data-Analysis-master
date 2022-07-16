def data_maxframe(df):
  df_max_frame=df['frame']
  max_frame=df_max_frame.max()
  return max_frame

def first_frame(df):
    first_value = df['frame'].iat[0]
    return first_value

def data_df(df):
  #adjust data 
  #Get the data again and apply coordinates operation to adjust players position
  df.set_index(['frame','ID'],inplace=True)
  df['X']=df['X'].apply(lambda x: ((x/10)*105/100)-11 if(x>500) else (x/10)*105/100)
  df['Y']=df['Y'].apply(lambda y: (y/10)*100/68)
  df2 = df.drop(columns=['Class', 'Color','Position'])
  return df2

def data_dfplayers(df):
  # Using one color of each unqiue ID 
  dfPlayers=df.groupby('ID').first() 
  return dfPlayers
