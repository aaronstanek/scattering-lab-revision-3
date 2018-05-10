import json

def read_json_ord_clump_basic(filename):
    # this function takes a filename
    # and returns a list of events
    # each event is encoded as dict
    # it has a second return value of the time between measurements
    infile = open(filename,"r")
    indata = infile.read()
    infile.close()
    block = json.loads(indata)
    # the block is all the data in the file
    # we only want the time and the events
    t = float(block["OSC_META"]["DISPLAY_TIMEDIVISION"])
    # t is now the time between measurements, encoded as a float
    ev = block["EVENTS"]
    # ev is a list of events
    return [ev,t]
