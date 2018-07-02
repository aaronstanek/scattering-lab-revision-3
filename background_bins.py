import quick_csv as qcsv
import bins

def merge_min_max(a,b):
    ou = dict()
    ou["min"] = min(a["min"],b["min"])
    ou["max"] = max(a["max"],b["max"])
    return ou

def get_single_channel_sum(scs):
    ou = 0
    for x in scs:
        ou += x
    return ou

def scale_single_channel_sum(scs,scale):
    ou = []
    for x in scs:
        ou.append(x*scale)
    return ou

def merge_single_channel_sums(source,background):
    source_count = get_single_channel_sum(source)
    background_count = get_single_channel_sum(background)
    source_normalized = scale_single_channel_sum(source,1.0/float(source_count))
    background_normalized = scale_single_channel_sum(background,1.0/float(backgorund_count))
    ou_scaled = []
    for i in range(len(source_normalized)):
        ou_scaled.append(source_normalized[i] - background_normalized[i])
    # the sum of ou_scaled could be anywhere from 0 to 2, we want to put it back to the sacle of source
    # 0 means they are identical, our math is useless
    ou_scaled_count = get_single_channel_sum(ou_scaled)
    if ou_scaled_count == 0:
        raise Exception("cannot do background subtraction, source data and background data are identical")
    ou = scale_single_channel_sum(ou_scaled,float(source_count)/float(ou_scaled_count))
    return ou

def single_channel_background_bins(source_infile,background_infile,outfile,channel,bin_count):
    # functions similarly to bins.single_channel_bins
    # source_infile, background_infile are strings refering to existing files
    # outfile is a string refering to a nonexistent file
    # channel (int) indicates which channel to bin
    # bin_count (int) indicates how many bins to make
    source_indata = qcsv.from_file(source_indata)
    background_indata = qcsv.from_file(background_infile)
    source_index = bins.channel_index(source_indata,channel)
    background_index = bins.channel_index(background_indata,channel)
    source_mm = bins.get_channel_min_max(source_indata,source_index)
    background_mm = bins.get_channel_min_max(background_indata,background_index)
    mm = merge_min_max(source_mm,background_mm)
    source_sorted = bins.single_channel_sort(source_indata,source_index,mm,bin_count)
    background_sorted = bins.single_channel_sort(background_indata,background_index,mm,bin_count)
    sorted = merge_single_channel_sums(source_sorted,background_sorted)
    ou = bins.single_channel_format(sorted,channel,bin_count,mm)
    qcsv.to_file(outfile,ou)
