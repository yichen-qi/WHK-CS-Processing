import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

filepath = r'C:\Users\Admin\Desktop\WHK CS processing\data_excel_192\T1,5 A0,2 YM20.xlsx'
filepath2 = r'C:\Users\Admin\Desktop\WHK CS processing\data_excel_48\T1,5 A0,2 YM20.xlsx'
pos_file = r'C:\Users\Admin\Desktop\WHK CS processing\traindata_npy\coordinate_index_48.npy'
pos = np.load(pos_file)

x_min, x_max = pos[:,0].min()-0.06, pos[:,0].max()+0.1
z_min, z_max = pos[:,1].min()-0.06, pos[:,1].max()+0.04

#-------------strain distribution by nodes--------------
df = pd.read_excel(filepath, header=None)

df_do = df.iloc[:, 3:] 


x = df_do.iloc[:, 0]
z = df_do.iloc[:, 1]
values = df_do.iloc[:, 2]

vmin, vmax = values.values.min(), values.values.max()

plt.figure(figsize=(9, 6))
sc = plt.scatter(x, z, c=values, cmap='rainbow', vmin=vmin, vmax=vmax)


color_bar = plt.colorbar(sc)
color_bar.set_label('Value')  

plt.xlim(x_min, x_max)
plt.ylim(z_min, z_max)
plt.title('XZ Plane Strain Distribution with 192 nodes')
plt.xlabel('X')
plt.ylabel('Z')

plt.show()


#--------------strain distribution by elments-------------
df = pd.read_excel(filepath2, header=None)
df_do2 = df.iloc[:, 3:] 


x = df_do2.iloc[:, 0]
z = df_do2.iloc[:, 1]
values = df_do2.iloc[:, 2]


plt.figure(figsize=(9, 6))
sc = plt.scatter(x, z, c=values, cmap='rainbow')


color_bar = plt.colorbar(sc)
color_bar.set_label('Value')  

plt.xlim(x_min, x_max)
plt.ylim(z_min, z_max)
plt.title('XZ Plane Strain Distribution with 48 areas')
plt.xlabel('X')
plt.ylabel('Z')

plt.show()


# ---------------------------24-area strain distribution by nodes-
df = pd.read_excel(filepath2, header=None)

df_48 = df.iloc[:, 5] 


pos = np.load(pos_file)

df_pos = pd.DataFrame(pos)

ind = df_pos.sort_values(by=[1, 0], ascending=[False, True]).index

matrix_values = df_48.iloc[ind].values.reshape(6, 8)

matrix_x = df_pos.iloc[ind, 0].values.reshape(6, 8)
matrix_z = df_pos.iloc[ind, 1].values.reshape(6, 8)

matrix_values_avg = (matrix_values[::2, :] + matrix_values[1::2, :]) / 2
matrix_x_avg = (matrix_x[::2, :] + matrix_x[1::2, :]) / 2
matrix_z_avg = (matrix_z[::2, :] + matrix_z[1::2, :]) / 2

x = matrix_x_avg.reshape(-1)
z = matrix_z_avg.reshape(-1)
values = matrix_values_avg.reshape(-1)


plt.figure(figsize=(9, 6))
sc = plt.scatter(x, z, c=values, cmap='rainbow')


color_bar = plt.colorbar(sc)
color_bar.set_label('Value')  

plt.xlim(x_min, x_max)
plt.ylim(z_min, z_max)

plt.title('XZ Plane Strain Distribution with 24 areas')
plt.xlabel('X')
plt.ylabel('Z')

plt.show()


# ---------------------------12-area strain distribution by nodes-

df = pd.read_excel(filepath2, header=None)

df_48 = df.iloc[:, 5] 


pos = np.load(pos_file)

df_pos = pd.DataFrame(pos)

ind = df_pos.sort_values(by=[1, 0], ascending=[False, True]).index

matrix_values = df_48.iloc[ind].values.reshape(6, 8)

matrix_x = df_pos.iloc[ind, 0].values.reshape(6, 8)
matrix_z = df_pos.iloc[ind, 1].values.reshape(6, 8)

matrix_values_3x8 = (matrix_values[::2, :] + matrix_values[1::2, :]) / 2
matrix_x_3x8 = (matrix_x[::2, :] + matrix_x[1::2, :]) / 2
matrix_z_3x8 = (matrix_z[::2, :] + matrix_z[1::2, :]) / 2

matrix_values_3x4 = (matrix_values_3x8[:, 0::2] + matrix_values_3x8[:, 1::2]) / 2
matrix_x_3x4 = (matrix_x_3x8[:, 0::2] + matrix_x_3x8[:, 1::2]) / 2
matrix_z_3x4 = (matrix_z_3x8[:, 0::2] + matrix_z_3x8[:, 1::2]) / 2


x = matrix_x_3x4.reshape(-1)
z = matrix_z_3x4.reshape(-1)
values = matrix_values_3x4.reshape(-1)


plt.figure(figsize=(9, 6))
sc = plt.scatter(x, z, c=values, cmap='rainbow')


color_bar = plt.colorbar(sc)
color_bar.set_label('Value')  

plt.xlim(x_min, x_max)
plt.ylim(z_min, z_max)

plt.title('XZ Plane Strain Distribution with 12 areas')
plt.xlabel('X')
plt.ylabel('Z')

plt.show()


# ---------------------------4-area strain distribution by nodes-
df = pd.read_excel(filepath2, header=None)

df_48 = df.iloc[:, 5] 


pos = np.load(pos_file)

df_pos = pd.DataFrame(pos)

ind = df_pos.sort_values(by=[1, 0], ascending=[False, True]).index

matrix_values = df_48.iloc[ind].values.reshape(6, 8)

matrix_x = df_pos.iloc[ind, 0].values.reshape(6, 8)
matrix_z = df_pos.iloc[ind, 1].values.reshape(6, 8)


matrix_values_2x8 = matrix_values.reshape(2, 3, 8).mean(axis=1)
matrix_x_2x8 = matrix_x.reshape(2, 3, 8).mean(axis=1)
matrix_z_2x8 = matrix_z.reshape(2, 3, 8).mean(axis=1)

matrix_values_2x2 = matrix_values_2x8.reshape(2, 2, 4).mean(axis=2)
matrix_x_2x2 = matrix_x_2x8.reshape(2, 2, 4).mean(axis=2)
matrix_z_2x2 = matrix_z_2x8.reshape(2, 2, 4).mean(axis=2)



x = matrix_x_2x2.reshape(-1)
z = matrix_z_2x2.reshape(-1)
values = matrix_values_2x2.reshape(-1)


plt.figure(figsize=(9, 6))
sc = plt.scatter(x, z, c=values, cmap='rainbow')


color_bar = plt.colorbar(sc)
color_bar.set_label('Value')  

plt.xlim(x_min, x_max)
plt.ylim(z_min, z_max)

plt.title('XZ Plane Strain Distribution with 4 areas')
plt.xlabel('X')
plt.ylabel('Z')

plt.show()