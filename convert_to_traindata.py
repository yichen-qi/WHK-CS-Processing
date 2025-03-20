import pandas as pd
import os
import numpy as np


class Convert_traindata:

    def __init__(self, data_folder):
        self.data_folder = data_folder

    
    
    def con_td(self):
        input = []
        output = []

        for filename in os.listdir(self.data_folder):
            if filename.endswith('.xlsx'):
                file_path = os.path.join(self.data_folder, filename)

                df = pd.read_excel(file_path, header=None)

                valid_input = df.iloc[0, :3].values
                valid_output = df.iloc[:, -1].values

                co_ind = df.iloc[:, [3,4]].values

                input.append(valid_input)
                output.append(valid_output)


        inputs = np.array(input)
        outputs = np.array(output)
        co_ind = np.array(co_ind)

        return inputs, outputs, co_ind


data_folder_48 = 'data_excel_48'
data_folder_192 = 'data_excel_192'

ct_48 = Convert_traindata(data_folder_48)
ct_192 = Convert_traindata(data_folder_192)

inputs_48, outputs_48, co_ind_48 = ct_48.con_td()
inputs_192, outputs_192, co_ind_192 = ct_192.con_td()


save_folder_path = 'traindata_npy'
np.save(os.path.join(save_folder_path, 'inputs_48.npy'), inputs_48)
np.save(os.path.join(save_folder_path, 'outputs_48.npy'), outputs_48)

# np.save(os.path.join(save_folder_path, 'inputs_192.npy'), inputs_192)
# np.save(os.path.join(save_folder_path, 'outputs_192.npy'), outputs_192)

np.save(os.path.join(save_folder_path, 'coordinate_index_48.npy'), co_ind_48)
# np.save(os.path.join(save_folder_path, 'coordinate_index_192.npy'), co_ind_192)


