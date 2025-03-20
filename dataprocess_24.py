import pandas as pd
import numpy as np
import os
import re

excel_folder = r'C:\Users\Admin\Desktop\WHK CS processing\data_excel_48'

os.makedirs(excel_folder, exist_ok=True)

save_folder = r'C:\Users\Admin\Desktop\WHK CS processing\data_excel_24'


for file_name in os.listdir(excel_folder):
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(excel_folder, file_name)

        try:
            data = pd.read_excel(file_path, header=None)
        except Exception as e:
            print(f'Error reading {file_path}: {e}')
            continue

        data_48 = data.iloc[:, 5] 
        df_pos = data.iloc[:, 3:5]
        df_pos.columns = [0, 1]
        ind = df_pos.sort_values(by=[1, 0], ascending=[False, True]).index

        matrix_values = data_48.iloc[ind].values.reshape(6, 8)
        matrix_x = df_pos.iloc[ind, 0].values.reshape(6, 8)
        matrix_z = df_pos.iloc[ind, 1].values.reshape(6, 8)

        matrix_values_avg = (matrix_values[::2, :] + matrix_values[1::2, :]) / 2
        matrix_x_avg = (matrix_x[::2, :] + matrix_x[1::2, :]) / 2
        matrix_z_avg = (matrix_z[::2, :] + matrix_z[1::2, :]) / 2

    

        df_avg = pd.concat([pd.DataFrame(matrix_x_avg.reshape(-1,1)), pd.DataFrame(matrix_z_avg.reshape(-1,1)), pd.DataFrame(matrix_values_avg.reshape(-1,1))], axis=1)

        file_name_do = file_name.replace(',', '.')
        matches = re.findall(r'T(-?\d+\.?\d*)|A(-?\d+\.?\d*)|YM(-?\d+\.?\d*)', file_name_do)
        numbers = [float(num) for match in matches for num in match if num]
        insert_data = np.tile(numbers, (24, 1))
        for i in range(insert_data.shape[1]):
            df_avg.insert(i, f'NewColumn{i+1}', insert_data[:, i])

        out_file_name = f"{os.path.splitext(file_name)[0]}.xlsx"
        out_file_path = os.path.join(save_folder, out_file_name)


        try:
            df_avg.to_excel(out_file_path, index=False, header=False)
            print(f'Wrote {out_file_path}')
        except Exception as e:
            print(f'Error writing {out_file_path}: {e}')

