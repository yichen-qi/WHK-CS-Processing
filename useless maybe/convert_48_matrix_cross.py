import pandas as pd
import os
import numpy as np

data_folder_48 = 'data_excel_48'

input = []
output_u_l = []
output_u_r = []
output_l_l = []
output_l_r = []


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

        matrix_u_l = matrix.iloc[:3, :4].values.reshape(-1)
        matrix_u_r = matrix.iloc[:3, 4:].values.reshape(-1)
        matrix_l_l = matrix.iloc[3:, :4].values.reshape(-1)
        matrix_l_r = matrix.iloc[3:, 4:].values.reshape(-1)

        input.append(valid_input)
        output_u_l.append(matrix_u_l)
        output_u_r.append(matrix_u_r)
        output_l_l.append(matrix_l_l)
        output_l_r.append(matrix_l_r)

inputs = np.array(input)
outputs_u_l = np.array(output_u_l)
outputs_u_r = np.array(output_u_r)
outputs_l_l = np.array(output_l_l)
outputs_l_r = np.array(output_l_r)

save_folder_path = 'train_data_matrix_cross_npy'
np.save(os.path.join(save_folder_path, 'inputs_48_cross.npy'), inputs)
np.save(os.path.join(save_folder_path, 'outputs_u_l.npy'), outputs_u_l)
np.save(os.path.join(save_folder_path, 'outputs_u_r.npy'), outputs_u_r)
np.save(os.path.join(save_folder_path, 'outputs_l_l.npy'), outputs_l_l)
np.save(os.path.join(save_folder_path, 'outputs_l_r.npy'), outputs_l_r)
        