import csv

def to_file(filename,data):
    # filename is a string
    # data is a 2D array, list of rows, each row is a list of elements
    # elements are strings (numbers also acceptable, but they will be read as strings)
    outfile = open(filename,"w",newline="")
    outfile.truncate(0)
    outfile.seek(0,0)
    c = csv.writer(outfile, dialect="excel")
    for row in data:
        c.writerow(row)
    outfile.close()

def from_file(filename):
    # filename is a string
    # returns 2D array, list of rows
    # each row containing string objects
    infile = open(filename,"r",newline="")
    c = csv.reader(infile, dialect="excel")
    ou = []
    for row in c:
        ou.append(row)
    infile.close()
    return ou
