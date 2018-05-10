import os
from correct_ending_slash import *

def get_files_in_folder(folder_path):
    # returns a list of all files in a particular folder
    dirpath = correct_ending_slash(folder_path)
    ls = os.listdir(dirpath)
    # ls is a list of files and subdirectories
    # we want to omit the subdirectories
    ou = []
    for x in ls:
        fullpath = dirpath + x # adding strings is safe because dirpath will always have an ending slash
        if os.path.isfile(fullpath):
            ou.append(fullpath)
    return ou # ou is a list of full pathnames to the desired files
