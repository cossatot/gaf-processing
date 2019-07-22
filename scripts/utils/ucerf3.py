import numpy as np
import pandas as pd


def process_ucerf3(ucf_df):
    ucf_df['net_slip_rate'] = ucf_df.apply(ucerf_slip_rate_parse, axis=1)
    ucf_df['average_dip'] = ucf_df.apply(parse_dip, axis=1)
    ucf_df['average_rake'] = ucf_df.apply(parse_rake, axis=1)
    ucf_df['lower_seis_depth'] = ucf_df.apply(parse_lower_seis_depth, axis=1)
    ucf_df['upper_seis_depth'] = ucf_df.apply(parse_upper_seis_depth, axis=1)
    ucf_df['slip_type'] = ucf_df.apply(parse_style, axis=1)

    return ucf_df


def ucerf_slip_rate_parse(row):
    return '({},{},{})'.format(np.round(row.slip_rate_mean * 1000, 2),
                               np.round(row.slip_rate_min * 1000, 2),
                               np.round(row.slip_rate_max * 1000, 2))


def parse_dip(row):
    if row['Dip'] not in ('', None):
        return '({},,)'.format(row['Dip'])
    else:
        return None


def parse_rake(row):
    if row['Rake'] not in ('', None):
        return '({},,)'.format(row['Rake'])


def parse_upper_seis_depth(row):
    if row['Upper Seis Depth'] not in ('', None):
        return '({},,)'.format(row['Upper Seis Depth'])


def parse_lower_seis_depth(row):
    if row['Lower Seis Depth'] not in ('', None):
        return '({},,)'.format(row['Lower Seis Depth'])


def parse_style(row):
    conv_d = {
        'N': 'Normal',
        'N-RL': 'Normal-Dextral',
        'R-LL': 'Reverse-Sinistral',
        'R': 'Reverse',
        'RL-N': 'Dextral-Normal',
        'RL': 'Dextral',
        'R-RL': 'Reverse-Dextral',
        'LL': 'Sinistral',
        'LL-R': 'Sinistral-Reverse',
        'RL-R': 'Dextral-Reverse',
        None: None,
        'RL-R?': 'Dextral-Reverse',
        '?': None,
        'RL?': 'Dextral',
        'N-RL?': 'Normal-Dextral',
        'N - RL': 'Normal-Dextral',
        'LL?': 'Sinistral',
        'R-RL?': 'Reverse-Dextral',
        'R?': 'Reverse',
        'N?': 'Reverse'
    }

    return conv_d[row['style']]
