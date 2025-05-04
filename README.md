# 📊 Data Converter Tool

A user-friendly **PyQt6 GUI** application for converting `.txt` files into **Excel spreadsheets** and generating `.npy` datasets for machine learning — including **training**, **testing**, and **validation** sets.

---

## 🧭 Table of Contents

- [✨ Features](#-features)
- [🗂️ Folder Structure](#️-folder-structure)
- [⚙️ Requirements](#️-requirements)
- [🚀 Getting Started](#-getting-started)
- [📝 Notes](#-notes)
- [📄 License](#-license)

---

## ✨ Features

### 🔄 TXT to Excel Conversion
- 🔍 Extracts parameters from filenames:  
  **Temperature (`T`)**, **Amplitude (`A`)**, **Young's Modulus (`YM`)**
- 🧹 Cleans, averages, and organizes data into `.xlsx` format
  The focus is on **converting the 192 nodes** in the cross-section of the solder joint strain distribution **into 48 elemental areas**,
  each of which takes the **mean** of the **coordinates and plastic strain values** on the 4 nodes.
- 📂 Supports **batch processing** of multiple `.txt` files

### 📁 Dataset Generation
- Converts Excel files into **NumPy `.npy` arrays**:
  - `inputs.npy` – input features  
  - `outputs.npy` – target values  
  - `co_ind.npy` – coordinate info (for training data only)
- 📦 Supports **train**, **test**, and **validation** folder generation

---

## 🗂️ Folder Structure

```text
project/
├── APPp.py
├── data_txt
├── data_excel
├── traindata_npy/
│   ├── inputs.npy
│   ├── outputs.npy
│   └── co_ind.npy
├── testdata_npy/
│   ├── inputs.npy
│   └── outputs.npy
└── valdata_npy/
    ├── inputs.npy
    └── outputs.npy
```

You can customize the save paths by editing the output directory selection in the GUI.  
To manually change the **default output path** in code, look for lines like:

```python
output_path = os.path.join(current_dir, 'traindata_npy')
```

Replace 'traindata_npy' with your desired directory, or expose this as a user input in the GUI.

---

## ⚙️ Requirements

```bash
Python 3.12
pip install pyqt6 pandas numpy openpyxl
```

---

## 🚀 Getting Started

1. Place your `.txt` files in the `data_txt/` folder.

2. Run the app:

  ```bash
  git clone https://github.com/yichen-qi/WHK-CS-Processing.git your_projectfolder_name
  cd your_projectfolder_name
  python APPp.py
  ```
3. Use the GUI to:
   
  ✅ Convert .txt files to .xlsx in data_excel/

  ✅ Generate .npy datasets into traindata_npy/, testdata_npy/, and valdata_npy/

---

## 📝 Notes

- 📄 Each `.txt` file must follow a naming format like: `T85_A0.5_YM65.txt`
- 🧮 The program groups every **4 nodes** into **1 element**, converting **192 nodes → 48 elements**
- 📌 `co_ind.npy` (coordinate data) is generated **only for training data**

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).



