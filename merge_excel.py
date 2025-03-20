import os
import pandas as pd
import numpy as np

folder_path = 'data_excel_192'  
output_file = '0106merged_file_48.xlsx'  

dataframes = []

for file_name in os.listdir(folder_path):
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(folder_path, file_name)
        
        df = pd.read_excel(file_path, header=None)

        df_do = df.iloc[:, [5,6,7,8]] 
        df_do_mean = df_do.groupby(df_do.columns[-2], as_index=False).mean()
        original_columns = df_do.columns  
        df_do_mean = df_do_mean[original_columns]
        df_do_mean.insert(0, 4, np.arange(48))
        df_3 = df.iloc[:,[0,1,2]]
        df_3.drop(range(48,192),axis=0,inplace=True)
        result = pd.concat([df_3, df_do_mean], axis=1)  
                
        dataframes.append(result)

merged_df = pd.concat(dataframes, ignore_index=True)

merged_df.to_excel(output_file, index=False)

print(f"Merged file saved as {output_file}")
