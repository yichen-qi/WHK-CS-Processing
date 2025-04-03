import sys
import os
import re
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog, 
                             QVBoxLayout, QLabel, QTabWidget, QHBoxLayout, QGroupBox)


def custom_float_conversion(value):
    """ 处理字符串中的浮点数 """
    try:
        return float(value.replace(',', '.'))
    except ValueError:
        return None
    


class Convert_data_npy:

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


class DataConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Data Convert Tool')
        self.setGeometry(100, 100, 600, 400)

        # 创建 TabWidget（选项卡）
        self.tabs = QTabWidget()  # 创建一个选项卡控件
        self.tab_txt_excel = QWidget()  # 创建“TXT to Excel”页面
        self.tab_train_data = QWidget()  # 创建“Train Data”页面
        self.tab_test_data = QWidget()  # 创建“Test Data”页面
        self.tab_val_data = QWidget()  # 创建“Validation Data”页面

        # 添加选项卡
        self.tabs.addTab(self.tab_txt_excel, "TXT to Excel") # 添加“TXT to Excel”标签页
        self.tabs.addTab(self.tab_train_data, "Train Data")
        self.tabs.addTab(self.tab_test_data, "Test Data")
        self.tabs.addTab(self.tab_val_data, "Validation Data")

        # 初始化各个界面
        self.init_txt_excel_tab() # 初始化 "TXT to Excel" 界面
        self.init_train_data_tab()
        self.init_test_data_tab()
        self.init_val_data_tab()

        # 创建主窗口的垂直布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs) # 将选项卡控件添加到主布局
        self.setLayout(main_layout) # 设置窗口的主布局

    def init_txt_excel_tab(self):
        """ 初始化 TXT to Excel 界面 """
        layout = QVBoxLayout()
        group_box = QGroupBox("TXT to Excel") # 创建一个分组框（带标题）

        self.txt_label = QLabel("Please select the TXT folder")
        self.txt_button = QPushButton("Select TXT folder")
        self.txt_button.clicked.connect(self.select_folder_txt)

        self.excel_label = QLabel("Please select the Excel output folder")
        self.excel_button = QPushButton("Select Excel output folder")
        self.excel_button.clicked.connect(self.select_output_folder)

        self.convert_button = QPushButton("Start conversion")
        self.convert_button.clicked.connect(self.convert_txt_to_excel)

        self.status_label = QLabel("Waiting for operation...")

        # 布局
        vbox = QVBoxLayout()
        vbox.addWidget(self.txt_label)
        vbox.addWidget(self.txt_button)
        vbox.addWidget(self.excel_label)
        vbox.addWidget(self.excel_button)
        vbox.addWidget(self.convert_button)
        vbox.addWidget(self.status_label)

        group_box.setLayout(vbox)
        layout.addWidget(group_box) # 把分组框添加到选项卡布局
        self.tab_txt_excel.setLayout(layout) # 设置当前选项卡的布局

        # 变量
        self.txt_folder = None
        self.excel_folder = None

    def init_train_data_tab(self):
        """ 初始化 Train Data 界面 """
        layout = QVBoxLayout()
        group_box = QGroupBox("generate training set")

        self.train_label = QLabel("please select the Excel file")
        self.train_button = QPushButton("Select Excel folder")
        self.train_button.clicked.connect(self.select_folder_train)

        self.train_convert_button = QPushButton("generate training set")
        self.train_convert_button.clicked.connect(self.convert_train_data)

        self.train_status_label = QLabel("Waiting for operation...")

        # 布局
        vbox = QVBoxLayout()
        vbox.addWidget(self.train_label)
        vbox.addWidget(self.train_button)
        vbox.addWidget(self.train_convert_button)
        vbox.addWidget(self.train_status_label)

        group_box.setLayout(vbox)
        layout.addWidget(group_box)
        self.tab_train_data.setLayout(layout)

        # 变量
        self.train_folder = None

    def init_test_data_tab(self):
        """ 初始化 Test Data 界面 """
        layout = QVBoxLayout()
        group_box = QGroupBox("generate test set")

        self.test_label = QLabel("please select the Excel file")
        self.test_button = QPushButton("Select Excel folder")
        self.test_button.clicked.connect(self.select_folder_test)

        self.test_convert_button = QPushButton("generate test set")
        self.test_convert_button.clicked.connect(self.convert_test_data)

        self.test_status_label = QLabel("waiting for operation...")

        # 布局
        vbox = QVBoxLayout()
        vbox.addWidget(self.test_label)
        vbox.addWidget(self.test_button)
        vbox.addWidget(self.test_convert_button)
        vbox.addWidget(self.test_status_label)

        group_box.setLayout(vbox)
        layout.addWidget(group_box)
        self.tab_test_data.setLayout(layout)

        # 变量
        self.test_folder = None


    def init_val_data_tab(self):
        """ 初始化 Validation Data 界面 """
        layout = QVBoxLayout()
        group_box = QGroupBox("generate validation set")

        self.val_label = QLabel("please select the Excel file")
        self.val_button = QPushButton("Select Excel folder")
        self.val_button.clicked.connect(self.select_folder_val)

        self.val_convert_button = QPushButton("generate validation set")
        self.val_convert_button.clicked.connect(self.convert_val_data)

        self.val_status_label = QLabel("waiting for operation...")

        # 布局
        vbox = QVBoxLayout()
        vbox.addWidget(self.val_label)
        vbox.addWidget(self.val_button)
        vbox.addWidget(self.val_convert_button)
        vbox.addWidget(self.val_status_label)

        group_box.setLayout(vbox)
        layout.addWidget(group_box)
        self.tab_val_data.setLayout(layout)

        # 变量
        self.val_folder = None



    def select_folder_txt(self):
        """ 选择 TXT 文件夹 """
        folder = QFileDialog.getExistingDirectory(self, 'Select TXT data folder')
        if folder:
            self.txt_folder = folder
            self.txt_label.setText(f'Selected: {folder}')

    def select_output_folder(self):
        """ 选择 Excel 保存文件夹 """
        folder = QFileDialog.getExistingDirectory(self, 'Select Excel output folder')
        if folder:
            self.excel_folder = folder
            self.excel_label.setText(f'Output folder: {folder}')

    def convert_txt_to_excel(self):
        """ TXT → Excel 转换功能 """
        if not self.txt_folder or not self.excel_folder:
            self.status_label.setText("please select both TXT and Excel folders first")
            return

        # 模拟转换逻辑（你可以在这里加上具体转换代码）
        for file_name in os.listdir(self.txt_folder):
            if file_name.endswith('.txt'):
                file_path = os.path.join(self.txt_folder, file_name)
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
                out_file_path = os.path.join(self.excel_folder, out_file_name)

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
        self.status_label.setText(f"TXT data converted to Excel in {self.excel_folder}")

    def select_folder_train(self):
        """ 选择用于训练集的 Excel 目录 """
        folder = QFileDialog.getExistingDirectory(self, 'select training data folder')
        if folder:
            self.train_folder = folder
            self.train_label.setText(f'selected: {folder}')

    def convert_train_data(self):
        """ 生成训练集 """
        if not self.train_folder:
            self.train_status_label.setText("please select training data folder first")
            return
        
        save_folder = 'traindata_npy'
        os.makedirs(save_folder, exist_ok=True)

        converter = Convert_data_npy(self.train_folder)
        inputs, outputs, co_ind = converter.con_td()

        np.save(os.path.join(save_folder, 'inputs.npy'), inputs)
        np.save(os.path.join(save_folder, 'outputs.npy'), outputs)
        np.save(os.path.join(save_folder, 'co_ind.npy'), co_ind)

        self.train_status_label.setText(f"training data generated: {save_folder}")

    def select_folder_test(self):
        """ 选择用于测试集的 Excel 目录 """
        folder = QFileDialog.getExistingDirectory(self, 'select test data folder')
        if folder:
            self.test_folder = folder
            self.test_label.setText(f'selected: {folder}')

    def convert_test_data(self):
        """ 生成测试集 """
        if not self.test_folder:
            self.test_status_label.setText("please select test data folder first")
            return
        
        save_folder = 'testdata_npy'
        os.makedirs(save_folder, exist_ok=True)

        converter = Convert_data_npy(self.test_folder)
        inputs, outputs, _ = converter.con_td()

        np.save(os.path.join(save_folder, 'inputs.npy'), inputs)
        np.save(os.path.join(save_folder, 'outputs.npy'), outputs)
        

        self.test_status_label.setText(f"test data generated: {save_folder}")

    
    def select_folder_val(self):
        """ 选择用于验证集的 Excel 目录 """
        folder = QFileDialog.getExistingDirectory(self, 'select validation data folder')
        if folder:
            self.val_folder = folder
            self.val_label.setText(f'selected: {folder}')

    def convert_val_data(self):
        """ 生成验证集 """
        if not self.val_folder:
            self.val_status_label.setText("please select validation data folder first")
            return
        
        save_folder = 'valdata_npy'
        os.makedirs(save_folder, exist_ok=True)

        converter = Convert_data_npy(self.val_folder)
        inputs, outputs, _ = converter.con_td()

        np.save(os.path.join(save_folder, 'inputs.npy'), inputs)
        np.save(os.path.join(save_folder, 'outputs.npy'), outputs)
        

        self.val_status_label.setText(f"validation data generated: {save_folder}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataConverterApp()
    window.show()
    sys.exit(app.exec())
