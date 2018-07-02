import quick_csv as qcsv
import bins

def merge_min_max(a,b):
    ou = dict()
    ou["min"] = min(a["min"],b["min"])
    ou["max"] = max(a["max"],b["max"])
    return ou
