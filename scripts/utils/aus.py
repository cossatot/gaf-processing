def process_aus(aus_df):

    aus_df['net_slip_rate'] = aus_df.apply(process_slip_rate, axis=1)
    aus_df['average_dip'] = aus_df.apply(process_dip, axis=1)
    aus_df['slip_type'] = aus_df.apply(infer_slip_type, axis=1)

    return aus_df


def process_dip(row):
    return '({},,)'.format(row['Dip'])


def process_slip_rate(row):

    s_min, s_max = sorted(row[['SL_RT_ST', 'SL_RT_LT']])
    s_min *= 0.001
    s_max *= 0.001
    s_mean = ((s_min + s_max) / 2)

    s_mean, s_min, s_max = [round(s, 3) for s in (s_mean, s_min, s_max)]

    if s_min == 0.:
        s_min = 0.
    return '({},{},{})'.format(s_mean, s_min, s_max)


def infer_slip_type(row):
    if row['Dip'] >= 60.:
        return 'Strike-Slip'
    else:
        return 'Reverse'
