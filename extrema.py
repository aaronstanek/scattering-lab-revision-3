import quick_csv as qcsv
import bins

class format_error(Exception):
    def __init__(self):
        super().__init__("Input file does not have the expected format.")

def binnum_to_value(binnum,mm):
    return mm["min"] + ((float(binnum) + 0.5) * mm["width"])

def single_channel_confirm_format(indata):
    if len(indata) < 1:
        raise format_error
    if len(indata[0]) != 6:
        raise format_error
    if indata[0][0] != "BINS":
        raise format_error
    if indata[0][1] != "1":
        raise format_error

def single_channel_get_mm(indata):
    ou = dict()
    ou["bins"] = int(indata[0][3])
    ou["min"] = float(indata[0][4])
    ou["max"] = float(indata[0][5])
    bins.get_bin_width(ou,ou["bins"])
    return ou

def single_channel_extrema(indata,first_bin,last_bin):
    big_b = first_bin
    big = float(indata[first_bin+1][0])
    small_b = big_b
    small = big
    for i in range(first_bin,last_bin+1):
        v = float(indata[i+1][0])
        if v > big:
            big_b = i
            big = v
        if v < small:
            small_b = i
            small = v
    ou = dict()
    ou["max_x_bin"] = big_b
    ou["max_value"] = big
    ou["min_x_bin"] = small_b
    ou["min_value"] = small
    return ou

def single_channel_format(ex):
    ou = []
    ou.append(["MAX"])
    ou.append(["X",ex["max_x"]])
    ou.append(["VALUE",ex["max_value"]])
    ou.append(["MIN"])
    ou.append(["X",ex["min_x"]])
    ou.append(["VALUE",ex["min_value"]])
    return ou

def single_channel(infile,outfile,**args):
    # infile is a string that refers to an existing csv file in the BINS format
    # outfile is a string that refers to a file
    # args may optionally contain min and max
    # these are floats that can be used to narrow the search space
    indata = qcsv.from_file(infile)
    single_channel_confirm_format(indata)
    mm = single_channel_get_mm(indata)
    if "min" in args:
        first_bin = bins.put_in_bin(args["min"],mm,mm["bins"])
    else:
        first_bin = 0
    if "max" in args:
        last_bin = bins.put_in_bin(args["max"],mm,mm["bins"])
    else:
        last_bin = mm["bins"] - 1
    ex = single_channel_extrema(indata,first_bin,last_bin)
    ex["max_x"] = binnum_to_value(ex["max_x_bin"],mm)
    ex["min_x"] = binnum_to_value(ex["min_x_bin"],mm)
    ou = single_channel_format(ex)
    qcsv.to_file(outfile,ou)
