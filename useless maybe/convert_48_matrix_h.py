import pandas as pd
import os
import numpy as np

data_folder_48 = 'data_excel_48'

input = []
output_l = []
output_m = []
output_r = []

for filename in os.listdir(data_folder_48):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(data_folder_48, filename)
        df = pd.read_excel(file_path, header=None)

        valid_input = df.iloc[0, :3].values

        valid_output = df.iloc[:, -1]
        valid_output = pd.DataFrame(valid_output)

        co_ind = df.iloc[:, [3,4]]

        ind = co_ind.sort_values(by=[co_ind.columns[1], co_ind.columns[0]], ascending=[False, True]).index
        matrix = valid_output[valid_output.columns[0]].iloc[ind].values.reshape(6, 8)
        matrix = pd.DataFrame(matrix)

        matrix_l = matrix.iloc[:2, :].values.reshape(-1)
        matrix_m = matrix.iloc[2:4, :].values.reshape(-1)
        matrix_r = matrix.iloc[4:, :].values.reshape(-1)

        input.append(valid_input)
        output_l.append(matrix_l)
        output_m.append(matrix_m)
        output_r.append(matrix_r)

inputs = np.array(input)
outputs_l = np.array(output_l)
outputs_m = np.array(output_m)
outputs_r = np.array(output_r)


save_folder_path = 'train_data_matrix_h_npy'
np.save(os.path.join(save_folder_path, 'inputs_48_h.npy'), inputs)
np.save(os.path.join(save_folder_path, 'outputs_l.npy'), outputs_l)
np.save(os.path.join(save_folder_path, 'outputs_m.npy'), outputs_m)
np.save(os.path.join(save_folder_path, 'outputs_r.npy'), outputs_r)
