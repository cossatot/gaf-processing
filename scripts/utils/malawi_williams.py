from ast import literal_eval as leval
import numpy as np
import pandas as pd

tup_str = '({},{},{})'

def process_malawi_williams(malawi_df: pd.DataFrame):
    mdf = malawi_df[['geometry', 'References', 'Dip_Dir', 'FaultNotes', 
        'SMSSD ID', 'Fault_Name']]

    mdf['slip_type'] = 'Normal'
    mdf['net_slip_rate'] = malawi_df.apply(get_malawi_slip_rate_row, axis=1)
    mdf['average_dip']= malawi_df.apply(get_malawi_dip_row, axis=1)
    
    return mdf


def get_malawi_slip_rate_row(row):
    return tup_str.format(row.Sec_SR_M, row.Sec_SR_L, row.Sec_SR_U)

def get_malawi_dip_row(row):
    return tup_str.format(row.Dip_M, row.Dip_L, row.Dip_U)