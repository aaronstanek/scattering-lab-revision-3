import quick_csv as qcsv
import bins

def merge_min_max(a,b):
    ou = dict()
    ou["min"] = min(a["min"],b["min"])
    ou["max"] = max(a["max"],b["max"])
    return ou

def channel_in_common(infile,channel):
    ou = dict()
    ou["indata"] = qcsv.from_file(infile)
    ou["index"] = bins.channel_index(ou["indata"],channel)
    ou["mm"] = bins.get_channel_min_max(ou["indata"],ou["index"])
    return ou

def single_channel_sort_wrapper(d,mm,bin_count):
    return bins.single_channel_sort(d["indata"],d["index"],mm,bin_count)

def single_channel_find_factor(source_s,background_s):
    is_set = False
    source_cutoff = max(source_s) / 10.0
    background_cutoff = max(background_s) / 10.0
    for i in range(len(source_s)):
        # source_s and background_s were produced at the same time so we can guarantee that they have then same length
        # we need to filter away bins with a small number of hits because their uncertainty is too large
        if source_s[i] < source_cutoff:
            continue
        if background_s[i] < background_cutoff:
            continue
        if is_set == False:
            f = background_s[i] / source_s[i]
            is_set = True
        else:
            v = background_s[i] / source_s[i]
            # f is the maximum squish factor needed to make background_s fit inside source_s
            # if v > f we need to update f
            if v > f:
                f = v
    if is_set == False:
        # this means that the datasets are disjoint-ish
        return -1
    else:
        return f

def single_channel_do_subtraction(source_s,background_s,factor):
    if factor == -1:
        return source_s
    ou = []
    for i in range(len(source_s)):
        p = source_s[i] - ( background_s[i] / factor )
        if p < 0:
            p = 0
        ou.append(p)
    return ou

def single_channel_background_subtract(source_s,background_s):
    factor = single_channel_find_factor(source_s,background_s)
    sorted = single_channel_do_subtraction(source_s,background_s,factor)
    return sorted

def single_channel_background_bins(source_infile,background_infile,outfile,channel,bin_count):
    # this is meant to mirror bins.single_channel_bins
    # source_infile, background_infile are string refering to exisitng csv files
    # outfile is a string refering to a nonexistent csv file
    # channel is an inter refering to a channel
    # bin_count is an int inicating how many bins to make
    source_d = channel_in_common(source_infile,channel)
    background_d = channel_in_common(background_infile,channel)
    mm = merge_min_max(source_d["mm"],background_d["mm"])
    bins.get_bin_width(mm,bin_count)
    source_s = single_channel_sort_wrapper(source_d,mm,bin_count)
    background_s = single_channel_sort_wrapper(background_d,mm,bin_count)
    # source_s and background_s are now lists of floats
    # we want to make a single list from this, opposed to how single_channel_bins does it
    sorted = single_channel_background_subtract(source_s,background_s)
    ou = bins.single_channel_format(sorted,channel,bin_count,mm)
    qcsv.to_file(outfile,ou)
