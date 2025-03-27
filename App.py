import sys
import os
import re
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel


def custom_float_conversion(value):
    try:
        return float(value.replace(',', '.'))
    except ValueError:
        return None

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
    


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('data convert tool')
        self.setGeometry(100, 100, 500, 300)  # （x, y, width, height）

        layout = QVBoxLayout()

        self.label = QLabel('select txt data folder')
        layout.addWidget(self.label) #add to window

        #first button
        self.button_select_txt = QPushButton('select folder')
        self.button_select_txt.clicked.connect(self.select_folder_txt)
        layout.addWidget(self.button_select_txt)

        #second button
        self.button_convert_npy = QPushButton('convert to .npy')
        self.button_convert_npy.clicked.connect(self.convert_to_npy)
        layout.addWidget(self.button_convert_npy)

        self.setLayout(layout)
        self.data_excel_folder = None

    def select_folder_txt(self):
        folder = QFileDialog.getExistingDirectory(self, 'select txt data folder')
        if folder:
            self.label.setText(f'processing: {folder}')
            self.process_data(folder)
            self.label.setText('Txt to Excel Conversion Finished')

    def process_data(self, txt_folder):
        excel_folder = 'data_excel_48'
        os.makedirs(excel_folder, exist_ok=True)
        self.data_excel_folder = excel_folder

        for file_name in os.listdir(txt_folder):
            if file_name.endswith('.txt'):
                file_path = os.path.join(txt_folder, file_name)
                try:
                    data = pd.read_csv(file_path, delimiter='\t')
                except Exception as e:
                    print(f'read {file_path} fail: {e}')
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
                df_3.drop(range(48,192), axis=0, inplace=True)

                data_48 = pd.concat([df_3, df_do_mean], axis=1)
                del data_48[data.columns[5]] 

                try:
                    data_48.to_excel(out_file_path, index=False, header=False)
                    print(f'write already: {out_file_path}')
                except Exception as e:
                    print(f'write {out_file_path} fail: {e}')

    def convert_to_npy(self):
        if not self.data_excel_folder:
            self.label.setText('Please select and convert TXT data first!')
            return
        
        save_folder = 'traindata_npy'
        os.makedirs(save_folder, exist_ok=True)

        converter = Convert_traindata(self.data_excel_folder)
        inputs, outputs, co_ind = converter.con_td()

        np.save(os.path.join(save_folder, 'inputs.npy'), inputs)
        np.save(os.path.join(save_folder, 'outputs.npy'), outputs)
        np.save(os.path.join(save_folder, 'co_ind.npy'), co_ind)

        self.label.setText('Excel to NPY Conversion Finished')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
