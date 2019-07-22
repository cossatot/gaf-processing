from ast import literal_eval as leval
import re

import numpy as np


def process_usgs_hazfaults(usgs_df):
    """
    Processes the USGS HazFaults 2014 dataset for merging with master_df
    """

    usgs_df = usgs_df[usgs_df['primary_st'] != 'California']

    preprocess_rakes(usgs_df)

    usgs_df['average_rake'] = usgs_df.apply(process_rake, axis=1)
    usgs_df['dip_dir'] = usgs_df.apply(process_dip_dir, axis=1)

    usgs_df['average_dip'] = usgs_df.apply(process_dip, axis=1)
    usgs_df['slip_type'] = usgs_df.apply(process_slip_type, axis=1)
    usgs_df['net_slip_rate'] = usgs_df.apply(process_slip_rate, axis=1)

    return usgs_df


def process_dip(row):
    return '({},,)'.format(int(row['dip']))


def process_dip_dir(row):
    if row['dip_dir'] not in (None, '', 'V'):
        return row['dip_dir']
    else:
        return None


def preprocess_rakes(df):
    df.loc[df['geo_slip_r'] == 0., 'geo_rake'] = None
    df.loc[df['bird_slip_'] == 0., 'bird_rake'] = None
    df.loc[df['zeng_slip_'] == 0., 'zeng_rake'] = None


def process_slip_rate(row):
    rate_list = row[['geo_slip_r', 'bird_slip_', 'zeng_slip_']].tolist()
    rate_list = sorted(rate_list)

    return '({},{},{})'.format(rate_list[1], rate_list[0], rate_list[2])


def process_rake(row):
    rake_list = row[['geo_rake', 'bird_rake', 'zeng_rake']].tolist()
    rake_list = sorted((r for r in rake_list if not np.isnan(r)))

    if len(rake_list) == 2:
        rake_list = [round(np.mean(rake_list)), rake_list[1], rake_list[0]]
    elif len(rake_list) == 1:
        rake_list = ['', rake_list[0], '']

    rake_tup = '({},{},{})'.format(rake_list[1], rake_list[0], rake_list[2])

    return rake_tup


def process_slip_type(row):
    rake_to_kin = {
        180.: 'Dextral',
        -90.: 'Normal',
        0.: 'Sinistral',
        90.: 'Reverse'
    }

    try:
        slip_type = rake_to_kin[row['geo_rake']]
    except KeyError:
        if row['disp_slip_'] == 'normal':
            slip_type = 'Normal'
        elif row['disp_slip_'] == 'thrust':
            slip_type = 'Reverse'

    return slip_type
