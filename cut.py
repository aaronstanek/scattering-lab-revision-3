import quick_csv as qcsv

class cut_instruction:
    def __init__(self,channel,direction,value):
        self.channel = channel # which channel does this apply to? (int)
        self.direction = direction # remove above or below? (string) "a" for above, "b" for below
        self.value = value # where to make the cut? (float)
        if (direction != "a") and (direction != "b"):
            raise Exception("cut_instruction direction must be \"a\" or \"b\"")
    def cut_value(self,v):
        # v is a float
        # we want to know if v is included in the output or gets cut
        # this function returns True if v gets cut
        if self.direction == "a":
            # remove above self.value
            if v>self.value:
                return True
            else:
                return False
        else:
            # remove below self.value
            if v<self.value:
                return True
            else:
                return False

def sort_instructions(chans,cutinfo):
    # chans is list (string) where the strings encode integers
    # cutinfo is described below
    # this function returns list (list (cut_instruction))
    # the nth sublist of this list will apply cuts to the nth column of the csv file
    # this way we don't have to keep checking which channel we are working in
    # if we are in the nth column of the file, we check the nth sublist to see what cuts to make
    ou = []
    for c in chans:
        n = int(c)
        k = [] # this is the list of cut_instruction that apply to channel n
        for x in cutinfo:
            if x.channel == n: # if a cut_instruction applies to this channel, add it to k
                k.append(x)
        ou.append(k)
    return ou

def apply_cuts(indata,si):
    # indata is described below
    # si is sorted_instructions, it is the output of sort_instructions, described above
    column_count = len(si)
    ou = []
    ou.append(indata[0]) # we want to keep the same headers
    for row_num in range(1,len(indata)):
        include = True # this tells us if we should include this event in the output
        for col_num in range(column_count):
            v = indata[row_num][col_num]
            v = float(v) # it comes in as a string, we need to convert it
            for c in si[col_num]:
                # look at all the cuts that apply to this column/channel
                # these cuts are stored in si[col_num]
                # iterate over them
                if c.cut_value(v): # if the cut_instruction says to cut this value, then do not include this row in the output
                    include = False
                    break
            # break statement jumps to here
            if include == False:
                break # if this row is being rejected, there is no point in checking the rest of it
        # break statement jumps to here
        # after we have tested a row's worthiness, we land at this line
        # if include is True, then no cut_instruction said to cut this row
        # if include is False, then at least one cut_instruction said to cut this row
        if include:
            ou.append(indata[row_num])
    return ou

def cut(infile,outfile,cutinfo):
    # infile and outfile are strings
    # they indicate the input and output file names and paths
    # cutinfo is list (cut_instruction)
    indata = qcsv.from_file(infile)
    sorted_instructions = sort_instructions(indata[0],cutinfo) # sorts cut_instruction by the channel to which they apply
    ou = apply_cuts(indata,sorted_instructions)
    qcsv.to_file(outfile,ou)
