import quick_csv as qcsv
import numpy as np
import matplotlib.pyplot as plt
import extrema as ex

def sig_figs(num,sf):
    # takes a float (num) and returns it as a string with sf (int) many significant figures
    if num == 0:
        return "0.00e0"
    if num > 0:
        g = float(num)
        neg = False
    else:
        g = float(num) * (-1.0)
        neg = True
    h = 1.0
    p = 0
    while h >= g:
        h /= 10.0
        p -= 1
    while h <= g:
        h *= 10.0
        p += 1
    oul = []
    for i in range(sf):
        h /= 10.0
        y = int(g/h) % 10
        oul.append(y)
    if neg:
        ou = "-"
    else:
        ou = ""
    ou = ou + str(oul[0]) + "." + str(oul[1]) + str(oul[2]) + "e" + str(p-1)
    return ou

def set_arg_values(args):
    # takes a dict (string->string,int)
    # copys specific values from the input dict into an output dict
    # if one of those specific values is not present in the input, a default value is given to the output
    # the keys that are guaranteed in the output are:
    # "x_label", "y_label", "title", "label_spacing"
    ou = dict()
    for p in ["x_label","y_label","title"]:
        if p in args:
            ou[p] = args[p]
        else:
            ou[p] = ""
    if "label_spacing" in args:
        ou["label_spacing"] = args["label_spacing"]
    else:
        ou["label_spacing"] = 1
    return ou

def single_channel(infile,outfile,**args):
    # infile is a string refering to a csv file with binned data
    # outfile is a string indicating a nonexistent file that the output should be saved to
    # outfile should end in .png
    # this function makes a plot of the data in infile and saves it to outfile
    # args may contain "title", "x_label", "y_label", "label_spacing"
    # these are string, string, string, and int
    v = set_arg_values(args)
    indata = qcsv.from_file(infile)
    ex.single_channel_confirm_format(indata)
    mm = ex.single_channel_get_mm(indata)
    values = []
    names = []
    for i in range(mm["bins"]):
        values.append(float(indata[i+1][0]))
        if i % v["label_spacing"] == 0:
            names.append(sig_figs(mm["min"]+mm["width"]*float(i),3))
        else:
            names.append("")
    # now plot it
    plt.figure(1)
    plt.clf()
    plt.title(v["title"])
    plt.xlabel(v["x_label"])
    plt.ylabel(v["y_label"])
    y_pos = np.arange(len(values))
    plt.bar(y_pos, values, align='center')
    plt.xticks(y_pos,names)
    plt.savefig(outfile)

def double_channel_make_table(d):
    # when the data is loaded from the csv file, each datapoint is encoded as a string
    # we want to turn them into floats
    # that's what this function does
    ou = []
    for i in range(1,len(d)):
        k = []
        for j in range(len(d[i])):
            k.append(float(d[i][j]))
        ou.append(k)
    return ou

def double_channel(infile,outfile,**args):
    # infile is a string refering to a csv file with binned data
    # outfile is a string indicating a nonexistent file that the output should be saved to
    # outfile should end in .png
    # this function makes a plot of the data in infile and saves it to outfile
    # args may contain "title", "x_label", "y_label"
    # all three are strings
    v = set_arg_values(args)
    indata = qcsv.from_file(infile)
    ex.double_channel_confirm_format(indata)
    mm = ex.double_channel_get_mm(indata)
    bounds = [ mm["x"]["min"], mm["x"]["max"], mm["y"]["min"], mm["y"]["max"] ]
    table = double_channel_make_table(indata)
    # now plot it
    plt.figure(1)
    plt.clf()
    plt.title(v["title"])
    plt.xlabel(v["x_label"])
    plt.ylabel(v["y_label"])
    plt.imshow(table, cmap="hot", origin="lower", extent=bounds)
    plt.colorbar()
    plt.savefig(outfile)
