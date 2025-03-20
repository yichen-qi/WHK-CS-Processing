import pandas as pd
import os
import re
import numpy as np

def custom_float_conversion(value):
    """
    Convert a string representation of a number where:
    - ',' is the decimal point
    - '.' is the thousands separator
    """
    try:
        return float(value.replace(',', '.'))
    except ValueError:
        return None  # Handle cases where conversion fails

txt_folder = 'data_txt'
excel_folder = 'data_excel_48'

os.makedirs(excel_folder, exist_ok=True)

for file_name in os.listdir(txt_folder):
    if file_name.endswith('.txt'):
        file_path = os.path.join(txt_folder, file_name)

        try:
            data = pd.read_csv(file_path, delimiter='\t')
        except Exception as e:
            print(f'Error reading {file_path}: {e}')
            continue

        data_converted = data.applymap(lambda x: custom_float_conversion(x) if isinstance(x, str) else x)
        del data_converted[data.columns[3]]

        file_name_do = file_name.replace(',', '.')
        matches = re.findall(r'T(-?\d+\.?\d*)|A(-?\d+\.?\d*)|YM(-?\d+\.?\d*)', file_name_do)
        numbers = [float(num) for match in matches for num in match if num]
        insert_data = np.tile(numbers, (192, 1))
        for i in range(insert_data.shape[1]):
            data_converted.insert(i, f'NewColumn{i+1}', insert_data[:, i])

        out_file_name = f"{os.path.splitext(file_name)[0]}.xlsx"
        out_file_path = os.path.join(excel_folder, out_file_name)
        

        df_do = data_converted.iloc[:, [5,6,7,8]] 
        df_do_mean = df_do.groupby(df_do.columns[-2], as_index=False).mean()
        original_columns = df_do.columns  
        df_do_mean = df_do_mean[original_columns]

        df_3 = data_converted.iloc[:,[0,1,2]]
        df_3.drop(range(48,192),axis=0,inplace=True)

        data_48 = pd.concat([df_3, df_do_mean], axis=1)
        del data_48[data.columns[5]] 

        try:
            data_48.to_excel(out_file_path, index=False, header=False)
            print(f'Wrote {out_file_path}')
        except Exception as e:
            print(f'Error writing {out_file_path}: {e}')
            













