def correct_ending_slash(folder_path):
    # this function ensures that we always terminate directory pathnames with a slash character
    if folder_path[-1]!="/" and folder_path[-1]!="\\":
        return folder_path+"/"
    return folder_path
