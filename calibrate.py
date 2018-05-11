import quick_csv as qcsv

def colmul(chans,coef):
    # chans is list (string), where the strings encode integers
    # coef is passed from calibrate function
    # this function returns list (float)
    # this list has the same length as chans
    # the nth element is the thing that the nth column will be multiplied by
    ou = []
    for c in chans:
        n = int(c)
        if n not in coef:
            raise Exception("There is no calibration coefficient specified for channel "+c)
        ou.append(coef[n])
    return ou

def build_output(indata,coef_list):
    # this iterates over the entire csv file
    # calibrating each measurement
    column_count = len(coef_list)
    ou = []
    ou.append(indata[0]) # we want to keep the same headers
    for row_num in range(1,len(indata)): # this hits every row except the headers
        k = []
        for col_num in range(column_count):
            v = indata[row_num][col_num]
            v = float(v) # it comes in as a string, so we have to convert it
            v = v*coef_list[col_num] # the actual calibration
            k.append(v)
        ou.append(k)
    return ou

def calibrate(infile,outfile,coef):
    # infile and outfile are strings
    # they indicate the input and output file names and paths
    # coef is dict (int->float)
    # the keys are channel numbers, the values are the numbers by which the integration sums
    # for that channel should be multiplied
    # first load the data
    indata = qcsv.from_file(infile)
    # now we want to know what scalar value to multiply each column by
    coef_list = colmul(indata[0],coef) # indata[0] should be the channel numbers
    # now we build an output
    ou = build_output(indata,coef_list)
    # and now we save it
    qcsv.to_file(outfile,ou)
