import pandas as pd
import glob
from tqdm import tqdm
from multiprocessing import Pool
len_df = 0

def load_df(filename):
    asset = 'XBTUSD'
    global len_df
    assert len_df != 0
    tqdm.pandas(desc="load csvs #" + str(len_df))

    data = pd.read_csv(filename, header=None, low_memory=False, dtype={
                       3: float}, usecols=[0, 1, 3], skiprows=2, na_values=0).progress_apply(lambda x: x)
    # print(data)
    for n, i in enumerate(data[1]):
        if i == asset:
            data = pd.DataFrame(data.values[n:])
            break
    for n, j in enumerate(data[1]):
        if j != asset:
            data = pd.DataFrame(data.values[:n])
            break
    del data[1]
    len_df = len_df - 1
    return data


def load_dfs(asset, files):
    frm = files[0].split('/')[1].split('.')[0]
    too = files[-1].split('/')[1].split('.')[0]
    print('backtest dates: ' + frm + '-' + too)
    if 1 == 1 or not glob.glob('../loaded' + frm + too + '.csv'):
        a = []
        first = True
        for i in tqdm(files):
            data = load_df(filename=i)
            if not first:
                a = pd.concat([a, data], ignore_index=True)
            else:
                first = False
                a = data
        a.to_csv(path_or_buf='../loaded' + frm + too + '.csv', header=False)
    else:
        a = pd.read_csv('../loaded' + frm + too + '.csv', header=None,
                        low_memory=False, dtype={1: float}, usecols=[0, 1], skiprows=2, na_values=0)
    print('loaded ' + str(a.shape[0]) + ' ticks of data')
    return a


def load_dfs_mult(asset, files):
    # multiprocessing version of load_dfs
    for n, i in enumerate(files):
        if i.split('/')[1].split('.')[0] == '20190927':
            del files[n]  # remove wonky day's data
    frm = files[0].split('/')[1].split('.')[0]
    too = files[-1].split('/')[1].split('.')[0]

    files.reverse()
    print('backtest dates: ' + frm + '-' + too)
    global len_df
    if len_df == 0:
        len_df = len(files)
    if 1 == 1 or not glob.glob('../loaded' + frm + too + '.csv'):
        with Pool(processes=16) as pool:
            df_list = (pool.map(load_df, files))
            tqdm.pandas(desc="concat csvs")
            combined = pd.concat(df_list, ignore_index=True).progress_apply(lambda x: x) # apply dummy lambda fn to call tqdm.pandas()
            combined.to_csv(path_or_buf='../loaded' +
                            frm + too + '.csv', header=False)
    else:
        combined = pd.read_csv('../loaded' + frm + too + '.csv', header=None,
                               low_memory=False, dtype={1: float}, usecols=[0, 1], skiprows=2, na_values=0)
    print('loaded ' + str(combined.shape[0]) + ' ticks of data')
    return combined
