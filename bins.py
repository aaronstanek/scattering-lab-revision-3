import quick_csv as qcsv

def channel_index(indata,channel):
    # indata is loaded from csv file
    # channel is int
    # we want to know which column has the data for channel
    for i in range(len(indata[0])):
        if int(indata[0][i]) == channel:
            return i
    raise Exception("The specified files does not contain data for channel "+str(channel))

def get_channel_min_max(indata,index):
    # indata[1] is the first row of data
    # indata[1][index] is the first value that we will consider
    small = indata[1][index]
    big = indata[1][index]
    for i in range(2,len(indata)): # i=0 is a header, i=1 was just considered above
        v = indata[i][index]
        if v < small:
            small = v
        elif v > big:
            big = v
    ou = dict()
    ou["min"] = small
    ou["max"] = big
    return ou

def get_bin_width(mm,bin_count):
    # mm is the minimum and maximum values in the channel
    # mm is dict (string->float), output of get_channel_min_max
    # creates new entry in mm
    # this represents the width of each bin
    mm["width"] ( mm["max"] - mm["min"] ) / float(bin_count)

def put_in_bin(value,mm,bin_count):
    n = ( value - mm["min"] ) / mm["width"]
    n = int(n) # we need to use this as an index of a list, this also rounds down
    if n >= bin_count: # if we are looking at the largest point in the dataset, this condition is True
        n = bin_count - 1
    return n # this is which bin we should put it in

def single_channel_counting_array(mm,bin_count):
    ou = []
    for i in range(bin_count):
        ou.append(0)
    return ou

def single_channel_sort(indata,index,mm,bin_count):
    ou = single_channel_counting_array(mm,bin_count)
    for i in range(1,len(indata)): # iterate over all events
        b = put_in_bin(indata[i][index],mm,bin_count)
        # b is which bin we should put this value in
        ou[b] += 1
    return ou

def single_channel_format(sorted,channel,bin_count,mm):
    ou = []
    ou.append(["BINS",1,channel,bin_count,mm["min"],mm["max"]])
    for x in sorted:
        ou.append([x])
    return ou

def single_channel_bins(infile,outfile,channel,bin_count):
    # infile and outfile are the source and destination files (strings)
    # channel is int
    # bin_count is int
    indata = qcsv.from_file(infile)
    index = channel_index(indata,channel)
    mm = get_channel_min_max(indata,index)
    get_bin_width(mm,bin_count)
    sorted = single_channel_sort(indata,index,mm,bin_count)
    ou = single_channel_format(sorted,channel,bin_count,mm)
    qcsv.to_file(outfile,ou)
