''' import required libraries'''
''' if running from ipyhton, please cd into the folder with downloaded files containing network.db etc.'''

import numpy as np; import pandas as pd; import sqlite3 as sql

conn = sql.connect('network.db')

df1 = pd.read_sql_query('select * from bus', conn)
df2 = pd.read_sql_query('select * from branch', conn)
df2.set_index('branch', inplace=True)

'''if power flow was previously calculated, omit the stored results'''
if 'power flow' in df2:
    df2.drop(columns='power flow', inplace=True)

bus_data = df1.to_numpy(dtype='int'); branch_data = df2.to_numpy(dtype='int')
net_power = bus_data[:,1] - bus_data[:,2]

'''create empty B matrix, which has NxN dimension'''
b_matrix = np.zeros((np.shape(bus_data)[0],np.shape(bus_data)[0]))

'''create an empty incidence matrix, which has MxN dimension'''
incidence = np.zeros((np.shape(branch_data)[0],np.shape(bus_data)[0]))

'''create eye matrix, with MxM, which is used to form D matrix according to the attached literature'''
diagonal_B = np.eye(np.shape(branch_data)[0])

'''calculate B matrix, incidence matrix, and D matrix'''
for i in range(np.shape(branch_data)[0]):
    b_matrix[branch_data[i][0]-1][branch_data[i][0]-1] -= branch_data[i][2]
    b_matrix[branch_data[i][1]-1][branch_data[i][1]-1] -= branch_data[i][2]
    b_matrix[branch_data[i][0]-1][branch_data[i][1]-1] += branch_data[i][2]
    b_matrix[branch_data[i][1]-1][branch_data[i][0]-1] += branch_data[i][2]

    for j in range(np.shape(bus_data)[0]):
        if branch_data[i][0] == bus_data[j][0]:
            incidence[i][j] = 1
        if branch_data[i][1] == bus_data[j][0]:
            incidence[i][j] = -1

    diagonal_B[i][i] *= -branch_data[i][2]

b_modded=np.delete(b_matrix,0,0); b_modded=np.delete(b_modded,0,1)
net_power_modded = np.delete(net_power,0,0)
b_modded_inverted = np.linalg.inv(b_modded)
angles = b_modded_inverted.dot(net_power_modded)
angles_full = np.append(0,angles)

power_flow = diagonal_B.dot(incidence.dot(angles_full))

df2['power flow'] = power_flow.tolist()

df2.to_sql('branch', conn, if_exists = 'replace')
conn.close()