def automation():
#   from google.colab import drive
#   drive.mount('/content/drive')

  #----------------------------------------------------------------------------------------------------#
  #-------------------------------Import necessary libraries-------------------------------------------#
  #----------------------------------------------------------------------------------------------------#
  import pandas as pd
  import datetime as dt
  from datetime import date
  import numpy as np
  import os
  import glob

  #----------------------------------------------------------------------------------------------------#
  #-----------------------Function to retrieve data from API-------------------------------------------#
  #----------------------------------------------------------------------------------------------------#
  def get_from_oecd(query):
      if "?" in query:
          return pd.read_csv(
              f"{query}&format=csv"
          )
      else:
          return pd.read_csv(
              f"{query}?format=csv"
          )

  #----------------------------------------------------------------------------------------------------#
  #-----------------------Access to file in drive------------------------------------------------------#
  #----------------------------------------------------------------------------------------------------#
  # Get current working directory
  #path = os.getcwd()

  # Change working directory
  #os.chdir("/content/drive/Shareddrives/General/Trainee Folders/Tuan Phan/Full data/full-data-update-schedule")

  # Show all file in directory
  #files = os.listdir(path)

  #read Relevant_variables excel file
  #df = pd.read_excel('Relevant_variables.xlsx') 
  df = pd.read_csv("https://raw.githubusercontent.com/TuanPhanDB/actions-test/main/Relevant_variables.csv")

  #----------------------------------------------------------------------------------------------------#
  #-----------------------Create dataframe-------------------------------------------------------------#
  #----------------------------------------------------------------------------------------------------#
  new_header = df.iloc[2].tolist() #grab the fourth row for the header
  df = df[3:208] #take the data from fifth row
  df.columns = new_header #set the header row as the df header

  #----------------------------------------------------------------------------------------------------#
  #-----------------------Fossil df function-----------------------------------------------------------#
  #----------------------------------------------------------------------------------------------------#
  def fossil_df(df):
    #create fossil fuel support dataframe
    fossil_df = df[156:]

    #create data range for fossil df
    end = date.today()
    end_year = end.year
    fossil_full = pd.DataFrame(data=[i for i in range(2010, end_year)], columns=['TIME_PERIOD'])

    #go through every dataset
    for i in range(len(fossil_df)):
      cur_data = fossil_df.iloc[i].copy()

      #get data from API column
      data = get_from_oecd(cur_data[6])

      #drop rows that have NaN in 'OBS_VALUE'
      data = data.dropna(subset=['OBS_VALUE'])

      #go through every row in current dataset
      for i in range(len(data)):
        cur_row = data.iloc[i]

        #create new column's name for fossil_full
        name = '['+ cur_data[0] + ']' + '[' + cur_row['STAGE'] + ']' +  '[' + cur_row['FUEL_CAT'] + ']'
        if name not in fossil_full.columns:
          fossil_full[name] = ''

        #fill data into cell that have correspond 'TIME_PERIOD'
        num_mask = (fossil_full['TIME_PERIOD'] == cur_row['TIME_PERIOD'])

        fossil_full.loc[num_mask, name] = cur_row['OBS_VALUE']

    return fossil_full

  #----------------------------------------------------------------------------------------------------#
  #-----------------------Relevant df functione--------------------------------------------------------#
  #----------------------------------------------------------------------------------------------------#
  def relevant_df(df):
    #create relevant df
    relevant_df = df[:156]

    #create time range from 01-2010 - now
    end = date.today()
    range_date = pd.date_range(start ='1/2010', end=end, freq ='M')

    #format date to yyyy-mm
    range_date = range_date.to_period('M')

   #create final dataframe with range_date
    relevant_data = pd.DataFrame(data=range_date, columns=['TIME_PERIOD'])

    for i in range(len(relevant_df)):
      cur = relevant_df.iloc[i].copy()
      if cur[5] == 'OECD':
        data = get_from_oecd(cur[6])

        #go through every row in current dataset
        for i in range(len(data)):
          cur_row = data.iloc[i]

          #remove blank part in name when measure or Unit/Transformation/Adjustment is empty
          if pd.isnull(cur[1]) and pd.isnull(cur[3]):
            name = cur[0]
          elif pd.isnull(cur[3]) and not pd.isnull(cur[1]):
            name = cur[0] + '[' + cur[1] + ']'
          elif pd.isnull(cur[1]) and not pd.isnull(cur[3]):
            name = cur[0] + '[' + cur[3] + ']'
          else:
            name = cur[0] + '[' + cur[1] + ']' +  '[' + cur[3] + ']'

          if name not in relevant_data.columns:
            relevant_data[name] = ''

          num_mask = (relevant_data['TIME_PERIOD'] == cur_row['TIME_PERIOD'])

          relevant_data.loc[num_mask, name] = cur_row['OBS_VALUE']

    return relevant_data

  #----------------------------------------------------------------------------------------------------#
  #-----------------------Update and export data-------------------------------------------------------#
  #----------------------------------------------------------------------------------------------------#
  def update():
    #fossil data
    fossil_fuel_support = fossil_df(df)
    # Result
    file_name = 'fossil_full.xlsx'
    fossil_fuel_support.to_excel(file_name)
    print('fossil done')

    #relevant data
    relevant_OECD = relevant_df(df)
     # Result
    file_name = 'relevant_full.xlsx'
    relevant_OECD.to_excel(file_name)
    print('relevant done')

  update()


#install()
automation()