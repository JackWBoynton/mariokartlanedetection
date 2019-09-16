import pandas as pd
import glob
from tqdm import tqdm
from multiprocessing import Pool

def load_df(filename):
    asset = 'XBTU19'
    data = pd.read_csv(filename, header=None, low_memory=False, dtype={3: float}, usecols=[0, 1, 3], skiprows=2)

    for n, i in enumerate(data[1]):
        if i == asset:
            data = pd.DataFrame(data.values[n:])
            break

    for n, j in enumerate(data[1]):
        if j != asset:
            data = pd.DataFrame(data.values[:n])
            break
    #del data[0]

    del data[1]
    #print(data.head())
    return data


def load_dfs(asset, files):
    frm = files[0].split('/')[1].split('.')[0]
    too = files[-1].split('/')[1].split('.')[0]
    print('backtest dates: ' + frm + '-' + too)
    if 1 == 1 or not glob.glob('../../loaded'+frm+too+'.csv'):
        a = []
        first = True
        for i in tqdm(files):
            data = load_df(filename=i)
            if not first:
                a = pd.concat([a, data], ignore_index=True)
            else:
                first = False
                a = data

        a.to_csv(path_or_buf='../../loaded'+frm+too+'.csv', header=False)
    else:
        a = pd.read_csv('../../loaded'+frm+too+'.csv', header=None, low_memory=False, dtype={1: float}, usecols=[0, 1])
    print('loaded ' + str(a.shape[0]) + ' ticks of data')
    return a


def load_dfs_mult(asset, files):
    # multiprocessing version of load_dfs
    frm = files[0].split('/')[1].split('.')[0]
    too = files[-1].split('/')[1].split('.')[0]
    print('backtest dates: ' + frm + '-' + too)
    if 1==1 or not glob.glob('../../loaded'+frm+too+'.csv'):
        with Pool(processes=8) as pool:
            df_list = (pool.map(load_df, tqdm(files)))
            combined = pd.concat(tqdm(df_list), ignore_index=True)
            combined.to_csv(path_or_buf='../../loaded'+frm+too+'.csv', header=False)
    else:
        combined = pd.read_csv('../../loaded'+frm+too+'.csv', header=None, low_memory=False, dtype={1: float}, usecols=[0, 1])
    print('loaded ' + str(combined.shape[0]) + ' ticks of data')
    print (combined.head())
    print (combined.tail())
    return combined
