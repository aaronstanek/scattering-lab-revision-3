import get_files_in_folder as gfif
import read_json_ord_clump as rjoc
import integrate_json_ord_clump as ijoc
import quick_csv as qcsv

def prepare_to_dump(channels,data):
    # this function just changes the format of the data
    # it prepares it to be dumped to a csv file
    # each sublist in ou represents a row of the csv file
    ou = []
    ou.append(channels)
    for file in data:
        for event in file:
            # event is a dict(int->float)
            # k is a list(float)
            # we are just replacing the dict with a tuple
            k = []
            for c in channels:
                k.append(event[c])
            ou.append(k)
    return ou

def integrate_to_csv(folderpath,outputfile):
    # folderpath and outputfile are both strings
    # folderpath should point to an existing directory
    # outputfile should point to a .csv file, it does not need to exist in advance
    # but the directory where the file is to be put must exist in advance
    files = gfif.get_files_in_folder(folderpath)
    ll_sums = [] # This is a list. The elements are the outputs of integrate_json_ord_clump.
    # so it is a list of lists of dicts (int->float)
    for f in files: # f is the name of a .ord.json file
        v = rjoc.read_json_ord_clump_basic(f)
        # v is a list of events v[0] and the time between measurements v[1]
        i = ijoc.integrate_json_ord_clump(v[0],v[1])
        # i is a list of dicts (int->float) that maps channels to integral sums
        ll_sums.append(i)
    # clean up a bit
    del(files)
    try:
        del(f)
    except:
        pass
    try:
        del(v)
    except:
        pass
    try:
        del(i)
    except:
        pass
    # done cleaning up
    # we only have ll_sums left
    channels = list(ll_sums[0][0]) # get the first event of the first file, return the keys of this dict as a list
    channels.sort() # channels is list (int)
    ou = prepare_to_dump(channels,ll_sums)
    # clean up
    del(ll_sums)
    del(channels)
    # done cleaning up
    # we only have ou left
    qcsv.to_file(outputfile,ou)
