from .data_checks import change_triple_sort, triple_to_vals


def process_gfe(gfe_df):

    gfe_df['upper_seis_depth'] = gfe_df.apply(upper_seis_depth, axis=1)
    gfe_df['lower_seis_depth'] = gfe_df.apply(lower_seis_depth, axis=1)
    gfe_df['strike_slip_rate'] = gfe_df.apply(process_ss_rate, axis=1)

    return gfe_df


def process_ss_rate(row):
    if row.slip_type is not None:
        if 'Sinistral' in row.slip_type:
            if row.ns_strike_slip_rate is not None:
                vals = triple_to_vals(row.ns_strike_slip_rate)
                new_vals = []
                new_tup = '({},{},{})'
                for val in vals:
                    try:
                        val = float(val) * -1
                    except ValueError:
                        val = val
                    new_vals.append(val)
                new_tup.format(*new_vals)
                return new_tup
            else:
                return None
        else:
            return row['ns_strike_slip_rate']
    else:
        return row['ns_strike_slip_rate']


def upper_seis_depth(row):
    if row['ns_upper_sm_depth'] is not None:
        sm = row['ns_upper_sm_depth']
    elif row['fs_upper_sm_depth'] is not None:
        sm = row['fs_upper_sm_depth']
    else:
        sm = None

    if sm is not None:
        sm = change_triple_sort(sm)

    return sm


def lower_seis_depth(row):
    if row['ns_lower_sm_depth'] is not None:
        sm = row['ns_lower_sm_depth']
    elif row['fs_lower_sm_depth'] is not None:
        sm = row['fs_lower_sm_depth']
    else:
        sm = None

    if sm is not None:
        sm = change_triple_sort(sm)

    return sm
