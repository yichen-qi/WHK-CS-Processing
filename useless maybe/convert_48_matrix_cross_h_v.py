import pandas as pd
import os
import numpy as np

class Convert48Matrix:

    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.input = []
        self.outputs = {"u_l": [], "u_r": [], "l_l": [], "l_r": [],
                        "l_h": [], "m": [], "r_h": [],
                        "l_v": [], "m_l": [], "m_r": [], "r_v": []}

    def split_matrix(self, matrix, mode):
        if mode == "cross":
            return [matrix.iloc[:3, :4].values.reshape(-1),
                    matrix.iloc[:3, 4:].values.reshape(-1),
                    matrix.iloc[3:, :4].values.reshape(-1),
                    matrix.iloc[3:, 4:].values.reshape(-1)]
        elif mode == "horizontal":
            return [matrix.iloc[:2, :].values.reshape(-1),
                    matrix.iloc[2:4, :].values.reshape(-1),
                    matrix.iloc[4:, :].values.reshape(-1)]
        elif mode == "vertical":
            return [matrix.iloc[:, :2].values.reshape(-1),
                    matrix.iloc[:, 2:4].values.reshape(-1),
                    matrix.iloc[:, 4:6].values.reshape(-1),
                    matrix.iloc[:, 6:].values.reshape(-1)]

    def append_outputs(self, mode, values):
        if mode == "cross":
            keys = ["u_l", "u_r", "l_l", "l_r"]
        elif mode == "horizontal":
            keys = ["l_h", "m", "r_h"]
        elif mode == "vertical":
            keys = ["l_v", "m_l", "m_r", "r_v"]
        for key, value in zip(keys, values):
            self.outputs[key].append(value)

    def convert_matrix(self):
        for filename in os.listdir(self.data_folder):
            if filename.endswith('.xlsx'):
                file_path = os.path.join(self.data_folder, filename)
                df = pd.read_excel(file_path, header=None)

                self.input.append(df.iloc[0, :3].values)

                valid_output = df.iloc[:, -1]
                co_ind = df.iloc[:, [3, 4]]
                ind = co_ind.sort_values(by=[co_ind.columns[1], co_ind.columns[0]], ascending=[False, True]).index
                matrix = valid_output.iloc[ind].values.reshape(6, 8)
                matrix = pd.DataFrame(matrix)

                self.append_outputs("cross", self.split_matrix(matrix, "cross"))
                self.append_outputs("horizontal", self.split_matrix(matrix, "horizontal"))
                self.append_outputs("vertical", self.split_matrix(matrix, "vertical"))

        inputs = np.array(self.input)
        outputs = {key: np.array(value) for key, value in self.outputs.items()}
        return inputs, outputs

    def save_data(self, inputs, outputs, folder_paths):
        np.save(os.path.join(folder_paths["inputs"], 'inputs.npy'), inputs)
        for key, folder in folder_paths.items():
            if key != "inputs":
                np.save(os.path.join(folder, f'outputs_{key}.npy'), outputs[key])

# Usage
data_folder = 'data_excel_48'
cm = Convert48Matrix(data_folder)
inputs, outputs = cm.convert_matrix()

# save_folder_paths = {
#     "inputs": 'train_data_matrix_cross_npy',
#     "u_l": 'train_data_matrix_cross_npy',
#     "u_r": 'train_data_matrix_cross_npy',
#     "l_l": 'train_data_matrix_cross_npy',
#     "l_r": 'train_data_matrix_cross_npy',
#     "l_h": 'train_data_matrix_h_npy',
#     "m": 'train_data_matrix_h_npy',
#     "r_h": 'train_data_matrix_h_npy',
#     "l_v": 'train_data_matrix_v_npy',
#     "m_l": 'train_data_matrix_v_npy',
#     "m_r": 'train_data_matrix_v_npy',
#     "r_v": 'train_data_matrix_v_npy'
# }

save_folder_paths = {
    "inputs": 'test_data_matrix_cross_npy',
    "u_l": 'test_data_matrix_cross_npy',
    "u_r": 'test_data_matrix_cross_npy',
    "l_l": 'test_data_matrix_cross_npy',
    "l_r": 'test_data_matrix_cross_npy',
    "l_h": 'test_data_matrix_h_npy',
    "m": 'test_data_matrix_h_npy',
    "r_h": 'test_data_matrix_h_npy',
    "l_v": 'test_data_matrix_v_npy',
    "m_l": 'test_data_matrix_v_npy',
    "m_r": 'test_data_matrix_v_npy',
    "r_v": 'test_data_matrix_v_npy'
}

cm.save_data(inputs, outputs, save_folder_paths)
